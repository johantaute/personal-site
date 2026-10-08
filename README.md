# Taute Group website

A static business website for Taute Group, a cybersecurity consultancy for South African small and medium businesses. The live project uses plain HTML and CSS and a Python standard-library build. No package installation is needed for local development.

## Source and preview

Edit the finished HTML pages in `public/` and shared styles in `public/assets/site.css`. Assets, favicon and social image are self-hosted. The palette uses navy, warm white and muted red. The homepage business-context diagram and Approach roadmap explain the service. An optional priority matrix on Approach is conceptual, not client data or statistics. Service fit and outputs stay visible, with further assessment and deliverable details in native expandable sections. A custom owl guides homepage visitors to Cyber Risk Discovery and accompanies enquiry invitations on the other business pages; see `ARTWORK.md` for provenance and the generation prompt. The public contact address is `contact@tautegroup.co.za`, supplied by the owner. Contact links open an email application; there is no form, submission backend or verified delivery claim.

Requires Python 3.9 or later:

```sh
python3 scripts/build.py
python3 scripts/check.py
python3 scripts/preview.py
```

Open http://127.0.0.1:4173. The server binds only to loopback. For another port use `python3 scripts/preview.py --port 4174`. `/__review` offers a 390px embedded viewport for mobile review. Use `/__review?page=/sample-report/` or `/__review?page=/contact/` to review those pages. This tool is served dynamically by the preview script and is never part of the published assets. Local preview permits same-origin framing for this tool and omits HTTPS-only headers; production headers retain frame blocking and HTTPS protections.

`dist/` is generated. Do not edit it. The builder copies only `public/`, rejects symlinks, hidden files and common credential extensions, and generates Cloudflare `_headers`. Public pages use no remote fonts, trackers or forms. Contact has one small inline clipboard helper, allowed by its generated SHA-256 CSP hash. It writes only the public email address, sends no network requests and shows success or failure feedback. The copy button is available when the browser supports clipboard writes in a secure context; email links and manual copying remain available. Keep private notes, GitBook exports, credentials and original personal content outside `public/`.

## Actual deployment configuration

Inspected 9 October 2026. Production is the existing Cloudflare Worker `personal-site`, connected through Workers Builds to GitHub `johantaute/personal-site`. The custom domain is `tautegroup.co.za`. The separate private `johantaute/website` repository contains the future Astro app and is not this live site.

The existing `wrangler.jsonc` is preserved: static assets from `./dist`, `not_found_handling: none`, `run_worker_first: false`, compatibility date `2026-10-09`, with workers.dev and preview URLs enabled. Cloudflare’s build configuration is managed in its dashboard, not by a GitHub Actions workflow.

| Setting | Production | Branch previews |
| --- | --- | --- |
| Root directory | `/` | `/` |
| Build command | `python3 scripts/build.py` | `python3 scripts/build.py` |
| Branches | `main` | All except `main` |
| Deploy command | `npx --yes wrangler@4.149.0 deploy` | `npx --yes wrangler@4.149.0 versions upload` |

Production and branch previews are automatic. Edit these source files in GitHub or github.dev; a commit or merge to `main` publishes production. Other branches automatically upload preview versions. Keep personal notes, original pages and local review archives out of the repository. No local checkout is required for ongoing edits.

This approved business website replaces the previous personal website. The preserved earlier commit remains available in Git history. For rollback, revert the relevant change in GitHub and let the same build publish the reverted source. Do not enable paid services when a free limit is reached.

After deployment, verify all five main routes, privacy, assets, contact links, security headers and mobile navigation on the custom domain. The old production commit `4578bb489505812e52db314b26ee5610dc811b05` is the inspected rollback reference; verify it against any subsequent work before using it.

Keep Workers Free and the existing free website plan. This redesign introduces no backend, database, paid service, subscription or new deployment workflow. Do not enable paid plans, overages or metered features. Review pinned Wrangler updates explicitly.

## Verification

`check.py` verifies each published page’s main landmark, single primary heading, metadata, image alternatives, internal links and anchors, and absence of forms, embedded frames and inline event handlers, with only the reviewed Contact clipboard helper permitted. Review keyboard focus, contrast and responsive rendering in the browser as well. Email delivery is not tested by sending messages.

The illustrative sample report is at `/sample-report/`, linked from Home and Services. Home has five native expandable FAQ answers. Contact shows the typical Discovery enquiry journey, with ongoing support optional.
