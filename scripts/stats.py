"""Generate cyber-themed stats and language SVG cards for the profile README.

Runs inside GitHub Actions with GITHUB_TOKEN; writes dist/stats.svg and dist/langs.svg.
"""
import json
import os
import urllib.request
from datetime import datetime, timezone

USER = os.environ.get("GH_USER", "BhanuPrasad-2006")
TOKEN = os.environ["GITHUB_TOKEN"]
OUT = os.environ.get("OUT_DIR", "dist")

QUERY = """
query($login: String!) {
  user(login: $login) {
    createdAt
    followers { totalCount }
    repositories(ownerAffiliations: OWNER, isFork: false, first: 100, privacy: PUBLIC) {
      totalCount
      nodes {
        stargazerCount
        languages(first: 10, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
    contributionsCollection {
      totalCommitContributions
      restrictedContributionsCount
      totalPullRequestContributions
      totalIssueContributions
      contributionCalendar { totalContributions }
    }
  }
}
"""


def gql():
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": {"login": USER}}).encode(),
        headers={"Authorization": f"bearer {TOKEN}", "Content-Type": "application/json"},
    )
    with urllib.request.urlopen(req) as r:
        data = json.load(r)
    if "errors" in data:
        raise SystemExit(data["errors"])
    return data["data"]["user"]


FONT = "'JetBrains Mono','Fira Code','Cascadia Code',Consolas,'Courier New',monospace"
NEON, CYAN, PINK, DIM, TXT, BG = "#00ff9c", "#00e5ff", "#ff2e88", "#8b949e", "#e6edf3", "#0a0e14"


def frame(w, h, title, body):
    return f"""<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}" role="img" aria-label="{title}">
  <style>
    text {{ font-family: {FONT}; }}
    .row {{ animation: in .6s ease-out backwards; }}
    @keyframes in {{ from {{ opacity: 0; transform: translateX(-8px) }} to {{ opacity: 1; transform: none }} }}
    .bar {{ transform-box: fill-box; transform-origin: left; animation: grow 1.1s ease-out backwards; }}
    @keyframes grow {{ from {{ transform: scaleX(0) }} to {{ transform: scaleX(1) }} }}
    .blink {{ animation: b 1s steps(1) infinite; }} @keyframes b {{ 50% {{ opacity: 0 }} }}
  </style>
  <rect x="1" y="1" width="{w-2}" height="{h-2}" rx="12" fill="{BG}" stroke="{NEON}" stroke-opacity=".35"/>
  <text x="24" y="36" fill="{NEON}" font-size="16" font-weight="700">{title}</text>
  <rect class="blink" x="{24 + len(title)*9.8 + 6}" y="23" width="8" height="16" fill="{NEON}"/>
  <line x1="24" y1="50" x2="{w-24}" y2="50" stroke="{NEON}" stroke-opacity=".2"/>
{body}
</svg>
"""


def stats_card(u):
    c = u["contributionsCollection"]
    stars = sum(n["stargazerCount"] for n in u["repositories"]["nodes"])
    commits = c["totalCommitContributions"] + c["restrictedContributionsCount"]
    rows = [
        ("[+]", "Commits (last year)", commits, NEON),
        ("[+]", "Total contributions", c["contributionCalendar"]["totalContributions"], NEON),
        ("[+]", "Pull requests", c["totalPullRequestContributions"], CYAN),
        ("[+]", "Issues", c["totalIssueContributions"], CYAN),
        ("[+]", "Public repositories", u["repositories"]["totalCount"], PINK),
        ("[+]", "Stars earned", stars, PINK),
    ]
    body = []
    for i, (tag, label, val, col) in enumerate(rows):
        y = 82 + i * 28
        body.append(
            f'  <g class="row" style="animation-delay:{0.15*i:.2f}s">'
            f'<text x="24" y="{y}" font-size="14" fill="{col}">{tag}</text>'
            f'<text x="60" y="{y}" font-size="14" fill="{TXT}">{label}</text>'
            f'<text x="{450-24}" y="{y}" font-size="14" fill="{col}" text-anchor="end" font-weight="700">{val}</text></g>'
        )
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body.append(f'  <text x="24" y="{82+len(rows)*28+4}" font-size="11" fill="{DIM}">last scan: {stamp}</text>')
    return frame(450, 82 + len(rows) * 28 + 22, "$ ./scan --stats", "\n".join(body))


def langs_card(u):
    totals = {}
    colors = {}
    for n in u["repositories"]["nodes"]:
        for e in n["languages"]["edges"]:
            name = e["node"]["name"]
            totals[name] = totals.get(name, 0) + e["size"]
            colors[name] = e["node"]["color"] or NEON
    top = sorted(totals.items(), key=lambda kv: -kv[1])[:6]
    s = sum(v for _, v in top) or 1
    body, bar_x, bar_w = [], 24, 402
    x = bar_x
    for i, (name, v) in enumerate(top):
        w = bar_w * v / s
        body.append(f'  <rect class="bar" style="animation-delay:{0.1*i:.2f}s" x="{x:.1f}" y="66" width="{max(w,1):.1f}" height="10" fill="{colors[name]}"/>')
        x += w
    for i, (name, v) in enumerate(top):
        col, row = i % 2, i // 2
        tx, ty = 24 + col * 210, 104 + row * 26
        body.append(
            f'  <g class="row" style="animation-delay:{0.12*i:.2f}s">'
            f'<circle cx="{tx+5}" cy="{ty-5}" r="5" fill="{colors[name]}"/>'
            f'<text x="{tx+16}" y="{ty}" font-size="13" fill="{TXT}">{name}</text>'
            f'<text x="{tx+190}" y="{ty}" font-size="13" fill="{DIM}" text-anchor="end">{100*v/s:.1f}%</text></g>'
        )
    y = 104 + ((len(top) + 1) // 2) * 26 + 8
    repos = u["repositories"]["totalCount"]
    body.append(f'  <text x="24" y="{y}" font-size="12" fill="{DIM}">scanned {repos} public repos · by bytes of code</text>')
    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    body.append(f'  <text x="24" y="{82+6*28+4}" font-size="11" fill="{DIM}">last scan: {stamp}</text>')
    return frame(450, 82 + 6 * 28 + 22, "$ cat languages.log", "\n".join(body))


if __name__ == "__main__":
    os.makedirs(OUT, exist_ok=True)
    u = gql()
    open(os.path.join(OUT, "stats.svg"), "w").write(stats_card(u))
    open(os.path.join(OUT, "langs.svg"), "w").write(langs_card(u))
    print("wrote stats.svg and langs.svg")
