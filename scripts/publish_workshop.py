#!/usr/bin/env python3
"""Publish a Housing Realism release to an existing Steam Workshop item.

Run it by hand on Windows or macOS from a clean checkout of the release tag.
Use --dry-run to run the content checks and write the VDF without contacting
Steam or checking git.

Required environment:
  WORKSHOP_ITEM_ID   publishedfileid of the existing item. Must be non-zero.
  STEAM_USERNAME     Steam account owning that item.

Optional environment:
  STEAM_CMD          directory containing steamcmd.sh or steamcmd.exe. When
                     unset, steamcmd is looked up on PATH.

The first step logs in interactively, so SteamCMD asks for the password and
Steam Guard code when it has no cached session. SteamCMD keeps the session on
this machine; no credential is stored in the repository.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

APP_ID = "529340"
ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / ".metadata" / "metadata.json"
PUBLISH_ROOT = ROOT / ".publish"
STAGING = ROOT / ".publish-staging" / "current"

# Only game-facing content goes into the workshop item. Repository tooling,
# docs and release scripts must never be uploaded.
INCLUDE = (
    ".metadata",
    "common",
    "events",
    "gfx",
    "gui",
    "localization",
    "thumbnail.png",
    "LICENSE",
)


def fail(message: str) -> None:
    print(f"error: {message}", file=sys.stderr)
    raise SystemExit(1)


def vdf_quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def read_metadata() -> dict:
    if not METADATA.is_file():
        fail(f"missing {METADATA}")
    try:
        data = json.loads(METADATA.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot parse .metadata/metadata.json: {exc}")
    if data.get("game_id") != "victoria3":
        fail(f"game_id must be victoria3, got {data.get('game_id')!r}")
    version = data.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"[0-9][A-Za-z0-9.+-]*", version):
        fail(f"metadata version is not a usable release version: {version!r}")
    return data


def resolve_item_id() -> str:
    item_id = os.environ.get("WORKSHOP_ITEM_ID", "").strip()
    if not re.fullmatch(r"[0-9]+", item_id) or item_id == "0":
        fail("WORKSHOP_ITEM_ID must be the non-zero numeric id of an existing workshop item")
    return item_id


def git(*args: str) -> str:
    result = subprocess.run(
        ["git", *args], cwd=ROOT, text=True, capture_output=True, check=False
    )
    if result.returncode != 0:
        fail(f"git {' '.join(args)} failed: {result.stderr.strip()}")
    return result.stdout


def check_release_checkout(version: str) -> None:
    if git("status", "--porcelain").strip():
        fail("working tree has uncommitted changes; commit or stash them first")
    tags = git("tag", "--points-at", "HEAD").split()
    if f"v{version}" not in tags:
        fail(f"HEAD is not tagged v{version} (tags at HEAD: {tags or 'none'})")


def build_staging() -> Path:
    if STAGING.exists():
        shutil.rmtree(STAGING)
    STAGING.mkdir(parents=True)

    included: list[str] = []
    for name in INCLUDE:
        source = ROOT / name
        if not source.exists():
            continue
        target = STAGING / name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
        included.append(name)

    if ".metadata" not in included:
        fail("staging has no .metadata directory; launcher would not recognise the mod")
    if not (STAGING / ".metadata" / "metadata.json").is_file():
        fail("staging is missing .metadata/metadata.json")
    if "common" not in included:
        fail("staging has no common/ directory")
    return STAGING


def write_vdf(staging: Path, item_id: str, note: str) -> Path:
    PUBLISH_ROOT.mkdir(exist_ok=True)
    vdf = PUBLISH_ROOT / "workshop.vdf"

    # Keys omitted from the VDF are left untouched on the workshop page.
    # title, description, visibility, tags and previewfile are intentionally
    # absent so an update only replaces content and the change note.
    lines = [
        '"workshopitem"',
        "{",
        f'\t"appid" "{APP_ID}"',
        f'\t"publishedfileid" "{item_id}"',
        f'\t"contentfolder" "{vdf_quote(str(staging))}"',
        f'\t"changenote" "{vdf_quote(note)}"',
        "}",
        "",
    ]
    vdf.write_text("\n".join(lines), encoding="utf-8")
    return vdf


def find_steamcmd() -> Path:
    steam_dir = os.environ.get("STEAM_CMD", "").strip()
    if steam_dir:
        for name in ("steamcmd.exe", "steamcmd.sh"):
            candidate = Path(steam_dir) / name
            if candidate.is_file():
                return candidate
        fail(f"no steamcmd.exe or steamcmd.sh in STEAM_CMD={steam_dir}")
    found = shutil.which("steamcmd")
    if not found:
        fail("steamcmd not found; set STEAM_CMD to its directory or add it to PATH")
    return Path(found)


def run_steamcmd(vdf: Path, item_id: str) -> None:
    username = os.environ.get("STEAM_USERNAME", "").strip()
    if not username:
        fail("STEAM_USERNAME is not set")
    steamcmd = str(find_steamcmd())

    # Interactive login: the terminal stays attached so SteamCMD can ask for
    # the password and Steam Guard code, then caches the session.
    print("logging in; enter the password and Steam Guard code if asked", flush=True)
    login = subprocess.run([steamcmd, "+login", username, "+quit"], check=False)
    if login.returncode != 0:
        fail(f"steamcmd login exited with {login.returncode}")

    # The session is cached now, so the upload must never prompt.
    command = [
        steamcmd,
        "+@NoPromptForPassword",
        "1",
        "+@ShutdownOnFailedCommand",
        "1",
        "+login",
        username,
        "+workshop_build_item",
        str(vdf),
        "+quit",
    ]
    print("running:", " ".join(command), flush=True)
    result = subprocess.run(command, text=True, capture_output=True, check=False)
    output = result.stdout + result.stderr
    print(output, flush=True)

    if result.returncode != 0:
        fail(f"steamcmd exited with {result.returncode}")
    lowered = output.lower()
    if "skipping hidden file" in lowered:
        fail("steamcmd skipped a hidden file; .metadata may be missing from the item")
    if "error!" in lowered or "failed to update workshop item" in lowered:
        fail("steamcmd reported an upload error")
    # A login line can also contain "success". Require the commit line too.
    if "success" not in lowered or "committing update" not in lowered:
        fail("steamcmd did not report a successful commit; refusing to assume the upload worked")

    # steamcmd rewrites publishedfileid on success. A changed value would mean
    # a new item was created instead of updating the existing one.
    rewritten = re.search(r'"publishedfileid"\s+"([0-9]+)"', vdf.read_text(encoding="utf-8"))
    if not rewritten or rewritten.group(1) != item_id:
        fail("publishedfileid changed during upload; the wrong item may have been published")

    print(f"published workshop item {item_id}", flush=True)
    # A successful SubmitItemUpdate does not guarantee the public Change Notes
    # changed, nor that the launcher recognises the downloaded content.
    print("verify on the workshop page: change note, file list, and a fresh subscription", flush=True)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true", help="build staging and VDF only")
    parser.add_argument("--note", help="change note (default: the version)")
    args = parser.parse_args()

    metadata = read_metadata()
    version = metadata["version"]
    item_id = resolve_item_id()
    if not args.dry_run:
        check_release_checkout(version)

    note = (args.note or "").strip() or f"v{version}"
    # Steam rejects SubmitItemUpdate above ~8000 bytes even when the text is
    # well under the character limit (EResult=8 on multi-byte descriptions).
    if len(note.encode("utf-8")) > 8000:
        fail("change note exceeds Steam's 8000-byte limit")

    staging = build_staging()
    vdf = write_vdf(staging, item_id, note)

    files = sorted(
        str(path.relative_to(staging)) for path in staging.rglob("*") if path.is_file()
    )
    print(f"version:   {version}")
    print(f"item id:   {item_id}")
    print(f"note:      {note}")
    print(f"staging:   {staging}")
    print(f"vdf:       {vdf}")
    print(f"files ({len(files)}):")
    for name in files:
        print(f"  {name}")
    print("--- VDF ---")
    print(vdf.read_text(encoding="utf-8"), end="")

    if args.dry_run:
        print("dry run complete; no upload performed")
        return

    run_steamcmd(vdf, item_id)


if __name__ == "__main__":
    main()
