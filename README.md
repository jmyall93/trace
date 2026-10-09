# TRACE v2.1.0 — GitHub + Cloudflare Pages + D1

This release packages the TRACE web UI for Cloudflare Pages with **D1-backed multi-company login**, username/password, a 14-day trial and email-based password resets (when Resend is configured).

## Deployment

1. Create a **private GitHub repository** and upload the contents of this folder to its root.
2. In Cloudflare, create a D1 database named `trace-db` (or run `npx wrangler d1 create trace-db`). Copy its UUID into `wrangler.toml` under `database_id`.
3. Run `npm install` and `npx wrangler d1 migrations apply trace-db --remote` from the project root, after authenticating Wrangler with your Cloudflare account.
4. Cloudflare **Workers & Pages → Create → Pages → Connect to Git**. Select the repository. Set framework preset to **None**, build command to **(empty)**, output directory to **public** and root to the repository root. Confirm the Pages project has the D1 binding `DB` pointing at `trace-db` (Settings → Bindings, if not automatically read from wrangler.toml). Redeploy after binding changes.
5. Configure password-reset email using a verified sender domain and the secrets `RESEND_API_KEY` and `RESET_FROM_EMAIL` in Cloudflare Pages project settings. Without these, **Forgot password does not send email**; the UI still gives a non-enumerating response.
6. Open the deployed URL and select **Start free trial**. Supply a new Company ID, username, work email and password (12+ characters). The first user becomes the workspace creator. No payment collection is implemented.

## Local testing

`npm install` then `npm run db:local` and `npm run dev`. Use Wrangler's local Pages environment for functions and D1. Opening `public/index.html` directly will not support login.

## Security and limitations

- Passwords are PBKDF2-SHA256 salted hashes; sessions use random HttpOnly Secure SameSite cookies stored hashed in D1. The D1 data model separates companies. Origin checking is included for POST requests.
- **Not production-audited.** Before accepting external users add abuse prevention/rate limits (Cloudflare WAF/Turnstile), email verification, role-based access, account recovery support, comprehensive tenant authorization for all future data APIs, and a security review.
- Trial expiration is enforced on login; a full subscription/billing lifecycle is not included. Existing sessions should also be restricted by trial status on every protected data endpoint when those endpoints are built.
- The original dashboard is **demo data**. It is not synchronized to D1, Fiix, Honeywell or a PLC. Existing simulation screens remain demonstrative only.
- **Cloudflare Pages cannot directly access a private on-prem OPC UA server.** The included OPC UA screen is an honest deployment notice. The separate local TRACE v2.0 Edge preview can be used for isolated engineering testing, but **it is not connected to this cloud app**. Never expose that preview's unsecured OPC UA or HTTP service to the public internet.
- Password reset requires Resend credentials and a verified sender domain. Microsoft SSO is not implemented and has been removed from the login screen.
- This package does not automatically create a GitHub repository, D1 database, or live Cloudflare deployment. Those require access to your accounts.

## Brand update
Login background replaced with a generic industrial mechanical facility visual, avoiding tunnel-specific imagery. Asset: `public/industrial-bg.webp`.
