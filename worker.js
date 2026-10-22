// Vorläufiger Zugang zur Seite im Aufbau (nur Hash im Code, kein Geheimnis im Repo).
// Ohne Anmeldung zeigt "/" den schlichten Platzhalter mit Login-Knopf; mit Cookie die echte Seite.
const PW_SHA256 = "9235b16e379f9f9263b9b0c9afc384d003183fd2ced9855f8bf01d390efe62f6";
const COOKIE = "bpb_zugang";
const OEFFENTLICH = new Set(["/", "/login", "/logout", "/platzhalter/platzhalter.css", "/favicon.svg", "/logo-dach.svg", "/logo-dach-atmend.svg", "/robots.txt"]);

async function sha256Hex(text) {
  const buf = await crypto.subtle.digest("SHA-256", new TextEncoder().encode(text));
  return [...new Uint8Array(buf)].map((b) => b.toString(16).padStart(2, "0")).join("");
}

function sameText(a, b) {
  if (a.length !== b.length) return false;
  let d = 0;
  for (let i = 0; i < a.length; i++) d |= a.charCodeAt(i) ^ b.charCodeAt(i);
  return d === 0;
}

function cookieValue(request, name) {
  const all = request.headers.get("Cookie") || "";
  for (const part of all.split(";")) {
    const i = part.indexOf("=");
    if (i > 0 && part.slice(0, i).trim() === name) return part.slice(i + 1).trim();
  }
  return "";
}

const HEADERS_SEITE = {
  "Content-Type": "text/html; charset=utf-8",
  "Cache-Control": "no-store",
  "X-Robots-Tag": "noindex, nofollow",
  "X-Content-Type-Options": "nosniff",
  "Referrer-Policy": "no-referrer",
  "Content-Security-Policy":
    "default-src 'none'; style-src 'self'; img-src 'self' data:; base-uri 'none'; form-action 'self'; frame-ancestors 'none'",
};

function loginSeite(fehler) {
  const meldung = fehler ? '<p class="fehler">Das Passwort stimmt nicht. Bitte noch einmal versuchen.</p>' : "";
  const html = `<!doctype html>
<html lang="de">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Login</title>
<meta name="robots" content="noindex, nofollow">
<meta name="theme-color" content="#1c1240">
<link rel="icon" href="/favicon.svg" type="image/svg+xml">
<link rel="stylesheet" href="/platzhalter/platzhalter.css">
</head>
<body>
<main>
  <picture><source media="(prefers-reduced-motion: reduce)" srcset="/logo-dach.svg"><img class="logo" src="/logo-dach-atmend.svg" alt="BPB" width="110" height="110"></picture>
  <h1>Login</h1>
  <form method="post" action="/login">
    <input id="pw" name="pw" type="password" placeholder="Passwort" autocomplete="current-password" autocapitalize="none" autocorrect="off" spellcheck="false" autofocus required>
    <button type="submit">Weiter</button>
  </form>
  ${meldung}
  <a class="zurueck" href="/">Zurück</a>
</main>
</body>
</html>`;
  return new Response(html, { status: fehler ? 401 : 200, headers: HEADERS_SEITE });
}

function umleiten(ziel, extra) {
  const h = new Headers({ Location: ziel, "Cache-Control": "no-store" });
  if (extra) h.append("Set-Cookie", extra);
  return new Response(null, { status: 303, headers: h });
}

export default {
  async fetch(request, env) {
    const url = new URL(request.url);
    const pfad = url.pathname;
    const token = await sha256Hex(PW_SHA256 + "|bpb-zugang");
    const drin = sameText(cookieValue(request, COOKIE), token);

    if (pfad === "/logout") {
      return umleiten("/", `${COOKIE}=; Path=/; Max-Age=0; HttpOnly; Secure; SameSite=Lax`);
    }

    if (pfad === "/login") {
      if (drin) return umleiten("/");
      if (request.method === "POST") {
        let pw = "";
        try {
          pw = String((await request.formData()).get("pw") || "").trim();
        } catch (e) {
          return loginSeite(true);
        }
        if (!sameText(await sha256Hex(pw), PW_SHA256)) return loginSeite(true);
        return umleiten("/", `${COOKIE}=${token}; Path=/; Max-Age=2592000; HttpOnly; Secure; SameSite=Lax`);
      }
      return loginSeite(false);
    }

    if (drin) {
      const res = await env.ASSETS.fetch(request);
      const out = new Response(res.body, res);
      out.headers.set("Cache-Control", "private, no-store");
      return out;
    }

    if (!OEFFENTLICH.has(pfad)) return umleiten("/");
    if (pfad === "/") {
      const res = await env.ASSETS.fetch(new Request(new URL("/platzhalter/", url), request));
      const out = new Response(res.body, res);
      out.headers.set("Cache-Control", "no-store");
      return out;
    }
    return env.ASSETS.fetch(request);
  },
};
