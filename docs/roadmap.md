# Roadmap

Delivered foundation: independent repository/history, 20 compact editable material
sources, licensing/credits, manifests, reproducible index, offline search/info,
integrity checks, contribution workflow and hosting policy.

Delivered portal: [Ignis Catalog](https://ignis.web.app/catalog/) inside the existing
engine website, with EN/PT search/filter, licensed native thumbnails, credits,
source downloads and interactive WebGPU previews of all twenty materials using
native Ignis WGSL and packed GPU data. This is an opaque-material preview host,
not the complete editor, simulation or a universal asset player.

Next increments, each requiring implementation and acceptance:

1. Versioned release tooling and remote link-health checks, explicit unavailable
   states, mirrors and contributor review.
2. Ignis editor integration: browse/download selected content, verify integrity,
   import atomically, retain credits, track versions and offline cache.
3. Plants, meshes, animation, audio and VFX with native sources and compatibility
   checks specific to each kind.
4. Larger community publishing/review and optional sponsorship. A paid marketplace
   is outside this free launch and requires reviewing hosting and workflows.

Engine presets/examples remain in place to preserve ongoing work. The catalog is
the independent home for new catalog content. Removing built-in recipes/changing
loaders is a separate coordinated migration. The browser host and native export
bridge are maintained in the Ignis engine/site project, independently of asset licensing.
