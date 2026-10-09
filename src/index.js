import { handleAuth } from './auth.js';

export default {
  async fetch(request, env, ctx) {
    const url = new URL(request.url);
    if (url.pathname.startsWith('/api/auth/')) {
      const path = url.pathname.slice('/api/auth/'.length).split('/').filter(Boolean);
      return handleAuth({request, env, params:{path}});
    }
    if (url.pathname.startsWith('/api/')) {
      return new Response(JSON.stringify({error:'Not found'}), {
        status:404, headers:{'Content-Type':'application/json','Cache-Control':'no-store'}
      });
    }
    // Cloudflare Workers Static Assets serves the unchanged TRACE UI.
    return env.ASSETS.fetch(request);
  }
};
