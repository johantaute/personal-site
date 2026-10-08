# Project instructions

The source of truth for the live website is GitHub `johantaute/personal-site`. Public business pages are finished static HTML in `public/`, with shared CSS and assets. The private `johantaute/website` repository contains a separate future Astro app. Keep personal notes and GitBook material separate.

Keep Cloudflare on Workers Free. Do not enable paid plans, overages, metered storage/AI or purchased features. Preserve the existing Workers Builds production and preview configuration; do not add duplicate GitHub Actions deployment workflows. Pin Wrangler versions and review updates.

Only publish `public/` through the generated `dist/`. Never publish repository root, credentials, private vault content or the archived personal page. Run `python3 scripts/build.py` and `python3 scripts/check.py` before deployment changes. Keep CSP generation in the builder and review any new resource requirements explicitly. Do not submit enquiry messages during verification.

The initial Taute Group redesign was approved for production by the owner on 9 October 2026. For future work, respect the owner’s requested review and publishing scope. Branch pushes publish Cloudflare previews; main publishes production.
