"""Generate animated cyber-themed project cards for the profile README."""
from pathlib import Path

OUT = Path(__file__).resolve().parent.parent / "assets" / "cards"
OUT.mkdir(parents=True, exist_ok=True)

W, H = 600, 330
FONT = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
BG = "#0a0e14"
TXT = "#e6edf3"
DIM = "#8b949e"


def esc(t):
    return t.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def chips(items, color, y):
    out, x = [], 28
    for it in items:
        w = 14 + len(it) * 7.6
        out.append(
            f'<g transform="translate({x:.0f} {y})"><rect width="{w:.0f}" height="24" rx="5" fill="{color}" fill-opacity=".08" stroke="{color}" stroke-opacity=".55"/>'
            f'<text x="{w/2:.0f}" y="16.5" text-anchor="middle" font-size="12" fill="{color}">{esc(it)}</text></g>'
        )
        x += w + 8
    return "\n".join(out)


def card(slug, accent, accent2, tag, title, bullets, stack, art, label):
    bl = []
    for i, b in enumerate(bullets):
        y = 150 + i * 30
        bl.append(
            f'<g class="row" style="animation-delay:{0.25 + 0.18*i:.2f}s"><text x="28" y="{y}" font-size="13.5" fill="{accent}">▸</text>'
            f'<text x="46" y="{y}" font-size="13.5" fill="{TXT}">{esc(b)}</text></g>'
        )
    svg = f"""<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" aria-label="{esc(label)}">
  <defs>
    <linearGradient id="bg" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#070b11"/><stop offset="1" stop-color="{BG}"/></linearGradient>
    <linearGradient id="edge" x1="0" x2="1"><stop offset="0" stop-color="{accent}"/><stop offset="1" stop-color="{accent2}"/></linearGradient>
    <pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse"><path d="M24 0H0V24" fill="none" stroke="{accent}" stroke-opacity=".06"/></pattern>
    <filter id="glow" x="-30%" y="-30%" width="160%" height="160%"><feGaussianBlur stdDeviation="2.4" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>
    <clipPath id="clip"><rect width="{W}" height="{H}" rx="14"/></clipPath>
  </defs>
  <style>
    text {{ font-family: {FONT}; }}
    .row {{ animation: in .6s ease-out backwards; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-10px) }} to {{ opacity: 1; transform: none }} }}
    .blink {{ animation: blink 1.2s steps(1) infinite; }} @keyframes blink {{ 50% {{ opacity: 0 }} }}
    .spin {{ animation: spin 10s linear infinite; transform-box: fill-box; transform-origin: center; }} @keyframes spin {{ to {{ transform: rotate(360deg) }} }}
  </style>
  <g clip-path="url(#clip)">
    <rect width="{W}" height="{H}" fill="url(#bg)"/>
    <rect width="{W}" height="{H}" fill="url(#grid)"/>
    <rect width="{W}" height="3" fill="url(#edge)"/>
    <rect y="3" width="{W}" height="60" fill="url(#edge)" opacity=".05"/>
    {art}
    <circle class="blink" cx="34" cy="38" r="5" fill="{accent}"/>
    <text x="48" y="43" font-size="12" fill="{accent}" letter-spacing="1.5">{esc(tag)}</text>
    <text x="28" y="100" font-size="24" font-weight="700" fill="{TXT}" filter="url(#glow)">{esc(title)}</text>
    <rect x="28" y="112" width="64" height="2.5" fill="url(#edge)"/>
    {chr(10).join(bl)}
    {chips(stack, accent2, 284)}
  </g>
  <rect x="1" y="1" width="{W-2}" height="{H-2}" rx="13" fill="none" stroke="url(#edge)" stroke-opacity=".6"/>
</svg>
"""
    (OUT / f"{slug}.svg").write_text(svg)


# ── art: face scan (election) ─────────────────────────────────────────
NEON, CYAN, PINK, AMBER, VIOLET = "#00ff9c", "#00e5ff", "#ff2e88", "#ffd166", "#b388ff"

face_pts = [(0, -52), (-30, -40), (30, -40), (-42, -10), (42, -10), (-40, 22), (40, 22), (-24, 48), (24, 48), (0, 58),
            (-18, -14), (18, -14), (0, 6), (-14, 28), (14, 28), (0, 30)]
edges = [(0, 1), (0, 2), (1, 3), (2, 4), (3, 5), (4, 6), (5, 7), (6, 8), (7, 9), (8, 9), (10, 12), (11, 12), (12, 15),
         (13, 15), (14, 15), (10, 1), (11, 2), (13, 7), (14, 8), (10, 3), (11, 4)]
cx, cy = 516, 150
mesh = "".join(
    f'<line x1="{cx+face_pts[a][0]}" y1="{cy+face_pts[a][1]}" x2="{cx+face_pts[b][0]}" y2="{cy+face_pts[b][1]}"/>' for a, b in edges)
dots = "".join(
    f'<circle cx="{cx+x}" cy="{cy+y}" r="2.6"><animate attributeName="opacity" values=".3;1;.3" dur="2s" begin="{i*0.12:.2f}s" repeatCount="indefinite"/></circle>'
    for i, (x, y) in enumerate(face_pts))
face_art = f"""
    <g opacity=".95">
      <ellipse cx="{cx}" cy="{cy+2}" rx="54" ry="68" fill="none" stroke="{CYAN}" stroke-opacity=".35" stroke-dasharray="3 5"/>
      <g stroke="{NEON}" stroke-opacity=".45" stroke-width="1">{mesh}</g>
      <g fill="{NEON}">{dots}</g>
      <g stroke="{CYAN}" stroke-width="2.5" fill="none">
        <path d="M{cx-66} {cy-58}v-18h18"/><path d="M{cx+66} {cy-58}v-18h-18"/><path d="M{cx-66} {cy+62}v18h18"/><path d="M{cx+66} {cy+62}v18h-18"/>
      </g>
      <rect x="{cx-64}" y="{cy-76}" width="128" height="3" fill="{NEON}" filter="url(#glow)">
        <animate attributeName="y" values="{cy-76};{cy+78};{cy-76}" dur="3s" repeatCount="indefinite"/>
      </rect>
      <g font-size="11">
        <rect x="{cx-62}" y="{cy+92}" width="124" height="22" rx="4" fill="{NEON}" fill-opacity=".1" stroke="{NEON}" stroke-opacity=".6"/>
        <text x="{cx}" y="{cy+107}" text-anchor="middle" fill="{NEON}">
          <tspan>LIVENESS ✓ · MATCH ✓</tspan>
          <animate attributeName="opacity" values="0;0;1;1" keyTimes="0;.45;.5;1" dur="3s" repeatCount="indefinite"/>
        </text>
        <text x="{cx}" y="{cy+107}" text-anchor="middle" fill="{CYAN}">
          <tspan>SCANNING…</tspan>
          <animate attributeName="opacity" values="1;1;0;0" keyTimes="0;.45;.5;1" dur="3s" repeatCount="indefinite"/>
        </text>
      </g>
    </g>"""

# ── art: CCTV tracker (SIH) ───────────────────────────────────────────
fx, fy, fw, fh = 420, 76, 158, 118
cctv_art = f"""
    <g>
      <rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="6" fill="#050809" stroke="{PINK}" stroke-opacity=".6"/>
      <g stroke="{PINK}" stroke-opacity=".12">{''.join(f'<line x1="{fx}" y1="{fy+i*6}" x2="{fx+fw}" y2="{fy+i*6}"/>' for i in range(1, fh//6))}</g>
      <circle class="blink" cx="{fx+14}" cy="{fy+14}" r="4.5" fill="#ff3b3b"/>
      <text x="{fx+24}" y="{fy+18}" font-size="10" fill="#ff6b6b">REC · CAM-03</text>
      <text x="{fx+fw-8}" y="{fy+fh-8}" font-size="9" fill="{DIM}" text-anchor="end">DHAV · carved</text>
      <g>
        <animateTransform attributeName="transform" type="translate" values="0 0;60 8;90 -6;30 4;0 0" dur="6s" repeatCount="indefinite"/>
        <circle cx="{fx+34}" cy="{fy+56}" r="11" fill="{DIM}" fill-opacity=".45"/>
        <path d="M{fx+18} {fy+96} q16 -26 32 0" fill="{DIM}" fill-opacity=".35"/>
        <rect x="{fx+19}" y="{fy+40}" width="30" height="32" fill="none" stroke="{NEON}" stroke-width="2"/>
        <text x="{fx+19}" y="{fy+36}" font-size="9" fill="{NEON}">face</text>
      </g>
      <g font-size="10" fill="{CYAN}" opacity=".85">
        <text x="{fx}" y="{fy+fh+22}">0x3F2A00  00 00 01 BA 44 00</text>
        <text x="{fx}" y="{fy+fh+36}">0x3F2A10  44 48 41 56 fd 1c</text>
        <rect x="{fx+62}" y="{fy+fh+12}" width="92" height="13" fill="{CYAN}" fill-opacity=".15">
          <animate attributeName="y" values="{fy+fh+12};{fy+fh+26};{fy+fh+12}" dur="2.4s" repeatCount="indefinite"/>
        </rect>
      </g>
      <text x="{fx}" y="{fy+fh+56}" font-size="10" fill="{PINK}">SHA-256 ✓  chain-of-custody ✓</text>
    </g>"""

# ── art: risk gauge (VaultCore) ───────────────────────────────────────
gx, gy, r = 500, 175, 74
gauge_art = f"""
    <g>
      <path d="M{gx-r} {gy} A{r} {r} 0 0 1 {gx-r*0.31:.1f} {gy-r*0.95:.1f}" fill="none" stroke="{NEON}" stroke-width="10"/>
      <path d="M{gx-r*0.31:.1f} {gy-r*0.95:.1f} A{r} {r} 0 0 1 {gx+r*0.31:.1f} {gy-r*0.95:.1f}" fill="none" stroke="{AMBER}" stroke-width="10"/>
      <path d="M{gx+r*0.31:.1f} {gy-r*0.95:.1f} A{r} {r} 0 0 1 {gx+r} {gy}" fill="none" stroke="{PINK}" stroke-width="10"/>
      <g font-size="9.5">
        <text x="{gx-r-4}" y="{gy+18}" fill="{NEON}">ALLOW</text>
        <text x="{gx}" y="{gy-r-14}" text-anchor="middle" fill="{AMBER}">2FA</text>
        <text x="{gx+r+4}" y="{gy+18}" text-anchor="end" fill="{PINK}">FREEZE</text>
      </g>
      <g>
        <line x1="{gx}" y1="{gy}" x2="{gx}" y2="{gy-r+14}" stroke="{TXT}" stroke-width="3" stroke-linecap="round"/>
        <animateTransform attributeName="transform" type="rotate" values="-70 {gx} {gy};-20 {gx} {gy};10 {gx} {gy};72 {gx} {gy};-70 {gx} {gy}" keyTimes="0;.3;.5;.75;1" dur="6s" repeatCount="indefinite"/>
      </g>
      <circle cx="{gx}" cy="{gy}" r="7" fill="{TXT}"/>
      <text x="{gx}" y="{gy+40}" text-anchor="middle" font-size="11" fill="{DIM}">ML risk score</text>
    </g>"""

# ── art: ECG pulse (hospital) ─────────────────────────────────────────
ecg = "M0 40 H40 L50 40 L56 30 L62 40 L70 40 L76 4 L84 74 L90 40 L100 40 L108 32 L118 40 H160"
pulse_art = f"""
    <g transform="translate(410 100)">
      <rect x="0" y="-12" width="170" height="100" rx="8" fill="#050809" stroke="{NEON}" stroke-opacity=".45"/>
      <clipPath id="ecgclip"><rect x="0" y="-12" width="170" height="100" rx="8"/></clipPath>
      <g clip-path="url(#ecgclip)">
        <g>
          <path d="{ecg}" transform="translate(5 0)" fill="none" stroke="{NEON}" stroke-width="2.4" filter="url(#glow)"/>
          <path d="{ecg}" transform="translate(165 0)" fill="none" stroke="{NEON}" stroke-width="2.4" filter="url(#glow)"/>
          <animateTransform attributeName="transform" type="translate" values="0 0;-160 0" dur="2.2s" repeatCount="indefinite"/>
        </g>
      </g>
      <text x="8" y="104" font-size="10" fill="{CYAN}">SOS · donors · 8 langs</text>
      <g transform="translate(118 116)">
        <path d="M14 0 L28 6 V18 C28 27 21 33 14 36 C7 33 0 27 0 18 V6 Z" fill="{NEON}" fill-opacity=".12" stroke="{NEON}" stroke-width="1.8"/>
        <path d="M8 18 l4 4 l8 -9" fill="none" stroke="{NEON}" stroke-width="2"/>
      </g>
      <text x="8" y="132" font-size="10" fill="{DIM}">zero-trust access</text>
    </g>"""

card("election", NEON, CYAN, "BIOMETRIC E-VOTING", "Secure College Election",
     ["ArcFace face recognition + passive liveness",
      "Anti-spoofing: rejects photos & replays",
      "Anonymous, hash-chained ballots",
      "One-time vote token · AI fraud alerts"],
     ["React", "FastAPI", "DeepFace", "PostgreSQL", "Redis"], face_art,
     "Secure College Election System — ArcFace face verification with passive liveness, hash-chained anonymous ballots")

card("sih", PINK, CYAN, "SIH 2026 · NTRO · SIH26150", "DVR/NVR Forensics",
     ["Recover deleted CCTV footage from disks",
      "AI face detection + search by photo",
      "Object & motion analytics · timelines",
      "Hashing, audit chain, court reports"],
     ["Python", "FastAPI", "OpenCV", "FFmpeg", "Docker"], cctv_art,
     "DVR/NVR Forensic Analysis Tool — deleted footage recovery, face detection and search, chain of custody")

card("vaultcore", AMBER, PINK, "FINTECH · FRAUD DETECTION", "VaultCore",
     ["Real-time ML risk score per withdrawal",
      "Allow · step-up 2FA · freeze account",
      "Device fingerprinting · AES-256",
      "Live WebSocket threat alerts"],
     ["Node.js", "scikit-learn", "PostgreSQL", "MongoDB"], gauge_art,
     "VaultCore — banking backend with real-time Isolation Forest fraud scoring")

card("hospital", CYAN, NEON, "HEALTHTECH · RURAL INDIA", "Hospital Management",
     ["AI prescription scanner",
      "SOS ambulance dispatch",
      "Blood-donor network · 8 languages",
      "JWT, lockout & zero-trust security"],
     ["React", "Express", "Prisma", "PostgreSQL", "FastAPI"], pulse_art,
     "Hospital Management System — AI prescription scanner, SOS dispatch, zero-trust security")

print("cards written to", OUT)
