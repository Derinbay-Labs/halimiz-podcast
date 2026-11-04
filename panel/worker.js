// Cloudflare Worker for panel.derinbay.com: HTTP Basic Auth in front of the static panel.
// Serves panel/ files from the public repo (raw.githubusercontent.com, master) so the panel
// is never published on halimiz.derinbay.com. Secrets: PANEL_USER, PANEL_PASSWORD.
// Deployed by hand from the Cloudflare dashboard (Workers & Pages → halimiz-panel).

const REPO = "Derinbay-Labs/halimiz-podcast";
const TYPES = { html: "text/html; charset=utf-8", js: "application/javascript; charset=utf-8",
                json: "application/json; charset=utf-8", css: "text/css; charset=utf-8",
                png: "image/png", jpg: "image/jpeg", svg: "image/svg+xml", txt: "text/plain; charset=utf-8" };

function unauthorized() {
  return new Response("Giriş gerekli.", { status: 401,
    headers: { "WWW-Authenticate": 'Basic realm="HAL\'imiz Panel", charset="UTF-8"', "Cache-Control": "no-store" } });
}

function safeEqual(a, b) {
  const enc = new TextEncoder();
  const x = enc.encode(a), y = enc.encode(b);
  if (x.length !== y.length) return false;
  let diff = 0;
  for (let i = 0; i < x.length; i++) diff |= x[i] ^ y[i];
  return diff === 0;
}

export default {
  async fetch(request, env) {
    const auth = request.headers.get("Authorization") || "";
    if (!auth.startsWith("Basic ")) return unauthorized();
    let user = "", pass = "";
    try {
      const decoded = atob(auth.slice(6));
      const i = decoded.indexOf(":");
      user = decoded.slice(0, i); pass = decoded.slice(i + 1);
    } catch { return unauthorized(); }
    if (!safeEqual(user, env.PANEL_USER || "") || !safeEqual(pass, env.PANEL_PASSWORD || "")) return unauthorized();

    const url = new URL(request.url);
    let path = url.pathname.replace(/^\/+/, "");
    if (path === "" || path.endsWith("/")) path += "index.html";
    if (path.includes("..")) return new Response("Not found", { status: 404 });
    const upstream = `https://raw.githubusercontent.com/${REPO}/master/panel/${path}`;
    const res = await fetch(upstream, { cf: { cacheTtl: 120, cacheEverything: true } });
    if (res.status === 404) return new Response("Not found", { status: 404 });
    const ext = path.split(".").pop().toLowerCase();
    return new Response(res.body, { status: res.status, headers: {
      "Content-Type": TYPES[ext] || "application/octet-stream",
      "Cache-Control": ext === "json" ? "no-cache" : "public, max-age=120",
      "X-Robots-Tag": "noindex, nofollow", "Referrer-Policy": "no-referrer" } });
  }
};
