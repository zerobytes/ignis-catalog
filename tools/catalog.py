#!/usr/bin/env python3
"""Validate and index the catalog offline. No dependencies or asset execution."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import sys
from urllib.parse import urlsplit

ROOT = Path(__file__).resolve().parents[1]
KINDS = {'material', 'mesh', 'plant', 'character', 'animation', 'audio', 'vfx', 'scene'}
LICENSES = {'CC-BY-4.0', 'CC0-1.0'}
MAX_LOCAL_FILE = 1024 * 1024
MAX_LOCAL_TOTAL = 256 * 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def text(value):
    return isinstance(value, str) and bool(value.strip())


def https(value):
    require(text(value), 'URL must be a string')
    parsed = urlsplit(value)
    require(parsed.scheme == 'https' and parsed.hostname and not parsed.username
            and not parsed.password and not parsed.fragment, 'Expected a public HTTPS locator')


def safe_path(value):
    require(text(value) and '\\' not in value, 'Invalid relative path')
    path = PurePosixPath(value)
    require(not path.is_absolute() and '..' not in path.parts and str(path) == value,
            'Path must be normalized and relative, without traversal')
    return path


def regular_file(root, value):
    rel = safe_path(value)
    current = root
    for part in rel.parts:
        current = current / part
        require(not current.is_symlink(), f'Symlinks are not supported: {value}')
    require(current.is_file() and current.resolve().is_relative_to(root.resolve()),
            f'Missing or escaping file: {value}')
    return current


def records(root=ROOT):
    result, ids, claimed, total = [], set(), set(), 0
    for path in sorted((root / 'assets').rglob('asset.json')):
        regular_file(root, path.relative_to(root).as_posix())
        require(path.stat().st_size <= MAX_LOCAL_FILE, 'Manifest exceeds local size budget')
        item = json.loads(path.read_text())
        require(item['format_version'] == 1, 'Unsupported manifest version')
        asset_id = item['id']
        require(isinstance(asset_id, str) and re.fullmatch(r'[a-z0-9]+(?:[.-][a-z0-9]+)+', asset_id), 'Invalid asset ID')
        require(asset_id not in ids, f'Duplicate ID: {asset_id}')
        ids.add(asset_id)
        require(re.fullmatch(r'\d+\.\d+\.\d+', item['version']), 'Expected semantic asset version')
        require(item['kind'] in KINDS and item['license'] in LICENSES, 'Unsupported kind/license')
        for key in ('name', 'summary', 'attribution'):
            require(text(item[key]), f'Missing {key}')
        require(text(item['author']['name']), 'Missing author')
        https(item['author']['url'])
        require(isinstance(item['tags'], list) and item['tags']
                and all(text(t) for t in item['tags']), 'Expected nonempty tags')
        origin = item['provenance']
        https(origin['repository'])
        require(re.fullmatch(r'[a-f0-9]{40}', origin['commit']), 'Expected pinned source commit')
        safe_path(origin['path'])
        compatibility = item['compatibility']
        require(compatibility['engine'] == 'ignis', 'Unsupported engine')
        require(text(compatibility['runtime_validation']), 'Missing validation scope')
        if item['kind'] == 'mesh':
            for geometry in (item['mesh'], item['native_preview']):
                require(type(geometry['vertices']) is int and 0 < geometry['vertices'] <= 3_000_000, 'Invalid mesh vertex budget')
                require(type(geometry['triangles']) is int and 0 < geometry['triangles'] <= 6_000_000, 'Invalid mesh triangle budget')
                bounds = geometry['bounds']
                require(all(isinstance(bounds[k], list) and len(bounds[k]) == 3 for k in ('min','max')), 'Invalid mesh bounds')
                import math
                require(all(isinstance(v, (int, float)) and math.isfinite(v) for k in bounds for v in bounds[k]), 'Invalid mesh bounds')
                require(all(a <= b for a, b in zip(bounds['min'], bounds['max'])), 'Invalid mesh bounds')
            preview = item['native_preview']
            require(preview['format'] == 'IGMP1+gzip' and preview['quality'] in {'full', 'reduced-tessellation'}, 'Unsupported native mesh preview')
            require(type(preview['decoded_bytes']) is int and 0 < preview['decoded_bytes'] <= 192 * 1024 * 1024, 'Invalid decoded preview budget')
            require(re.fullmatch(r'[a-f0-9]{64}', preview['decoded_sha256']), 'Missing decoded preview hash')
        files = item['files']
        require(isinstance(files, list) and files, 'Asset has no files')
        require(any(f['role'] == 'source' for f in files), 'Editable source is required')
        for file in files:
            require(file['role'] in {'source', 'preview', 'download'}, 'Invalid file role')
            require(text(file['media_type']), 'Missing media type')
            require(type(file['bytes']) is int and file['bytes'] > 0, 'Invalid byte size')
            require(re.fullmatch(r'[a-f0-9]{64}', file['sha256']), 'Expected SHA-256')
            require(('path' in file) != ('url' in file), 'Use exactly one path or URL')
            if 'url' in file:
                https(file['url'])
                for mirror in file.get('mirrors', []):
                    https(mirror)
                continue  # Offline validation does not verify remote availability/content.
            target = regular_file(root, file['path'])
            require(target.is_relative_to(path.parent), 'Local asset file must belong to its manifest directory')
            require(file['path'] not in claimed, 'Local file claimed more than once')
            claimed.add(file['path'])
            require(target.stat().st_size <= MAX_LOCAL_FILE, 'Large payloads must use external downloads')
            payload = target.read_bytes()
            require(len(payload) == file['bytes'], f'Size mismatch: {target}')
            require(hashlib.sha256(payload).hexdigest() == file['sha256'], f'Hash mismatch: {target}')
            total += len(payload)
            if target.suffix == '.ignis-material':
                material = json.loads(payload)
                require(material['version'] == compatibility['material_library_version'], 'Library version mismatch')
                require(isinstance(material['material'], dict), 'Invalid material envelope')
                require(type(compatibility['minimum_scene_version']) is int
                        and compatibility['minimum_scene_version'] > 0, 'Invalid minimum scene version')
        result.append(dict(item, manifest=path.relative_to(root).as_posix()))
    require(result, 'Catalog is empty')
    payloads = {p.relative_to(root).as_posix() for p in (root / 'assets').rglob('*')
                if p.is_file() and p.name != 'asset.json'}
    require(payloads == claimed, 'Unlisted local asset files')
    require(total <= MAX_LOCAL_TOTAL, 'Repository payload budget exceeded; use external hosting')
    return sorted(result, key=lambda item: item['id'])


def encoded(root=ROOT):
    return json.dumps({'format_version': 1, 'name': 'Ignis Catalog', 'assets': records(root)},
                      indent=2, ensure_ascii=False) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['validate', 'build', 'list', 'info'])
    parser.add_argument('query', nargs='?', default='')
    parser.add_argument('--check', action='store_true', help='Check generated index without writing')
    args = parser.parse_args()
    try:
        data = records()
        if args.command == 'build':
            output = ROOT / 'catalog.json'
            content = encoded()
            if args.check:
                require(output.read_text() == content, 'catalog.json is stale; run build')
            else:
                output.write_text(content)
        elif args.command == 'list':
            query = args.query.casefold()
            for item in data:
                if query in ' '.join([item['id'], item['name'], *item['tags']]).casefold():
                    print(f"{item['id']}\t{item['version']}\t{item['name']}\t{item['license']}")
            return 0
        elif args.command == 'info':
            item = next((i for i in data if i['id'] == args.query), None)
            require(item is not None, 'Asset ID not found')
            print(json.dumps(item, indent=2, ensure_ascii=False))
            return 0
        print(f'OK: {len(data)} assets; local hashes, attribution and manifests validated')
        return 0
    except (ValueError, KeyError, TypeError, OSError, StopIteration) as error:
        print(f'Catalog error: {error}', file=sys.stderr)
        return 1


if __name__ == '__main__':
    sys.exit(main())
