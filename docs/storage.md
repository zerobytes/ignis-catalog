# Hosting without a paid service

Policy checked on 2026-11-04. A zero-budget launch is practical; unlimited free
hosting at arbitrary scale is not guaranteed. No paid service is required or
configured by this repository.

| Content | Initial home | Growth policy |
| --- | --- | --- |
| Metadata, licenses, compact editable recipes | Public GitHub repository | Review additions and keep history small |
| Preview thumbnails | Small optimized files beside manifests | Full-resolution renders/videos stay external |
| Large distributable assets | Versioned Releases or the author's HTTPS host | Exact version, byte count, SHA-256, optional mirrors |
| Browse/search website | Existing Ignis site, static frontend | Index and thumbnails only |
| Imported assets | User's project/cache | Download selected assets, not the entire catalog |

The initial 20 material sources total **38,609 bytes**, about 37.7 KiB. They are
procedural recipes, not baked high-resolution texture collections. Storing the
recipe enables editable variations without storing every generated map. Surface
generation still requires a compatible engine and its CPU/GPU work.

## Official provider limits

- [GitHub Releases](https://docs.github.com/en/repositories/releasing-projects-on-github/about-releases):
  up to 1,000 files per release, each under 2 GiB; documentation lists no total
  release-size or bandwidth limit. Use for versioned project distributions and
  follow provider terms; this is not a guarantee of unrestricted object storage.
- [GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/github-pages-limits):
  free for public repositories, at most 1 GB published site, soft bandwidth limit
  100 GB/month. A free community catalog can be static. Pages does not permit
  ecommerce primarily facilitating commercial transactions. A paid marketplace
  needs a different hosting review. The portal uses the existing Ignis site;
  this catalog repository does not create another Pages site.
- [GitHub repository limits](https://docs.github.com/en/repositories/creating-and-managing-repositories/repository-limits):
  single Git object recommended <=1 MB, enforced at 100 MB; large generated
  payloads belong outside Git. Our validator deliberately limits local asset
  files to 1 MiB each and 256 MiB total: project policy, not provider quotas.
- [Git LFS](https://docs.github.com/en/billing/concepts/product-billing/git-lfs):
  GitHub Free includes 10 GiB storage and 10 GiB download bandwidth. Downloads and
  full revised versions consume the owner's allowance. No LFS is configured here
  and no account billing settings were changed.
- [Hugging Face](https://huggingface.co/docs/hub/storage-limits): free public
  storage is best-effort with community-value/dataset requirements. It is not a
  guaranteed free generic multi-terabyte CDN. Consider only for appropriate
  datasets with provider acceptance; not a launch dependency.
- [Cloudflare R2](https://developers.cloudflare.com/r2/pricing/): 10 GB-month free
  storage plus operation allowances; excess storage/operations are billable even
  with free egress. It is not our unconditional zero-budget default.

## Federation and durability

Listing and hosting are independent. Authors can publish source/downloads in
their own release repository; our index stores discovery and integrity metadata.
Use pinned version URLs, not mutable `latest` URLs. Mirrors serve identical bytes.
Changed payloads require a new asset version/hash and contributor review.

Offline validation checks URL structure and declared integrity, not remote
availability. No downloads, archive extraction, executable hooks, upload or paid
enrollment happen in the CLI. A future installer must enforce size/hash limits,
validate redirects and archive paths, preserve attribution and import atomically.
Hashes establish integrity, not publisher trust or safety.

At larger scale, prefer author-hosted releases, reduce derivatives, seek approved
open-source grants/sponsorship or pause central uploads. Do not evade provider
limits through chains of storage-only repositories.
