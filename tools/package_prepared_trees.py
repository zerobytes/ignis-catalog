#!/usr/bin/env python3
"""Package authored static trees with native moss, editable sources and portable previews."""
import argparse
import gzip
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import zipfile

CATALOG=Path(__file__).resolve().parents[1]


def digest(path):
    h=hashlib.sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):h.update(block)
    return h.hexdigest()


def record(path,role,media):
    return dict(role=role,media_type=media,bytes=path.stat().st_size,sha256=digest(path))


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--engine',type=Path,required=True)
    parser.add_argument('--only')
    args=parser.parse_args()
    engine=args.engine.resolve()
    plan_path=CATALOG/'recipes/ancestral/authoring.json'
    subprocess.run(['git','diff','--exit-code','HEAD','--',str(plan_path.relative_to(CATALOG))],cwd=CATALOG,check=True,stdout=subprocess.DEVNULL)
    revision=subprocess.check_output(['git','rev-parse','HEAD'],cwd=CATALOG,text=True).strip()
    plan_bytes=subprocess.check_output(['git','show',revision+':recipes/ancestral/authoring.json'],cwd=CATALOG)
    plan=json.loads(plan_bytes)
    output=engine/'artifacts/catalog-ancestral'
    tag='ancestral-v1.0.0'
    base=f'https://github.com/zerobytes/ignis-catalog/releases/download/{tag}/'
    for item in plan['variants']:
        asset_id=item['id'];slug=asset_id.removeprefix('ignis.mesh.tree.')
        if args.only and args.only!=slug:continue
        stage=output/slug
        authored=json.loads((stage/'authoring.json').read_text())
        source=stage/'source.ignis-botany'
        if authored['original_sha256']!=item['original_sha256'] or digest(source)!=authored['source_sha256']:
            raise ValueError('Authored source differs from pinned original/result')
        inputs=stage/'export-input.json'
        inputs.write_text(json.dumps([dict(id=asset_id,path=str(source),prepared_scene=str(stage/'tree.scene.json'),
            thumbnail=str(stage/'thumbnail.png'),materials={},portable_colors=True)]))
        subprocess.run([str(engine/'target/release/examples/export_web_meshes'),str(inputs),str(stage/'export')],check=True)
        exported=stage/'export'/asset_id
        full=json.loads((exported/'mesh.json').read_text())
        preview=json.loads((exported/'preview.json').read_text())
        packed=output/(asset_id+'.igmpz')
        raw=exported/'preview.igmp'
        decoded=record(raw,'preview','application/vnd.ignis.mesh-preview')
        with raw.open('rb') as src,packed.open('wb') as dst,gzip.GzipFile(fileobj=dst,mode='wb',mtime=0) as compressed:
            shutil.copyfileobj(src,compressed)
        target=CATALOG/'assets/meshes/trees'/slug
        target.mkdir(parents=True,exist_ok=True)
        subprocess.run(['sips','-Z','320','-s','format','jpeg','-s','formatOptions','85',str(stage/'thumbnail.png'),'--out',str(target/'thumbnail.jpg')],check=True,stdout=subprocess.DEVNULL)
        def stats(meta):
            return dict(vertices=sum(p['vertices'] for p in meta['parts']),triangles=sum(p['indices']//3 for p in meta['parts']),bounds=meta['bounds'])
        metadata=dict(id=asset_id,name=item['name'],source_sha256=digest(source),original_sha256=item['original_sha256'],
            engine_build=authored['build'],native=stats(full),preview=stats(preview),prepared_world_moss=True,
            native_recipe_version=34,native_scene_version=138,portable_appearance='representative-pbr-colors')
        (stage/'package.json').write_text(json.dumps(metadata,indent=2)+'\n')
        plan_snapshot=stage/'catalog-authoring.json';plan_snapshot.write_bytes(plan_bytes)
        files={'source.ignis-botany':source,'tree.scene.json':exported/'tree.scene.json','mesh.glb':exported/'mesh.glb',
               'ancestral.ignis-species':CATALOG/'recipes/ancestral/ancestral.ignis-species','authoring.json':plan_snapshot,
               'package.json':stage/'package.json','LICENSE.txt':CATALOG/'LICENSES/CC-BY-4.0.txt'}
        checks={name:record(path,'source','application/octet-stream') for name,path in files.items()}
        readme=f'''# {item['name']}\n\nBy Guilherme Oliveira / Zerobytes. CC BY 4.0.\nCredit: "{item['name']} by Guilherme Oliveira / Zerobytes — CC BY 4.0 — https://github.com/zerobytes/ignis-catalog". Link the license and indicate modifications.\n\nOpen tree.scene.json in an Ignis editor supporting scene 138 / botanical recipe 34.\nIt contains the complete static tree, full native bark/foliage/moss materials and\nan independently prepared geometric moss layer. The ordinary runtime draws the\nsaved meshes; it does not regenerate moss. Rotate/place the tree first and run\nVegetation > Prepare world moss after placement, growth or structural changes.\nThe supplied source is at the origin with a recorded long-term environment.\n\nsource.ignis-botany is the complete editable organ graph and material settings.\nancestral.ignis-species is a compact related species profile for generating new\nindividuals; it is not a byte-exact reconstruction of the custom original tree.\nauthoring.json pins the approved input hashes, palettes and environmental settings.\npackage.json identifies this asset's output source hash and native build.\n\nmesh.glb retains full mesh geometry, transforms and representative PBR colors.\nPortable GLB and web previews approximate the native textures and moss border\nshading with colors; they do not contain the full native texture appearance.\nThe web preview also reduces axis/leaf tessellation and moss mesh resolution.\nThe native scene is the full-appearance editable delivery.\n\nFull geometry: {metadata['native']['vertices']:,} vertices / {metadata['native']['triangles']:,} triangles.\nNo reference imagery, extracted game models or proprietary vendor textures are included.\nThese are authored fantasy trees, not field-calibrated biological simulations.\nAsset licensing does not relicense the separately distributed Ignis engine.\n'''
        archive=output/(asset_id+'.zip');partial=archive.with_suffix('.zip.part')
        with zipfile.ZipFile(partial,'w',zipfile.ZIP_DEFLATED,compresslevel=6) as z:
            for name,path in files.items():z.write(path,name)
            z.writestr('README.md',readme)
            z.writestr('checksums.json',json.dumps(checks,indent=2)+'\n')
        with zipfile.ZipFile(partial) as z:
            for name,expected in checks.items():
                h=hashlib.sha256()
                with z.open(name) as f:
                    for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
                if h.hexdigest()!=expected['sha256']:raise ValueError('Package member checksum failure')
        partial.replace(archive)
        download=record(archive,'source','application/zip');download['url']=base+archive.name
        web=record(packed,'preview','application/vnd.ignis.mesh-preview+gzip');web['url']=base+packed.name
        thumb=record(target/'thumbnail.jpg','preview','image/jpeg');thumb['path']=(target/'thumbnail.jpg').relative_to(CATALOG).as_posix()
        manifest=dict(format_version=1,id=asset_id,version='1.0.0',kind='mesh',name=item['name'],
            summary='Editable ancestral fantasy tree with continuous root/trunk/branch cords and independently prepared moss.',
            author=dict(name='Guilherme Oliveira / Zerobytes',url='https://github.com/zerobytes'),license='CC-BY-4.0',
            attribution=f"{item['name']} by Guilherme Oliveira / Zerobytes — CC BY 4.0 — https://github.com/zerobytes/ignis-catalog",
            tags=['trees','mesh','botany','ancestral','moss',slug],
            provenance=dict(repository='https://github.com/zerobytes/ignis-catalog',commit=revision,path='recipes/ancestral/authoring.json',
                source_sha256=digest(source),availability='versioned-download',note='Tracked compact authoring profile and input hashes; complete exact prepared botanical snapshot and native scene included in the release ZIP. No reference images included.'),
            compatibility=dict(engine='ignis',botany_recipe_version=34,minimum_scene_version=138,
                runtime_validation='Native source bake, explicit world moss preparation, scene validation and native renderer capture. Static snapshots; no FPS certification.'),
            mesh=metadata['native'],native_preview=dict(format='IGMP1+gzip',quality='reduced-tessellation',
                material_appearance='representative-pbr-colors',tessellation=preview['tessellation'],decoded_bytes=decoded['bytes'],decoded_sha256=decoded['sha256'],**metadata['preview']),
            files=[download,web,thumb])
        (target/'asset.json').write_text(json.dumps(manifest,indent=2,ensure_ascii=False)+'\n')
        (stage/'publication.json').write_text(json.dumps(dict(asset=manifest,package=metadata),indent=2)+'\n')
        shutil.rmtree(stage/'export')
        print(json.dumps(dict(id=asset_id,zip_bytes=download['bytes'],preview_bytes=web['bytes'],native=metadata['native'],preview=metadata['preview'])),flush=True)


if __name__=='__main__':main()
