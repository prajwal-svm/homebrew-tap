"""Moves the cask and the formula to FolderSkin's newest releases.

The cask follows the app's latest release (tags like v0.1.11) and the formula the command line's
newest release (tags like cli-v0.1.0). Each file changes only when its release is newer, and only
after the downloads are hashed, so a half-published release is never followed. Writes what it
moved to into .github/.bumped for the commit message.
"""
import hashlib
import json
import os
import re
import subprocess
import sys
import urllib.request

REPO = "prajwal-svm/folderskin"
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)


def gh(path):
    out = subprocess.run(["gh", "api", path], check=True, capture_output=True, text=True).stdout
    return json.loads(out)


def sha256_of(url):
    h = hashlib.sha256()
    with urllib.request.urlopen(url, timeout=600) as r:
        for chunk in iter(lambda: r.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def version_of(text):
    return re.search(r'^\s*version "([^"]+)"', text, re.M).group(1)


def as_tuple(v):
    return tuple(int(p) for p in re.findall(r"\d+", v))


moved = []

# The app: the cask.
cask_path = os.path.join(ROOT, "Casks", "folderskin.rb")
cask = open(cask_path).read()
latest = gh(f"repos/{REPO}/releases/latest")
app_version = latest["tag_name"].lstrip("v")
if as_tuple(app_version) > as_tuple(version_of(cask)):
    names = {a["name"] for a in latest["assets"]}
    dmg = f"FolderSkin_{app_version}_universal.dmg"
    if dmg not in names:
        sys.exit(f"{latest['tag_name']} has no {dmg} yet")
    sha = sha256_of(f"https://github.com/{REPO}/releases/download/v{app_version}/{dmg}")
    cask = re.sub(r'^(\s*version ")[^"]+(")', rf"\g<1>{app_version}\g<2>", cask, count=1, flags=re.M)
    cask = re.sub(r'^(\s*sha256 ")[0-9a-f]+(")', rf"\g<1>{sha}\g<2>", cask, count=1, flags=re.M)
    open(cask_path, "w").write(cask)
    moved.append(f"FolderSkin {app_version}")

# The command line: the formula.
formula_path = os.path.join(ROOT, "Formula", "folderskin-cli.rb")
formula = open(formula_path).read()
releases = gh(f"repos/{REPO}/releases?per_page=50")
cli = [r for r in releases if r["tag_name"].startswith("cli-v") and not r["draft"] and not r["prerelease"]]
if cli:
    newest = max(cli, key=lambda r: as_tuple(r["tag_name"]))
    cli_version = newest["tag_name"][len("cli-v"):]
    if as_tuple(cli_version) > as_tuple(version_of(formula)):
        sums_url = f"https://github.com/{REPO}/releases/download/cli-v{cli_version}/SHA256SUMS"
        sums = urllib.request.urlopen(sums_url, timeout=60).read().decode()
        sha = {name.lstrip("*"): digest for digest, name in (line.split() for line in sums.splitlines() if line.strip())}
        old = version_of(formula)
        formula = formula.replace(f"cli-v{old}/", f"cli-v{cli_version}/").replace(f"folderskin-cli-{old}-", f"folderskin-cli-{cli_version}-")
        formula = re.sub(r'^(\s*version ")[^"]+(")', rf"\g<1>{cli_version}\g<2>", formula, count=1, flags=re.M)

        def with_sha(match):
            url, digest = match.group(1), match.group(2)
            name = url.rsplit("/", 1)[1]
            if name not in sha:
                sys.exit(f"cli-v{cli_version} has no {name}")
            return match.group(0).replace(digest, sha[name])

        formula = re.sub(r'url "([^"]+)"\s*\n\s*sha256 "([0-9a-f]+)"', with_sha, formula)
        open(formula_path, "w").write(formula)
        moved.append(f"the command line {cli_version}")

open(os.path.join(HERE, ".bumped"), "w").write(" and ".join(moved))
print("Moved to " + " and ".join(moved) if moved else "Up to date")
