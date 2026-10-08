# Constraints

The source of truth for the live website is this GitHub repository. Edit public/index.html and let Cloudflare Workers Builds deploy main automatically. Keep the current design/content unless the user requests changes. The separate private johantaute/website repository holds the future Astro app.

Keep Cloudflare on Workers Free. Do not enable paid plans, overages, metered storage/AI, or purchased features. Do not add duplicate GitHub Actions deployment workflows. Only public files belong in public/; never publish repository root, credentials, or private vault content.

Run python3 scripts/build.py before deployment changes. Keep generated CSP hashes automatic and preserve required fonts/contact-form resources. Do not submit contact-form messages during verification. Pin Wrangler versions and review updates. Preserve production branch deployment and branch previews.
