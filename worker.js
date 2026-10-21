// Vorläufiger Passwortschutz für die Vorschau (nur Hash im Code, kein Geheimnis im Repo).
// Benutzername beliebig, Passwort wird per Browser-Dialog (HTTP Basic) abgefragt.
const PW_SHA256 = "aac74112139fbfee8171defea41a8cc55fd31ae15c801061eb7a2d55fabf7cf2";

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

function denied() {
  return new Response("Diese Seite ist im Aufbau. Bitte Passwort eingeben.", {
    status: 401,
    headers: {
      "WWW-Authenticate": 'Basic realm="BPB Vorschau", charset="UTF-8"',
      "Content-Type": "text/plain; charset=utf-8",
      "Cache-Control": "no-store",
      "X-Robots-Tag": "noindex, nofollow",
    },
  });
}

export default {
  async fetch(request, env) {
    const auth = request.headers.get("Authorization") || "";
    if (!auth.startsWith("Basic ")) return denied();
    let pass = "";
    try {
      const raw = new TextDecoder().decode(Uint8Array.from(atob(auth.slice(6)), (c) => c.charCodeAt(0)));
      pass = raw.slice(raw.indexOf(":") + 1);
    } catch (e) {
      return denied();
    }
    if (!sameText(await sha256Hex(pass), PW_SHA256)) return denied();
    const res = await env.ASSETS.fetch(request);
    const out = new Response(res.body, res);
    out.headers.set("Cache-Control", "private, no-store");
    return out;
  },
};
