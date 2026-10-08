# Johan Taute — live website

Production: https://tautegroup.co.za

## Edit and publish entirely in GitHub

1. Open [public/index.html](public/index.html) in GitHub and click Edit, or press `.` in the repository to use github.dev.
2. Commit to a branch when you want a preview. Cloudflare uploads a preview version automatically.
3. Commit or merge into `main` to publish production automatically. Cloudflare runs the build and deploys to the existing `personal-site` Worker.
4. Check the build result in [Cloudflare Workers Builds](https://dash.cloudflare.com/0c97a8906642dd94446718c2fa8377a2/workers/services/view/personal-site/production).

No local checkout, local server, GitHub Actions, or manually copied deployment files are needed.

## Deployment settings

- Repository: `johantaute/personal-site`
- Root directory: `/`
- Build command: `python3 scripts/build.py`
- Production deploy command: `npx --yes wrangler@4.149.0 deploy`
- Branch preview command: `npx --yes wrangler@4.149.0 versions upload`
- Assets directory: `dist/`
- Node version: `22.19.0` from `.node-version`
- Watched paths: `public/**`, `scripts/**`, `wrangler.jsonc`, `.node-version`

Only `public/` is copied into `dist/`. Repository documentation, deployment configuration, and tooling are never served as assets.

## Security and cost constraints

Cloudflare Workers Free was verified in the dashboard on 9 October 2026. The site serves static assets with no application Worker, paid storage, database, AI, or cron jobs. Keep that plan free; do not upgrade or enable paid add-ons. Free limits can block excess builds; do not upgrade automatically. Existing domain registration/renewal and third-party contact-form terms are separate.

The build regenerates CSP hashes for the inline JavaScript and adds anti-framing, MIME-sniffing protection, referrer restrictions, restricted browser permissions, and HTTPS security headers. Inline styles remain allowed to preserve the current design. The policy permits the existing Google Fonts, Web3Forms contact endpoint, and HTTPS Canarytokens image; review any future external resource before allowing it. It also rejects external script tags until their policy is explicitly reviewed.

The Web3Forms access key is a public form identifier, not a Cloudflare deployment token. Keep actual credentials in scoped Cloudflare secrets or deployment settings, never in this public repository. Account 2FA and GitHub branch protection must be managed in their respective account settings.

The separate [private Astro project](https://github.com/johantaute/website) is preserved for later development and does not replace this site. Private vault content must never be published as static assets.

For rollback, revert the relevant GitHub commit; Cloudflare redeploys the reverted files. Previous production deployments are also available in Cloudflare.
