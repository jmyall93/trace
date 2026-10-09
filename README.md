# TRACE v2.2.3 — Cloudflare Workers deployment

This version converts the existing Cloudflare Pages Functions authentication backend into a Worker route handler while preserving the TRACE UI, D1 schema and industrial login background.

## Deploy using the EXISTING Cloudflare Worker `trace`
1. Extract the ZIP and upload **the contents of this folder** into the root of your existing GitHub repository `jmyall93/trace` (not an extra enclosing folder). Replace old `wrangler.toml`, `package.json` and `public` files.
2. In Cloudflare → Workers & Pages → trace → Settings → Build, set **Build command** to blank, **Deploy command** to `npx wrangler deploy`, and **Root directory** to `/`.
3. Keep the existing `DB` binding to `trace-db`. The `wrangler.toml` also declares it with your existing database ID. Do not recreate or re-run the migration.
4. Push the changes to `main`; Cloudflare's Git integration should build and deploy.
5. Enable the workers.dev URL under Domains if you want to test it publicly.
6. Test trial signup, logout, login, trial expiry and D1 records before inviting anyone.

## Notes
- Worker routes: `/api/auth/{trial,login,me,logout,forgot,reset}`; all other requests go to Worker Static Assets.
- `pages-functions-archive` is retained for reference and is not deployed as Pages Functions.
- Password reset emails require `RESEND_API_KEY` and `RESET_FROM_EMAIL` secrets/configuration.
- This is a preproduction candidate. Authentication needs rate limiting, email verification, audit logging and comprehensive security testing before public release.
- Existing dashboard/PLC integrations remain demo/local as in v2.1.1; this release fixes hosting architecture, not live OPC UA connectivity.
- Never commit API tokens or passwords into GitHub.

## v2.2.3 fixes
- PBKDF2 iteration count changed from 310,000 to 100,000 to meet the observed Cloudflare runtime limit.
- Removed 12-character minimum for trial registration and password reset. Nonempty passwords remain required; a 256-character abuse-prevention ceiling remains.
- Observability enabled in wrangler.toml for troubleshooting.
- No database migration is required. Existing password hashes made using a different iteration count would need a compatible verification path; earlier failed signups did not finish hashing.
- **Security:** relaxed password requirements are temporary and unsuitable for commercial launch; add rate limits, stronger credential policies, and complete security testing.

## TRACE Edge installation page update
- The OPC UA Connector menu now displays a customer-facing installer download and manufacturer selection guide.
- `/edge-release.json` is intentionally `unpublished`. No download is displayed until a compiled, tested Windows installer is available.
- To publish: upload a validated, signed Windows installer to an approved GitHub Release; compute its SHA-256; set `status` to `approved`, `version`, `download_url` (a direct github.com release asset URL), and `sha256` in `public/edge-release.json`; redeploy.
- This change does **not** build or install OPC UA software, add device drivers, enable live data, or modify cloud security. Browser downloads require user consent.
- Do not mark a release approved without Windows installation, uninstallation, OT read-only, and security validation.

### v2.2.5 release check UX
The Check for release control now shows a timestamped result on every click, an explicit unpublished status, and detailed fetch/metadata errors. A cache-busting asset version is applied to edge-ui.js. No installer is published by this change.
