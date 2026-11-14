#!/usr/bin/env python3
"""Montanha: Zero Day - 한국어판 빌드 스크립트.

원작 저장소(코드 MIT)에서 코드만 받아 오고, 원작 에셋(ARR: assets/, icons/,
docs/screenshots/, 이름·스토리)은 저장소에 복사하지 않는다.
에셋은 런타임에 원작 GitHub Pages 에서 직접 불러온다(js/assets.js 의 ASSET_BASE).

실행: python3 tools/ko_build.py   (저장소 루트에서)
"""
import os
import re
import subprocess
import sys
import urllib.request

UPSTREAM = os.environ.get("MZD_UPSTREAM", "https://github.com/tiagovilasboas/montanha-zero-day.git")
ASSET_BASE = os.environ.get("MZD_ASSET_BASE", "https://tiagovilasboas.github.io/montanha-zero-day/")
SRC = "/tmp/mzd-upstream"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

report = []
fails = []

KO_CSS = """
/* 한국어판: 외부 웹폰트(Google Fonts)를 쓰지 않고 시스템 한글 폰트로 표시합니다. */
html[lang="ko"] {
  --font-display: "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", "Noto Sans CJK KR", ui-monospace, monospace;
  --font-body: "Apple SD Gothic Neo", "Malgun Gothic", "Noto Sans KR", "Noto Sans CJK KR", system-ui, sans-serif;
}
"""


def log(msg):
    report.append(str(msg))
    print(msg)


def read(path):
    with open(os.path.join(ROOT, path), encoding="utf-8") as f:
        return f.read()


def write(path, text):
    full = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full), exist_ok=True)
    with open(full, "w", encoding="utf-8") as f:
        f.write(text)


def patch(path, name, pattern, repl, expect=1, required=True):
    src = read(path)
    out, n = re.subn(pattern, repl, src)
    status = "OK" if n == expect else "MISS(%d/%d)" % (n, expect)
    log("patch %-16s %-22s %s" % (path, name, status))
    if n != expect and required:
        fails.append("%s:%s" % (path, name))
    if n:
        write(path, out)
    return n


def clone():
    if not os.path.isdir(os.path.join(SRC, ".git")):
        subprocess.run(["git", "clone", "--depth", "1", UPSTREAM, SRC], check=True)
    out = subprocess.run(["git", "-C", SRC, "rev-parse", "HEAD"], capture_output=True, text=True)
    log("upstream commit: " + out.stdout.strip())


def copy_code():
    copied = 0
    for name in ("index.html", "css/style.css"):
        dst = os.path.join(ROOT, name)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        with open(os.path.join(SRC, name), "rb") as a, open(dst, "wb") as b:
            b.write(a.read())
        copied += 1
    jsdir = os.path.join(SRC, "js")
    for f in sorted(os.listdir(jsdir)):
        if not f.endswith(".js") or f == "i18n.ko.js":
            continue
        with open(os.path.join(jsdir, f), "rb") as a, open(os.path.join(ROOT, "js", f), "wb") as b:
            b.write(a.read())
        copied += 1
    log("copied upstream code files: %d" % copied)


def patch_assets():
    log("ASSET_BASE = " + ASSET_BASE)
    patch("js/assets.js", "asset-base",
          r"export const assetPath = name => `assets/\$\{name\}\.webp`;",
          "const ASSET_BASE = '%s'; // 원작 ARR 에셋: 재배포하지 않고 원작 Pages 에서 직접 불러온다.\n\n"
          "export const assetPath = name => `${ASSET_BASE}assets/${name}.webp`;" % ASSET_BASE)
    patch("js/assets.js", "anims-json",
          r"fetch\('assets/anims\.json'\)",
          "fetch(`${ASSET_BASE}assets/anims.json`)")


def patch_i18n():
    patch("js/i18n.js", "ko-import",
          r"\nconst STORAGE_KEY = 'mzd-lang';",
          "\nimport { KO } from './i18n.ko.js';\n\nconst STORAGE_KEY = 'mzd-lang';")
    patch("js/i18n.js", "ko-ui-table",
          r"\n\};\n\n// Narrative lines stay in Portuguese",
          "\n};\n\nUI.ko = KO.ui; // 한국어 사전 (js/i18n.ko.js). 원문 en/pt 는 그대로 둡니다.\n\n"
          "// Narrative lines stay in Portuguese")
    patch("js/i18n.js", "ko-lines-table",
          r"\n\};\n\nfunction browserIsPortuguese",
          "\n};\n\nconst LINES_KO = KO.lines; // 포르투갈어 원문 -> 한국어\n\nfunction browserIsPortuguese")
    patch("js/i18n.js", "browser-is-korean",
          r"\nfunction timezoneIsBrazil\(\)",
          "\nfunction browserIsKorean() {\n"
          "  const primary = (navigator.languages?.[0] || navigator.language || '').toLowerCase();\n"
          "  return primary === 'ko' || primary.startsWith('ko-');\n"
          "}\n\nfunction timezoneIsBrazil()")
    patch("js/i18n.js", "detect-saved",
          r"if \(saved === 'pt' \|\| saved === 'en'\) return saved;",
          "if (saved === 'pt' || saved === 'en' || saved === 'ko') return saved;")
    patch("js/i18n.js", "detect-korean",
          r"return timezoneIsBrazil\(\) && browserIsPortuguese\(\) \? 'pt' : 'en';",
          "if (browserIsKorean()) return 'ko'; // 브라우저 언어가 한국어면 기본 한국어\n"
          "  return timezoneIsBrazil() && browserIsPortuguese() ? 'pt' : 'en';")
    patch("js/i18n.js", "tr-korean",
          r"if \(!text \|\| current === 'pt'\) return text;\s*\n\s*return LINES\[text\] \?\? text;",
          "if (!text || current === 'pt') return text;\n"
          "  if (current === 'ko') return LINES_KO[text] ?? LINES[text] ?? text;\n"
          "  return LINES[text] ?? text;")
    patch("js/i18n.js", "dom-lang-ko",
          r"document\.documentElement\.lang = current === 'pt' \? 'pt-BR' : 'en';",
          "document.documentElement.lang = current === 'pt' ? 'pt-BR' : current === 'ko' ? 'ko' : 'en';")
    patch("js/i18n.js", "toggle-3-way",
          r"current = current === 'pt' \? 'en' : 'pt';",
          "current = current === 'en' ? 'ko' : current === 'ko' ? 'pt' : 'en';")
    patch("js/i18n.js", "lang-switch-label",
          r"langSwitch: 'Português',",
          "langSwitch: '\ud55c\uad6d\uc5b4',")


def patch_main():
    patch("js/main.js", "no-service-worker",
          r"navigator\.serviceWorker\.register\('sw\.js'\)[^\n]*",
          "// Korean build: offline PWA caching is off - art stays on the author's Pages.")


def patch_fonts():
    total = 0
    for name in sorted(os.listdir(os.path.join(ROOT, "js"))):
        if not name.endswith(".js"):
            continue
        path = "js/" + name
        src = read(path)
        out = src.replace('"Press Start 2P", monospace',
                          '"Press Start 2P", "Malgun Gothic", "Apple SD Gothic Neo", ui-monospace, monospace')
        out = out.replace('"VT323", monospace',
                          '"VT323", "Malgun Gothic", "Apple SD Gothic Neo", ui-monospace, monospace')
        if out != src:
            write(path, out)
            total += 1
    log("canvas font strings patched in files: %d" % total)
    patch("css/style.css", "font-display-ko",
          r'--font-display: "Press Start 2P", ui-monospace, monospace;',
          '--font-display: "Press Start 2P", ui-monospace, "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", monospace;')
    patch("css/style.css", "font-body-ko",
          r'--font-body: "VT323", ui-monospace, monospace;',
          '--font-body: "VT323", ui-monospace, "Malgun Gothic", "Apple SD Gothic Neo", "Noto Sans KR", monospace;')
    css = read("css/style.css")
    if 'html[lang="ko"]' not in css:
        write("css/style.css", css.rstrip() + "\n" + KO_CSS)
        log("patch css/style.css    ko-block                 OK")


def patch_index():
    patch("index.html", "drop-google-fonts",
          r'<link[^>]*(?:fonts\.googleapis\.com|fonts\.gstatic\.com)[^>]*>', "", expect=3, required=False)
    patch("index.html", "drop-manifest-link",
          r'<link[^>]*rel="manifest"[^>]*>', "", expect=1, required=False)
    patch("index.html", "drop-icon-links",
          r'<link[^>]*href="icons/[^"]*"[^>]*>', "", expect=1, required=False)


def check_assets():
    src = read("js/assets.js")
    names = re.findall(r"'([a-z0-9_]+)'", re.search(r"const NAMES = \[(.*?)\];", src, re.S).group(1))
    anims = ("hero_idle", "hero_run", "hero_jump", "hero_shoot",
             "gle_idle", "gle_run", "gle_jump", "gle_shoot")
    urls = [ASSET_BASE + "assets/%s.webp" % n for n in names]
    urls += [ASSET_BASE + "assets/anim_%s.webp" % n for n in anims]
    bad = []
    for u in urls:
        try:
            with urllib.request.urlopen(urllib.request.Request(u, method="HEAD"), timeout=30) as r:
                if r.status != 200:
                    bad.append("%s %s" % (r.status, u))
        except Exception as e:
            bad.append("%s %s" % (e, u))
    log("asset HEAD check: %d urls, %d problems %s" % (len(urls), len(bad), "; ".join(bad[:4])))


def check_cors():
    url = ASSET_BASE + "assets/anims.json"
    for origin in ("", "https://sigco3111.github.io"):
        headers = {"Origin": origin} if origin else {}
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers=headers), timeout=30) as r:
                log("CORS %s origin=%s -> %s acao=%s" % (
                    url, origin or "-", r.status, r.headers.get("access-control-allow-origin")))
        except Exception as e:
            log("CORS %s origin=%s -> ERROR %s" % (url, origin or "-", e))


def final_checks():
    for name in ("sw.js", "manifest.webmanifest", "build.py", "game.html"):
        log("absent as expected: %-20s %s" % (name, not os.path.exists(os.path.join(ROOT, name))))
    hits = []
    for path, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d != ".git"]
        for f in files:
            if f.endswith((".html", ".css", ".js")):
                p = os.path.join(path, f)
                s = open(p, encoding="utf-8", errors="ignore").read()
                for pat in ("fonts.googleapis.com", "fonts.gstatic.com", 'src="/', 'href="/', "url(/"):
                    if pat in s:
                        hits.append("%s: %s" % (os.path.relpath(p, ROOT), pat))
    log("external/root-absolute references: %d %s" % (len(hits), hits[:8]))
    local_assets = []
    for f in sorted(os.listdir(os.path.join(ROOT, "js"))):
        s = read("js/" + f)
        if re.search(r"['\"`]assets/", s):
            local_assets.append("js/" + f)
    log("hard-coded local asset paths left: %d %s" % (len(local_assets), local_assets[:5]))
    if os.path.isdir(os.path.join(ROOT, "assets")):
        log("WARNING: assets/ exists in repo - ARR assets must not be redistributed")


def main():
    clone()
    copy_code()
    patch_assets()
    patch_i18n()
    patch_main()
    patch_fonts()
    patch_index()
    check_assets()
    check_cors()
    final_checks()
    log("FAILED PATCHES: %d %s" % (len(fails), fails))
    write("docs/build-report.txt", "\n".join(report) + "\n")
    if fails:
        sys.exit(1)


if __name__ == "__main__":
    main()
