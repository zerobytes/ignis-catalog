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


Static mesh records add `mesh` (full vertices/triangles/world bounds) and
`native_preview` (separate counts/bounds, IGMP1+gzip format, quality,
tessellation, decoded size and SHA-256). Source files can be a versioned ZIP
containing the editable source, full mesh, materials and a file-level checksum
list. A remote compressed preview and a small local native-capture thumbnail
are listed separately. The offline validator verifies local content and shape;
release/deployment tooling verifies the remote payload bytes.


Prepared native coatings can make a full tree exceed the botanical source mesh's
old 3M-vertex / 6M-triangle envelope. Full and preview count metadata now accepts
positive u32 counts, matching indexed mesh/GLB representation rather than imposing
that old source-only cap on the combined tree. This does not raise the browser's
192 MiB decoded packet guard or relax geometry checks in the native exporter.
`native_preview.material_appearance = representative-pbr-colors` explicitly marks
previews whose native textures/attribute domains are approximated. The portal
must disclose that distinction; the native download retains full appearance.
