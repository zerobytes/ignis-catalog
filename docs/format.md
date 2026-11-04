# Catalog manifest v1

Each `assets/<kind>/<family>/<slug>/asset.json` is a source record. `catalog.json`
is the deterministic generated index. Run `python3 tools/catalog.py build` after
edits. Tooling requires Python 3.10+ and no packages.

- `format_version`: 1; stable namespaced `id`; semantic content `version`.
- `name`, `summary`, `kind`, `tags`: discovery. Accepted kinds: material, mesh,
  plant, character, animation, audio, vfx, scene. Only materials have content now;
  accepting metadata does not prove engine support for every kind.
- `license`: CC-BY-4.0 or CC0-1.0; `author`: name/HTTPS profile; `attribution`:
  copyable credit including source, license link and change notice. First-party
  assets use CC BY 4.0 by explicit author decision.
- `provenance`: repository HTTPS URL, pinned 40-character Git commit, original
  relative path, availability and note. `local-unpublished` means the source
  commit was not on GitHub when transferred; no claim of a working remote source
  link is made. The complete licensed source bytes are present in this catalog.
  Non-Git provenance needs a future format extension, never invented commits.
- `compatibility`: engine `ignis`, runtime validation scope; materials also state
  minimum scene format and material library version. These feature minima are
  not certification of all executable revisions/platforms.
- `files`: role `source`, `preview` or `download`; MIME `media_type`, positive
  `bytes`, SHA-256; exactly one repository-relative `path` or HTTPS `url`.
  Remote files can have HTTPS `mirrors` containing identical bytes. At least one
  editable source is required. No executable hooks.

Local files must belong to their manifest directory, be normalized without `..`
or symlinks, all listed, <=1 MiB each and <=256 MiB combined. External size is
recorded but does not count against the local payload budget. Validation never
fetches remote content. Local material JSON is checked for library envelope and
version; semantic/render validation belongs to the engine and was not rerun for
this unchanged source transfer.

IDs remain stable when titles change. Increment content versions when bytes,
license, attribution or compatibility change. Keep pinned packages available.
The index selects one current version per asset, not a dependency/version solver.

No engine installer, account/payment/rating backend, dependency resolver or
automatic migration of built-in engine presets is delivered in v1.
