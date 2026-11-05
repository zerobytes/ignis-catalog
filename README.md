# Ignis Catalog

A free community asset catalog for [Ignis](https://github.com/zerobytes/ignis).
[Português](README.pt-BR.md)

Reusable content with editable sources, explicit licenses, attribution and
versioned integrity metadata. The collection contains **11 editable tree meshes and 20 procedural materials**: 12 marble
families, 4 continuous stone families and 4 basic surfaces. Material sources total
**38,609 bytes**. Tree packages are versioned downloads outside Git. No account, paid backend or Git LFS required.

**[Explore the asset portal](https://ignis.web.app/catalog/?lang=en)** inside the
Ignis website. Its interactive browser preview uses native Ignis WGSL material
shaders and GPU packets. [GitHub Pages mirror](https://zerobytes.github.io/ignis/catalog/?lang=en).
Editor installation and more asset families remain [next steps](docs/roadmap.md).

## Browse and use

Download a linked `.ignis-material` and load it onto a mesh through
**Aparência → Biblioteca de materiais** in a compatible Ignis editor. Keep runtime
evaluation or generate fixed maps explicitly. The engine generates the surface;
these files are editable recipes, not baked high-resolution texture sets.
Each adjacent `asset.json` states exact attribution, origin and compatibility.
Scene minima identify format capabilities, not tested minimum executable releases.

| Editable material source | Family | Minimum scene version |
| --- | --- | --- |
| [Ceramic](assets/materials/basic/ceramic/ceramic.ignis-material) | basic | 112 |
| [Painted Metal](assets/materials/basic/painted-metal/painted-metal.ignis-material) | basic | 112 |
| [Stone](assets/materials/basic/stone/stone.ignis-material) | basic | 112 |
| [Wood](assets/materials/basic/wood/wood.ignis-material) | basic | 112 |
| [Azul](assets/materials/marble/azul/azul.ignis-material) | marble | 115 |
| [Calacatta](assets/materials/marble/calacatta/calacatta.ignis-material) | marble | 115 |
| [Carrara](assets/materials/marble/carrara/carrara.ignis-material) | marble | 115 |
| [Emerald Gold](assets/materials/marble/emerald-gold/emerald_gold.ignis-material) | marble | 115 |
| [Emerald White Gold](assets/materials/marble/emerald-white-gold/emerald_white_gold.ignis-material) | marble | 115 |
| [Emperador](assets/materials/marble/emperador/emperador.ignis-material) | marble | 115 |
| [Nero Marquina](assets/materials/marble/nero-marquina/nero_marquina.ignis-material) | marble | 115 |
| [Portoro](assets/materials/marble/portoro/portoro.ignis-material) | marble | 115 |
| [Rosa](assets/materials/marble/rosa/rosa.ignis-material) | marble | 115 |
| [Rosso Levanto](assets/materials/marble/rosso-levanto/rosso_levanto.ignis-material) | marble | 115 |
| [Statuario](assets/materials/marble/statuario/statuario.ignis-material) | marble | 115 |
| [Verde Breccia](assets/materials/marble/verde-breccia/verde_breccia.ignis-material) | marble | 115 |
| [Alpine](assets/materials/rock/alpine/alpine.ignis-material) | rock | 119 |
| [Fractured](assets/materials/rock/fractured/fractured.ignis-material) | rock | 119 |
| [Ochre](assets/materials/rock/ochre/ochre.ignis-material) | rock | 119 |
| [Sedimentary](assets/materials/rock/sedimentary/sedimentary.ignis-material) | rock | 119 |

Clone to search, inspect and validate offline (Python 3.10+, no packages):

```sh
git clone https://github.com/zerobytes/ignis-catalog.git
cd ignis-catalog
python3 tools/catalog.py list rock
python3 tools/catalog.py info ignis.material.rock.alpine
python3 tools/catalog.py validate
python3 tools/catalog.py build --check
python3 -m unittest discover -s tests -v
```

## Tree meshes

Eight trees are available in [trees-v1.0.0](https://github.com/zerobytes/ignis-catalog/releases/tag/trees-v1.0.0):
areca palm, plane tree, eucalyptus, broad-crown fig, countryside fig, and three
golden birch variants. [Mesh manifests](assets/meshes/trees) contain download
URLs, SHA-256, exact sizes, original provenance and full/preview geometry counts.

Each ZIP contains the unchanged botanical source, a complete editable Ignis scene
with its native materials/source binding, full-geometry GLB, license and checksums.
Open `tree.scene.json` in a compatible Ignis editor. GLB preserves geometry and
uses representative portable PBR colors; native procedural patterns remain in the
Ignis files. The portal renders actual native mesh data with the Ignis shader,
using reduced preview tessellation (axis8 / sides6 / blade4), explicitly labelled.
Palmate leaves retain the native contour resolution. All organs are retained;
the download is full resolution. No reference images or unfinished game content
are included. Assets are authored, not scientifically calibrated botanical models.

Previews load only when activated; their transfer size is displayed. Large
payloads are pinned to this release and verified before use. The catalog can add
other static mesh families using the same records and package format.

### Areca palm 1.1.0

The [updated areca palm](https://github.com/zerobytes/ignis-catalog/releases/tag/palmeirinha-v1.1.0)
has continuous petiole-to-rachis curves with increasing tip curvature and authored
young/developed leaf sizes. The editable source includes growth-stage and height
variation controls (default 0.8). Native editing requires botanical recipe/source
format 9; browser preview and full-resolution GLB remain static presentations.
The original 1.0.0 package remains pinned in the initial tree release.

## Hosting and contribution

Recipes and metadata stay in Git. Large meshes, texture exports and other packages
use versioned Releases or the publisher's HTTPS hosting. Records contain size,
SHA-256 and optional mirrors, making discovery independent of storage.
[Hosting policy and official limits](docs/storage.md) ·
[Manifest contract](docs/format.md) · [Contribute](CONTRIBUTING.md).

No engine history was imported. Initial recipes are byte-for-byte copies from
the working engine snapshot identified in every manifest, independently licensed
by their author. Those engine commits were **not yet published** at transfer time;
provenance explicitly records `local-unpublished`. All recipe bytes are included
here. Existing engine examples remain intact pending coordinated migration.
Compatibility comes from the feature documentation; this transfer verifies
integrity, not new rendering or artistic acceptance.

## License and credits

Our assets, metadata and documentation: **CC BY 4.0**. Scripts/tests/workflow: **MIT**.
See [LICENSE](LICENSE) and individual manifests. Credit Guilherme Oliveira /
Zerobytes, link the asset and [license](https://creativecommons.org/licenses/by/4.0/),
and indicate modifications. Example:

> Alpine — Guilherme Oliveira / Zerobytes, CC BY 4.0.
> Source: https://github.com/zerobytes/ignis-catalog . Modified: describe changes.

The engine retains its separate license. This project is not affiliated with
Epic Games or Fab; asset licensing grants no rights over third-party trademarks
or unlicensed reference imagery.
