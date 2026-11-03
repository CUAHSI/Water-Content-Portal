#!/usr/bin/env python3
"""
Find frontmatter URL-like fields (edit_url, source_url, doi, venue.url,
author/affiliation url & github & orcid, binder, arxiv, ...) that don't
resolve, across every markdown page under book/, and write them to a CSV
report: one row per broken field, with columns path, field, value.

This never modifies content files - it only reads them and writes the CSV
report plus a local cache of previously-checked URLs (so repeat runs don't
re-hit the network for links that were already confirmed OK/broken
recently).

Usage:
    python3 scripts/check_frontmatter_urls.py [--refresh] [--strict]
        [--output PATH] [--cache-ttl-days N]

--refresh          ignore the cache and re-check every URL and every page
--strict            exit with a non-zero status if any broken links are found
--output PATH       where to write the CSV report (default: scripts/reports/frontmatter-url-report.csv)
--cache-ttl-days N  how long a cached "URL is fine" result stays valid (default: 30)

Set GITHUB_TOKEN (or GH_TOKEN) to raise GitHub's API rate limit.
"""

from __future__ import annotations

import argparse
import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    import yaml
except ImportError:  # pragma: no cover - degrade gracefully if PyYAML is missing
    yaml = None

REPO_ROOT = Path(__file__).resolve().parent.parent
BOOK_ROOT = REPO_ROOT / "book"
MYST_YML = BOOK_ROOT / "myst.yml"
EXCLUDE_DIR_NAMES = {"_build", "node_modules", ".git"}

CACHE_PATH = Path(__file__).resolve().parent / ".cache" / "frontmatter-url-cache.json"
DEFAULT_OUTPUT = Path(__file__).resolve().parent / "reports" / "frontmatter-url-report.csv"
DEFAULT_CACHE_TTL_DAYS = 30

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)
GITHUB_URL_RE = re.compile(r"^https?://github\.com/([^/]+)/?([^/]*?)/?$")
USER_AGENT = "Mozilla/5.0 (compatible; Water-Learning-Commons link checker)"

# frontmatter keys whose string value is a GitHub repo/user reference rather
# than a literal URL (handled via the GitHub API for accuracy + caching)
GITHUB_KEYS = {"github"}
# frontmatter keys that are literal URLs we can check directly
LITERAL_URL_KEYS = {"url", "edit_url", "source_url", "binder"}
# frontmatter keys that are identifiers we normalize into a URL first
IDENTIFIER_KEYS = {"doi", "arxiv", "orcid"}


class Cache:
    def __init__(self, path: Path, ttl_days: float):
        self.path = path
        self.ttl_seconds = ttl_days * 86400
        self.data = {"files": {}, "urls": {}}
        if path.exists():
            try:
                self.data = json.loads(path.read_text(encoding="utf-8"))
            except (json.JSONDecodeError, OSError):
                pass
        self.data.setdefault("files", {})
        self.data.setdefault("urls", {})

    def get_file_fields(self, rel_path: str, mtime: float):
        entry = self.data["files"].get(rel_path)
        if entry and entry.get("mtime") == mtime:
            return [tuple(field) for field in entry["fields"]]
        return None

    def set_file_fields(self, rel_path: str, mtime: float, fields: list[tuple[str, str]]):
        self.data["files"][rel_path] = {"mtime": mtime, "fields": [list(f) for f in fields]}

    def get_url_result(self, url: str) -> bool | None:
        entry = self.data["urls"].get(url)
        if not entry:
            return None
        if time.time() - entry.get("checked_at", 0) > self.ttl_seconds:
            return None
        return entry.get("ok")

    def set_url_result(self, url: str, ok: bool):
        self.data["urls"][url] = {"ok": ok, "checked_at": time.time()}

    def save(self):
        self.path.parent.mkdir(parents=True, exist_ok=True)
        tmp_path = self.path.with_suffix(".tmp")
        tmp_path.write_text(json.dumps(self.data, indent=2), encoding="utf-8")
        tmp_path.replace(self.path)


def parse_frontmatter(text: str) -> dict:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    if yaml is None:
        return {}
    try:
        data = yaml.safe_load(match.group(1))
    except yaml.YAMLError:
        return {}
    return data if isinstance(data, dict) else {}


def get_project_frontmatter() -> dict:
    if yaml is None:
        return {}
    try:
        data = yaml.safe_load(MYST_YML.read_text(encoding="utf-8"))
    except yaml.YAMLError:
        return {}
    project = data.get("project") if isinstance(data, dict) else None
    return project if isinstance(project, dict) else {}


def normalize_identifier(key: str, value: str) -> str | None:
    value = value.strip()
    if not value:
        return None
    if value.startswith("http://") or value.startswith("https://"):
        return value
    if key == "doi":
        return f"https://doi.org/{value}"
    if key == "arxiv":
        return f"https://arxiv.org/abs/{value}"
    if key == "orcid":
        return f"https://orcid.org/{value}"
    return None


def parse_github_reference(value: str) -> tuple[str, str | None] | None:
    """Return (owner, repo_or_None) for a github frontmatter value."""
    value = value.strip()
    match = GITHUB_URL_RE.match(value)
    if match:
        owner, repo = match.group(1), match.group(2) or None
        return owner, (repo.removesuffix(".git") if repo else None)
    if re.match(r"^@?[\w.-]+/[\w.-]+$", value):
        owner, repo = value.lstrip("@").split("/", 1)
        return owner, repo
    if re.match(r"^@?[\w.-]+$", value):
        return value.lstrip("@"), None
    return None


def walk_fields(node, path: str, out: list[tuple[str, str, str]]):
    """Collect (field_path, kind, raw_value) for every URL-like leaf field."""
    if isinstance(node, dict):
        for key, value in node.items():
            child_path = f"{path}.{key}" if path else key
            if isinstance(value, str):
                if key in LITERAL_URL_KEYS and value.lower() not in ("null", "none", ""):
                    if value.startswith("http://") or value.startswith("https://"):
                        out.append((child_path, "literal_url", value))
                elif key in GITHUB_KEYS:
                    out.append((child_path, "github", value))
                elif key in IDENTIFIER_KEYS:
                    out.append((child_path, "identifier:" + key, value))
            else:
                walk_fields(value, child_path, out)
    elif isinstance(node, list):
        for index, value in enumerate(node):
            walk_fields(value, f"{path}[{index}]", out)


def extract_fields(frontmatter: dict) -> list[tuple[str, str, str]]:
    fields: list[tuple[str, str, str]] = []
    walk_fields(frontmatter, "", fields)
    return fields


class NotFoundError(Exception):
    """The remote resource definitively does not exist (HTTP 404/410)."""


class ApiError(Exception):
    """The check was inconclusive (rate limiting, network error, 5xx, ...)."""


def _api_request(url: str) -> dict | list:
    headers = {"Accept": "application/vnd.github+json", "User-Agent": USER_AGENT}
    token = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
    if token:
        headers["Authorization"] = f"Bearer {token}"
    request = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        if error.code in (404, 410):
            raise NotFoundError(str(error)) from error
        raise ApiError(f"{error.code} {error.reason}") from error
    except urllib.error.URLError as error:
        raise ApiError(str(error.reason)) from error


_default_branch_cache: dict[str, str | None] = {}


def github_repo_exists(owner: str, repo: str | None) -> bool | None:
    try:
        if repo:
            _api_request(f"https://api.github.com/repos/{owner}/{repo}")
        else:
            _api_request(f"https://api.github.com/users/{owner}")
        return True
    except NotFoundError:
        return False
    except ApiError:
        return None


def get_default_branch(owner: str, repo: str) -> str | None:
    """Return the repo's default branch, or None if it can't be determined."""
    key = f"{owner}/{repo}"
    if key in _default_branch_cache:
        return _default_branch_cache[key]
    try:
        data = _api_request(f"https://api.github.com/repos/{owner}/{repo}")
        branch = data.get("default_branch")
    except (NotFoundError, ApiError):
        branch = None
    _default_branch_cache[key] = branch
    return branch


def github_path_exists(owner: str, repo: str, branch: str, path: str) -> bool | None:
    url = f"https://api.github.com/repos/{owner}/{repo}/contents/{urllib.parse.quote(path)}?ref={branch}"
    try:
        _api_request(url)
        return True
    except NotFoundError:
        return False
    except ApiError:
        return None


def http_url_resolves(url: str) -> bool | None:
    """Return True/False for a definitive result, None if inconclusive."""
    for method in ("HEAD", "GET"):
        request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT}, method=method)
        try:
            with urllib.request.urlopen(request, timeout=15) as response:
                return 200 <= response.status < 400
        except urllib.error.HTTPError as error:
            if error.code in (404, 410):
                return False
            if error.code == 405 and method == "HEAD":
                continue  # method not allowed on HEAD - retry with GET
            return None  # inconclusive: rate limited, forbidden, server error, etc.
        except urllib.error.URLError:
            return None  # inconclusive: DNS/connection/timeout error
    return None


def check_url(cache: Cache, url: str) -> bool | None:
    cached = cache.get_url_result(url)
    if cached is not None:
        return cached
    ok = http_url_resolves(url)
    if ok is not None:
        cache.set_url_result(url, ok)
    return ok


def check_github_reference(cache: Cache, value: str) -> bool | None:
    parsed = parse_github_reference(value)
    if not parsed:
        return True  # not a recognizable github reference - nothing to validate
    owner, repo = parsed
    cache_key = f"github:{owner}/{repo}" if repo else f"github-user:{owner}"
    cached = cache.get_url_result(cache_key)
    if cached is not None:
        return cached
    ok = github_repo_exists(owner, repo)
    if ok is not None:
        cache.set_url_result(cache_key, ok)
    return ok


def iter_markdown_files():
    for path in BOOK_ROOT.rglob("*.md"):
        if any(part in EXCLUDE_DIR_NAMES for part in path.parts):
            continue
        yield path


def check_auto_computed_links(cache: Cache, path: Path, frontmatter: dict, project_github: str | None, rows: list[tuple[Path, str, str]], unverifiable: list[tuple[Path, str]]):
    """Flag MyST's auto-computed edit_url/source_url when no explicit override is set."""
    if "edit_url" in frontmatter or "source_url" in frontmatter:
        return  # author already took responsibility for these links
    github_value = frontmatter.get("github") or project_github
    if not isinstance(github_value, str):
        return
    parsed = parse_github_reference(github_value)
    if not parsed or not parsed[1]:
        return
    owner, repo = parsed
    branch = get_default_branch(owner, repo)
    if not branch:
        unverifiable.append((path, "edit_url (auto-computed)"))
        return
    rel_path = path.relative_to(BOOK_ROOT).as_posix()
    computed_url = f"https://github.com/{owner}/{repo}/edit/{branch}/{rel_path}"
    result_key = f"path-exists:{owner}/{repo}@{branch}:{rel_path}"
    cached = cache.get_url_result(result_key)
    if cached is None:
        cached = github_path_exists(owner, repo, branch, rel_path)
        if cached is None:
            unverifiable.append((path, "edit_url (auto-computed)"))
            return
        cache.set_url_result(result_key, cached)
    if not cached:
        rows.append((path, "edit_url (auto-computed)", computed_url))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--refresh", action="store_true", help="ignore the cache and re-check everything")
    parser.add_argument("--strict", action="store_true", help="exit 1 if broken links are found")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT, help="CSV report output path")
    parser.add_argument("--cache-ttl-days", type=float, default=DEFAULT_CACHE_TTL_DAYS, help="cache validity window in days")
    args = parser.parse_args()

    if yaml is None:
        print("PyYAML is not installed - run 'pip install pyyaml' to enable frontmatter checking.", file=sys.stderr)
        return 1

    cache = Cache(CACHE_PATH, args.cache_ttl_days)
    if args.refresh:
        cache.data = {"files": {}, "urls": {}}

    project_frontmatter = get_project_frontmatter()
    project_github = project_frontmatter.get("github")

    broken_rows: list[tuple[Path, str, str]] = []
    unverifiable: list[tuple[Path, str]] = []

    for path in sorted(iter_markdown_files()):
        rel_path = path.relative_to(REPO_ROOT).as_posix()
        mtime = path.stat().st_mtime
        cached_fields = None if args.refresh else cache.get_file_fields(rel_path, mtime)
        text = path.read_text(encoding="utf-8")
        frontmatter = parse_frontmatter(text)

        if cached_fields is None:
            fields = extract_fields(frontmatter)
            cache.set_file_fields(rel_path, mtime, fields)
        else:
            fields = cached_fields

        for field_path, kind, raw_value in fields:
            if kind == "github":
                ok = check_github_reference(cache, raw_value)
                value = raw_value
            elif kind == "literal_url":
                ok = check_url(cache, raw_value)
                value = raw_value
            elif kind.startswith("identifier:"):
                identifier_key = kind.split(":", 1)[1]
                resolved = normalize_identifier(identifier_key, raw_value)
                if resolved is None:
                    continue
                ok = check_url(cache, resolved)
                value = resolved
            else:
                continue

            if ok is False:
                broken_rows.append((path, field_path, value))
            elif ok is None:
                unverifiable.append((path, field_path))

        check_auto_computed_links(cache, path, frontmatter, project_github, broken_rows, unverifiable)

    cache.save()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["path", "field", "value"])
        for path, field_path, value in broken_rows:
            writer.writerow([path.relative_to(REPO_ROOT).as_posix(), field_path, value])

    print(f"Checked {len(list(iter_markdown_files()))} page(s). Found {len(broken_rows)} confirmed broken field(s).")
    print(f"Report written to {args.output.relative_to(REPO_ROOT).as_posix()}")
    if unverifiable:
        print(f"{len(unverifiable)} field(s) could not be verified (rate limiting/network errors) and were left out of the report - re-run to retry them.")

    if args.strict and broken_rows:
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
