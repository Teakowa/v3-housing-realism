#!/usr/bin/env python3
"""Publish a Housing Realism release to an existing Steam Workshop item.

Run by .github/workflows/publish-workshop.yml. Use --dry-run to run every local
check and write the VDF without contacting Steam.

Required environment:
  WORKSHOP_ITEM_ID   publishedfileid of the existing item. Must be non-zero.
  STEAM_USERNAME     Steam account owning that item.
  STEAM_CMD          directory containing steamcmd.sh (set by setup-steamcmd).

Optional:
  RELEASE_TAG        tag that triggered the run, e.g. v1.0.2. Required
                     unless --dry-run is used.
  COMMIT_SHA         short commit hash used in the change note.
  CHANGE_NOTE        override the change note.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

APP_ID = "529340"
ROOT = Path(__file__).resolve().parent.parent
METADATA = ROOT / ".metadata" / "metadata.json"
PUBLISH_ROOT = ROOT / ".publish"
STAGING_ROOT = ROOT / ".publish-staging"

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


def check_release_tag(version: str, dry_run: bool) -> None:
    tag = os.environ.get("RELEASE_TAG", "").strip()
    if not tag:
        if dry_run:
            return
        fail("RELEASE_TAG is not set; publishing runs only from a version tag")
    if tag != f"v{version}":
        fail(f"tag {tag!r} does not match metadata version {version!r}; expected v{version}")


def build_staging(run_id: str) -> Path:
    staging = STAGING_ROOT / run_id
    if staging.exists():
        fail(f"staging path already exists: {staging}")
    staging.mkdir(parents=True)

    included: list[str] = []
    for name in INCLUDE:
        source = ROOT / name
        if not source.exists():
            continue
        target = staging / name
        if source.is_dir():
            shutil.copytree(source, target)
        else:
            shutil.copy2(source, target)
        included.append(name)

    if ".metadata" not in included:
        fail("staging has no .metadata directory; launcher would not recognise the mod")
    if not (staging / ".metadata" / "metadata.json").is_file():
        fail("staging is missing .metadata/metadata.json")
    if "common" not in included:
        fail("staging has no common/ directory")
    return staging


def write_vdf(run_id: str, staging: Path, item_id: str, note: str) -> Path:
    PUBLISH_ROOT.mkdir(exist_ok=True)
    vdf = PUBLISH_ROOT / f"workshop-{run_id}.vdf"

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


def run_steamcmd(vdf: Path, item_id: str) -> None:
    username = os.environ.get("STEAM_USERNAME", "").strip()
    if not username:
        fail("STEAM_USERNAME is not set")
    steam_dir = os.environ.get("STEAM_CMD", "").strip()
    if not steam_dir:
        fail("STEAM_CMD is not set; expected the directory containing steamcmd.sh")
    steamcmd = Path(steam_dir) / "steamcmd.sh"
    if not steamcmd.is_file():
        fail(f"steamcmd.sh not found at {steamcmd}")

    command = [
        str(steamcmd),
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
    args = parser.parse_args()

    metadata = read_metadata()
    version = metadata["version"]
    item_id = resolve_item_id()
    check_release_tag(version, args.dry_run)

    sha = os.environ.get("COMMIT_SHA", "").strip()[:7]
    note = os.environ.get("CHANGE_NOTE", "").strip() or f"v{version}" + (f" ({sha})" if sha else "")
    # Steam rejects SubmitItemUpdate above ~8000 bytes even when the text is
    # well under the character limit (EResult=8 on multi-byte descriptions).
    if len(note.encode("utf-8")) > 8000:
        fail("change note exceeds Steam's 8000-byte limit")
    if args.dry_run:
        # Local dry runs must not collide with an earlier staging tree.
        run_id = f"dryrun-{time.time_ns()}"
    else:
        run_id = sha or f"local-{time.strftime('%Y%m%d-%H%M%S')}"

    staging = build_staging(run_id)
    vdf = write_vdf(run_id, staging, item_id, note)

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
