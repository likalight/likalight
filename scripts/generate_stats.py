#!/usr/bin/env python3
"""Draw the profile's data graphics from the GitHub GraphQL API.

Standard library only -- urllib for the API -- so there is nothing to break
in CI. Fonts come from the pre-subsetted base64 files in assets/fonts/.

Outputs stats.svg, streak.svg, langs.svg and year.svg next to the README.

    GITHUB_TOKEN=... GH_LOGIN=likalight python3 scripts/generate_stats.py

Two things here exist purely for determinism, because without them the
nightly job commits a meaningless diff every single night:

  1. The contribution window is pinned to whole UTC days. Left alone,
     contributionsCollection measures "the past year" from the moment of
     the request, so two runs minutes apart bucket days into different
     weeks and shift the sparkline by a fraction of a pixel.
  2. Repositories are filtered to public only. A personal token sees
     private repos and the workflow's token does not, so without the
     filter the language percentages disagree depending on who ran it.
"""
import bisect
import datetime as dt
import json
import os
import urllib.error
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FONT_DIR = os.path.join(ROOT, "assets", "fonts")

RAMP = " .`:-=+*cs#%@"          # the portrait's own ramp, reused for the year
API = "https://api.github.com/graphql"

# ---------------------------------------------------------------- palette

CSS = (
    ".f{font-family:'JBM',ui-monospace,SFMono-Regular,Menlo,Consolas,monospace}"
    ".ink{fill:#1f2328}.mut{fill:#656d76}.dim{fill:#8c959f}.acc{fill:#0969da}"
    ".card{fill:none;stroke:#d8dee4}.rule{stroke:#d8dee4}.accs{stroke:#0969da}"
    ".bar{fill:#0969da}.barq{fill:#cfe2f8}"
    "@media(prefers-color-scheme:dark){"
    ".ink{fill:#e6edf3}.mut{fill:#8b949e}.dim{fill:#6e7681}.acc{fill:#58a6ff}"
    ".card{stroke:#2a3138}.rule{stroke:#2a3138}.accs{stroke:#58a6ff}"
    ".bar{fill:#58a6ff}.barq{fill:#173a5e}}"
)

QUERY = """
query($login:String!,$from:DateTime!,$to:DateTime!){
  user(login:$login){
    contributionsCollection(from:$from,to:$to){
      contributionCalendar{
        totalContributions
        weeks{contributionDays{date contributionCount}}
      }
    }
    repositories(first:100,privacy:PUBLIC,ownerAffiliations:OWNER,
                 isFork:false,orderBy:{field:PUSHED_AT,direction:DESC}){
      totalCount
      nodes{
        name
        stargazerCount
        primaryLanguage{name}
        languages(first:12,orderBy:{field:SIZE,direction:DESC}){
          edges{size node{name}}
        }
      }
    }
  }
}
"""

# ------------------------------------------------------------------ data


def fetch(login, token):
    """One request, over a window pinned to whole UTC days."""
    today = dt.datetime.now(dt.timezone.utc).date()
    start = today - dt.timedelta(days=364)
    variables = {
        "login": login,
        "from": start.isoformat() + "T00:00:00Z",
        "to": today.isoformat() + "T23:59:59Z",
    }
    body = json.dumps({"query": QUERY, "variables": variables}).encode()
    req = urllib.request.Request(
        API,
        data=body,
        headers={
            "Authorization": "bearer " + token,
            "Content-Type": "application/json",
            "User-Agent": "profile-self-generator",
        },
    )
    with urllib.request.urlopen(req, timeout=45) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        raise SystemExit("GraphQL: " + json.dumps(payload["errors"]))
    return payload["data"]["user"]


def days_of(user):
    """Flat [(date, count)] across the whole calendar, oldest first."""
    weeks = user["contributionsCollection"]["contributionCalendar"]["weeks"]
    out = []
    for week in weeks:
        for day in week["contributionDays"]:
            out.append((dt.date.fromisoformat(day["date"]), day["contributionCount"]))
    return out


def run_lengths(days):
    """(length, (start, end)) for every unbroken run of active days."""
    runs, start, count = [], None, 0
    for date, hits in days:
        if hits:
            count += 1
            start = start or date
            last = date
        elif count:
            runs.append((count, (start, last)))
            start, count = None, 0
    if count:
        runs.append((count, (start, last)))
    return runs


def streaks(days):
    """(current, current_span, longest, longest_span) over the window.

    Today is allowed to be empty without breaking the current streak --
    the day is not over yet -- but it is not counted either.
    """
    runs = run_lengths(days)
    longest, longest_span = max(runs, default=(0, None))
    tail = days[:-1] if days and days[-1][1] == 0 else days
    current, current_span = 0, None
    if tail and tail[-1][1]:
        current, current_span = run_lengths(tail)[-1]
    return current, current_span, longest, longest_span


def languages(user):
    """(by_bytes, by_repo_count), each a sorted [(name, value)] list."""
    by_bytes, by_repo = {}, {}
    for repo in user["repositories"]["nodes"]:
        for edge in repo["languages"]["edges"]:
            name = edge["node"]["name"]
            by_bytes[name] = by_bytes.get(name, 0) + edge["size"]
        primary = repo.get("primaryLanguage")
        if primary:
            by_repo[primary["name"]] = by_repo.get(primary["name"], 0) + 1
    rank = lambda table: sorted(table.items(), key=lambda kv: (-kv[1], kv[0]))
    return rank(by_bytes), rank(by_repo)


# ------------------------------------------------------------------ draw


def fonts(*names):
    """@font-face blocks for the given subsets, inlined as data URIs.

    An external font URL cannot work: these SVGs load through an <img> tag
    and browsers refuse subresource fetches for image documents.
    """
    weights = {"mono-regular": 400, "mono-bold": 700, "ramp": 400}
    css = ""
    for name in names:
        with open(os.path.join(FONT_DIR, name + ".b64"), encoding="ascii") as handle:
            b64 = handle.read().strip()
        css += (
            "@font-face{font-family:'JBM';font-style:normal;font-weight:%d;"
            "src:url(data:font/woff2;base64,%s) format('woff2')}"
            % (weights[name], b64)
        )
    return css


def esc(value):
    return str(value).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")


def head(width, height, title):
    return [
        '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
        'viewBox="0 0 %d %d" role="img" aria-label="%s">'
        % (width, height, width, height, esc(title)),
        "<style>%s%s</style>" % (fonts("mono-regular", "mono-bold"), CSS),
    ]


def text(x, y, body, cls="ink", size=13, weight=400, anchor="start", extra=""):
    return (
        '<text class="f %s" x="%s" y="%s" font-size="%s" font-weight="%d" '
        'text-anchor="%s"%s xml:space="preserve">%s</text>'
        % (cls, x, y, size, weight, anchor, extra, esc(body))
    )


def card(width, height, label):
    """Outer frame plus the small lowercase label every card carries."""
    return [
        '<rect class="card" x="0.5" y="0.5" width="%.1f" height="%.1f" rx="6"/>'
        % (width - 1, height - 1),
        text(18, 26, label, "dim", 11),
    ]


def commas(number):
    return "{:,}".format(number)


def write(path, parts):
    parts.append("</svg>")
    full = os.path.join(ROOT, path)
    with open(full, "w", encoding="utf-8") as handle:
        handle.write("".join(parts))
    print("wrote %-11s %5.1f KB" % (path, os.path.getsize(full) / 1024.0))


# ------------------------------------------------------------- the cards


def draw_stats(user, days):
    """Hero total, plus a weekly sparkline.

    Weekly, not daily: a line through daily counts claims values that never
    existed. Aggregated to weeks, the continuity is defensible.
    """
    width, height = 434, 190
    total = user["contributionsCollection"]["contributionCalendar"]["totalContributions"]
    repos = user["repositories"]["totalCount"]
    stars = sum(repo["stargazerCount"] for repo in user["repositories"]["nodes"])

    parts = head(width, height, "%s contributions in the last year" % total)
    parts += card(width, height, "contributions / 365 days")
    parts.append(text(18, 76, commas(total), "ink", 42, 700))
    parts.append(text(18, 98, "%d public repos, %d stars earned" % (repos, stars), "mut", 11))

    weekly = [sum(count for _, count in days[i:i + 7]) for i in range(0, len(days), 7)]
    left, top, plot_w, plot_h = 18, 118, width - 36, 46
    peak = max(weekly) or 1
    step = plot_w / float(max(len(weekly) - 1, 1))
    points = [
        (left + i * step, top + plot_h - (value / float(peak)) * plot_h)
        for i, value in enumerate(weekly)
    ]
    line = " ".join("%.1f,%.1f" % point for point in points)
    parts.append('<polygon class="barq" points="%.1f,%.1f %s %.1f,%.1f"/>'
                 % (left, top + plot_h, line, left + plot_w, top + plot_h))
    parts.append('<polyline class="accs" fill="none" stroke-width="1.6" '
                 'stroke-linejoin="round" points="%s"/>' % line)
    parts.append('<line class="rule" x1="%d" y1="%.1f" x2="%d" y2="%.1f"/>'
                 % (left, top + plot_h + 0.5, left + plot_w, top + plot_h + 0.5))
    parts.append(text(left, height - 14, "52 weeks ago", "dim", 10))
    parts.append(text(left + plot_w, height - 14, "peak %d a week" % peak, "dim", 10,
                      anchor="end"))
    write("stats.svg", parts)


def draw_streak(days):
    width, height = 434, 190
    current, current_span, longest, longest_span = streaks(days)

    def span(pair):
        if not pair:
            return "nothing running right now"
        return "%s - %s" % (pair[0].strftime("%d %b %Y"), pair[1].strftime("%d %b %Y"))

    parts = head(width, height, "current streak %d days, longest %d days" % (current, longest))
    parts += card(width, height, "streaks")
    for row, (label, value, pair) in enumerate(
        [("current", current, current_span), ("longest", longest, longest_span)]
    ):
        y = 84 + row * 60
        parts.append(text(18, y, str(value), "ink", 34, 700))
        parts.append(text(18 + 21 * len(str(value)) + 6, y,
                          "day" if value == 1 else "days", "mut", 12))
        parts.append(text(width - 18, y - 16, label, "dim", 11, anchor="end"))
        parts.append(text(width - 18, y, span(pair), "mut", 11, anchor="end"))
    parts.append('<line class="rule" x1="18" y1="112.5" x2="%d" y2="112.5"/>' % (width - 18))
    parts.append(text(18, height - 14, "measured over the same 365-day window", "dim", 10))
    write("streak.svg", parts)


def draw_langs(by_bytes, by_repo):
    width, height = 890, 210
    parts = head(width, height, "top languages across public repositories")
    parts += card(width, height, "languages / public repositories only")

    total = sum(value for _, value in by_bytes) or 1
    top = by_bytes[:6]
    left, bar_y, span_w = 18, 44, width - 36
    x = float(left)
    for i, (_, size) in enumerate(top):
        segment = span_w * size / float(total)
        parts.append('<rect class="bar" x="%.1f" y="%d" width="%.1f" height="8" '
                     'opacity="%.2f"/>' % (x, bar_y, max(segment - 2, 1), 1 - i * 0.13))
        x += segment
    if x < left + span_w:
        parts.append('<rect class="barq" x="%.1f" y="%d" width="%.1f" height="8"/>'
                     % (x, bar_y, left + span_w - x))

    column = span_w / 6.0
    for i, (name, size) in enumerate(top):
        cx = left + i * column
        parts.append('<rect class="bar" x="%.1f" y="72" width="8" height="8" '
                     'opacity="%.2f"/>' % (cx, 1 - i * 0.13))
        parts.append(text(cx + 14, 80, name, "ink", 12))
        parts.append(text(cx + 14, 98, "%.1f%%, %s KB" % (100.0 * size / total,
                                                          commas(size // 1024)), "mut", 11))

    parts.append('<line class="rule" x1="18" y1="126.5" x2="%d" y2="126.5"/>' % (width - 18))
    parts.append(text(18, 150, "by repository count", "dim", 11))
    ranked = by_repo[:8]
    peak = max([value for _, value in ranked] or [1])
    column = span_w / 8.0
    for i, (name, count) in enumerate(ranked):
        cx = left + i * column
        parts.append('<rect class="barq" x="%.1f" y="170" width="%.1f" height="6"/>'
                     % (cx, column - 16))
        parts.append('<rect class="bar" x="%.1f" y="170" width="%.1f" height="6"/>'
                     % (cx, (column - 16) * count / float(peak)))
        parts.append(text(cx, 192, "%s  %d" % (name, count), "mut", 11))
    write("langs.svg", parts)


def draw_year(days):
    """One character per day, on the portrait's ramp.

    Density is ranked against the year's own non-zero days, so the scale
    adapts instead of clipping a busy month flat against @.
    """
    char_w, line_h, size = 13.4, 16.0, 15.5
    pad_l, pad_t = 40, 58
    weeks = (len(days) + 6) // 7 + 1
    width = int(pad_l + weeks * char_w + 18)
    height = int(pad_t + 7 * line_h + 46)

    nonzero = sorted(count for _, count in days if count)

    def glyph(count):
        if not count:
            return RAMP[0]
        rank = bisect.bisect_left(nonzero, count) / float(max(len(nonzero) - 1, 1))
        return RAMP[1 + min(int(rank * (len(RAMP) - 1)), len(RAMP) - 2)]

    parts = head(width, height, "a year of contributions, one character per day")
    parts.append("<style>%s</style>" % fonts("ramp"))
    parts += card(width, height, "the year, one character per day")

    grid = [[" "] * weeks for _ in range(7)]
    lead = (days[0][0].weekday() + 1) % 7            # calendar weeks start Sunday
    months = {}
    for i, (date, count) in enumerate(days):
        cell = lead + i
        row, col = cell % 7, cell // 7
        if col < weeks:
            grid[row][col] = glyph(count)
            if date.day <= 7 and col < weeks - 2:
                months.setdefault(date.strftime("%b").lower(), col)

    for label, col in months.items():
        parts.append(text(pad_l + col * char_w, pad_t - 14, label, "dim", 10))
    spacing = ' letter-spacing="%.2f"' % (char_w - size * 0.6)
    for row, label in enumerate(["", "mon", "", "wed", "", "fri", ""]):
        y = pad_t + row * line_h + 12
        if label:
            parts.append(text(pad_l - 8, y, label, "dim", 10, anchor="end"))
        parts.append(text(pad_l, y, "".join(grid[row]), "acc", size, extra=spacing))

    baseline = int(pad_t + 7 * line_h + 26)
    parts.append(text(pad_l, baseline, "less", "dim", 10))
    parts.append(text(pad_l + 32, baseline, RAMP[1:], "mut", 13, extra=' letter-spacing="1.8"'))
    parts.append(text(pad_l + 32 + 138, baseline, "more", "dim", 10))
    parts.append(text(width - 18, baseline,
                      "%s contributions" % commas(sum(count for _, count in days)),
                      "dim", 10, anchor="end"))
    write("year.svg", parts)


def main():
    token = os.environ.get("GITHUB_TOKEN")
    login = os.environ.get("GH_LOGIN")
    if not token or not login:
        raise SystemExit("set GITHUB_TOKEN and GH_LOGIN")
    user = fetch(login, token)
    days = days_of(user)
    by_bytes, by_repo = languages(user)
    draw_stats(user, days)
    draw_streak(days)
    draw_langs(by_bytes, by_repo)
    draw_year(days)


if __name__ == "__main__":
    main()
