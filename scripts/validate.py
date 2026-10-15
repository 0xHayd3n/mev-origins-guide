#!/usr/bin/env python3
# SPDX-License-Identifier: MIT
"""Validate this reading guide offline; never run or reproduce the paper's study.

Uses only the Python standard library. Run from any directory with
``python scripts/validate.py`` (or pass ``--root`` for another checkout).
"""

from __future__ import annotations

import argparse
import html
import json
import posixpath
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


ARXIV_ID = "2604.27979"
VERSION = "v1"
TITLE = (
    "The Origins of MEV: Systematic Attribution of Arbitrage Opportunity "
    "Creation at Scale"
)
AUTHORS = (
    ("Andrei", "Seoev"),
    ("Dmitry", "Belousov"),
    ("Anastasiia", "Smirnova"),
    ("Ksenia", "Kurinova"),
    ("Aleksei", "Smirnov"),
    ("Denis", "Fedyanin"),
    ("Yury", "Yanovich"),
)
REQUIRED = (
    "README.md",
    "AGENTS.md",
    "SOURCES.md",
    "ATTRIBUTION.md",
    "CITATION.cff",
    "LICENSE.md",
    "LICENSE-CODE",
    "metadata.json",
    "llms.txt",
    "references/paper.bib",
)
SKIP_DIRS = {".git", ".venv", "venv", "__pycache__", ".pytest_cache"}
FORBIDDEN_SUFFIXES = {
    ".pdf", ".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".ico",
    ".bmp", ".tif", ".tiff", ".avif", ".heic", ".zip", ".tar", ".gz",
    ".bz2", ".xz", ".7z", ".rar", ".pem", ".key", ".p12", ".pfx",
    ".kdbx", ".sqlite", ".sqlite3", ".db",
}
FORBIDDEN_PARTS = {
    "private-source", "private-transfer", "attachments", "credentials",
    ".aws", ".ssh", ".codex", ".agents",
}
FORBIDDEN_NAMES = {".env", "credentials.json", "credentials", "secrets.json"}
SUSPICIOUS_FILENAME = re.compile(
    r"(?:^|[._-])(?:full[-_]?text|attachment)(?:[._-]|$)"
    r"|^2604[._]27979(?:v\d+)?\.(?:txt|md|html|xml)$",
    re.IGNORECASE,
)
# Match concrete credential shapes, not ordinary words such as "token" or "key".
SENSITIVE_PATTERNS = (
    ("Library file identifier", re.compile(r"\blibfile_[a-zA-Z0-9]{12,}\b")),
    ("attachment file identifier", re.compile(r"\bfile_[a-f0-9]{24,}\b")),
    ("GitHub credential", re.compile(r"\b(?:gh[pousr]_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,})\b")),
    ("AWS access key", re.compile(r"\b(?:AKIA|ASIA)[A-Z0-9]{16}\b")),
    ("API credential", re.compile(r"\bsk-(?:proj-)?[A-Za-z0-9_-]{24,}\b")),
    ("private key material", re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----")),
    ("signed or credential-bearing URL", re.compile(
        r"[?&](?:X-Amz-Signature|X-Amz-Credential|X-Amz-Security-Token|"
        r"X-Goog-Signature|X-Goog-Credential|sig|signature|access_token|"
        r"auth_token)=[^\s&<>\"']+", re.IGNORECASE,
    )),
    ("absolute machine path", re.compile(
        r"\b[A-Za-z]:[\\/][^\s<>\"']+"
        r"|(?<![\w\x3a/])/(?:Users|home|mnt|tmp|private/var)/[^\s<>\"']+",
        re.IGNORECASE,
    )),
)
MAGIC = (
    b"%PDF-", b"\x89PNG\r\n\x1a\n", b"\xff\xd8\xff", b"GIF87a", b"GIF89a",
    b"PK\x03\x04", b"\x1f\x8b", b"7z\xbc\xaf\x27\x1c", b"Rar!\x1a\x07",
)
INLINE_LINK = re.compile(
    r"!?\[[^\]\n]*\]\(\s*(?:<(?P<angle>[^>\n]*)>|"
    r"(?P<bare>(?:\\.|[^\s()\\]|\([^()\n]*\))+))"
)
REFERENCE_LINK = re.compile(
    r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:\s*(?:<([^>\n]*)>|(\S+))"
)
HTML_LINK = re.compile(r"\b(?:href|src)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)
HTML_ANCHOR = re.compile(r"\b(?:id|name)\s*=\s*[\"']([^\"']+)[\"']", re.IGNORECASE)


class Validation:
    def __init__(self, root: Path) -> None:
        self.root = root.resolve()
        self.errors: list[str] = []
        self.files: dict[str, Path] = {}
        self.text: dict[str, str] = {}
        self.json_files = 0
        self.local_links = 0
        self.anchor_cache: dict[str, set[str]] = {}

    def fail(self, file: str, message: str, line: int | None = None) -> None:
        location = f"{file}:{line}" if line is not None else file
        self.errors.append(f"{location}: {message}")

    def inventory(self) -> None:
        if not self.root.is_dir():
            self.fail("repository", "root directory does not exist")
            return
        for path in sorted(self.root.rglob("*")):
            relative = path.relative_to(self.root)
            if any(part in SKIP_DIRS for part in relative.parts):
                continue
            name = relative.as_posix()
            if path.is_symlink():
                self.fail(name, "symlinks are not allowed in this documentation repository")
                continue
            if not path.is_file():
                continue
            self.files[name] = path
            lower_parts = [part.lower() for part in relative.parts]
            if (
                path.suffix.lower() in FORBIDDEN_SUFFIXES
                or any(part in FORBIDDEN_PARTS for part in lower_parts)
                or path.name.lower() in FORBIDDEN_NAMES
                or SUSPICIOUS_FILENAME.search(path.name)
            ):
                self.fail(name, "paper assets, private inputs, archives, or credential files must not be published")
            try:
                data = path.read_bytes()
            except OSError as exc:
                self.fail(name, f"cannot read file ({exc.__class__.__name__})")
                continue
            if any(data.startswith(prefix) for prefix in MAGIC) or b"\0" in data:
                self.fail(name, "binary content is not allowed; link to paper assets instead")
                continue
            try:
                content = data.decode("utf-8")
            except UnicodeDecodeError:
                self.fail(name, "file must contain UTF-8 text")
                continue
            self.text[name] = content
            if b"\r" in data:
                self.fail(name, "use LF line endings")
            if re.search(r"[\x00-\x08\x0b\x0c\x0e-\x1f\x7f]", content):
                self.fail(name, "contains an unexpected control character")
            for label, pattern in SENSITIVE_PATTERNS:
                for match in pattern.finditer(content):
                    self.fail(name, f"contains {label}; matched value is deliberately hidden", content.count("\n", 0, match.start()) + 1)
        for name in REQUIRED:
            if name not in self.files:
                self.fail(name, "required file is missing")
            elif not self.text.get(name, "").strip():
                self.fail(name, "required file must contain readable text")

    def validate_json(self) -> dict | None:
        metadata = None

        def unique_object(pairs: list[tuple[str, object]]) -> dict:
            result = {}
            for key, value in pairs:
                if key in result:
                    raise ValueError("duplicate object key")
                result[key] = value
            return result

        def reject_constant(value: str) -> None:
            raise ValueError(f"non-JSON numeric constant: {value}")

        for name, content in self.text.items():
            if not name.lower().endswith(".json"):
                continue
            self.json_files += 1
            try:
                data = json.loads(content, object_pairs_hook=unique_object, parse_constant=reject_constant)
            except (ValueError, json.JSONDecodeError) as exc:
                self.fail(name, f"invalid JSON: {exc}")
                continue
            if name == "metadata.json":
                if isinstance(data, dict):
                    metadata = data
                else:
                    self.fail(name, "metadata must be a JSON object")
        return metadata

    def validate_metadata(self, metadata: dict | None) -> None:
        if metadata is None:
            return
        paper = metadata.get("paper")
        if not isinstance(paper, dict):
            self.fail("metadata.json", "paper must be an object")
            return
        if paper.get("arxiv_id") not in (ARXIV_ID, ARXIV_ID + VERSION):
            self.fail("metadata.json", f"paper.arxiv_id must identify {ARXIV_ID}")
        version = paper.get("version")
        if not (version in (VERSION, "1") or (type(version) is int and version == 1)):
            self.fail("metadata.json", "paper.version must identify v1")
        if " ".join(str(paper.get("title", "")).split()) != TITLE:
            self.fail("metadata.json", "paper.title does not match the attributed paper")
        names = []
        for author in paper.get("authors", []) if isinstance(paper.get("authors"), list) else []:
            if isinstance(author, str):
                names.append(" ".join(author.split()))
            elif isinstance(author, dict):
                names.append(f"{author.get('given', '')} {author.get('family', '')}".strip())
        if names != [f"{given} {family}" for given, family in AUTHORS]:
            self.fail("metadata.json", "paper.authors must list all seven paper authors in paper order")

        def strings(value: object):
            if isinstance(value, str):
                yield value
            elif isinstance(value, dict):
                for child in value.values():
                    yield from strings(child)
            elif isinstance(value, list):
                for child in value:
                    yield from strings(child)

        if not any(re.fullmatch(r"https://arxiv\.org/(?:abs|pdf|html)/2604\.27979v1(?:\.pdf)?", url) for url in strings(paper.get("urls"))):
            self.fail("metadata.json", "paper.urls must include an official, version-pinned arXiv v1 URL")
        status = metadata.get("research_status")
        if not isinstance(status, dict) or status.get("experiments_reproduced") is not False:
            self.fail("metadata.json", "research_status.experiments_reproduced must be false")

    def validate_attribution(self) -> None:
        readme = self.text.get("README.md", "")
        if not readme:
            return
        for given, family in AUTHORS:
            if not re.search(rf"\b{given}\s+{family}\b", readme):
                self.fail("README.md", f"missing paper author attribution: {given} {family}")
        for name in ("CITATION.cff", "references/paper.bib"):
            content = self.text.get(name, "")
            if not content:
                continue
            for given, family in AUTHORS:
                if not re.search(rf"\b{given}\b", content) or not re.search(rf"\b{family}\b", content):
                    self.fail(name, f"missing paper author name: {given} {family}")
            if ARXIV_ID not in content:
                self.fail(name, "missing paper arXiv identifier")
        if self.text.get("CITATION.cff") and not re.search(r"(?m)^cff-version:\s*[\"']?1\.2\.0", self.text["CITATION.cff"]):
            self.fail("CITATION.cff", "expected a CFF 1.2.0 citation declaration")

    @staticmethod
    def without_code(content: str) -> str:
        """Blank fenced/inline code while preserving offsets for line reporting."""
        lines = []
        fence_char = None
        fence_length = 0
        for line in content.splitlines(keepends=True):
            fence = re.match(r"^ {0,3}(`{3,}|~{3,})", line)
            if fence_char is None and fence:
                fence_char = fence.group(1)[0]
                fence_length = len(fence.group(1))
                lines.append("".join("\n" if char == "\n" else " " for char in line))
            elif fence_char is not None:
                lines.append("".join("\n" if char == "\n" else " " for char in line))
                if fence and fence.group(1)[0] == fence_char and len(fence.group(1)) >= fence_length:
                    fence_char = None
            else:
                lines.append(line)
        return re.sub(r"(`+)([^`\n]*?)\1", lambda match: " " * len(match.group(0)), "".join(lines))

    @staticmethod
    def heading_slug(text: str) -> str:
        text = re.sub(r"!?\[([^\]]+)\]\([^)]*\)", r"\1", text)
        text = html.unescape(re.sub(r"<[^>]+>", "", text)).lower().strip()
        text = "".join(char for char in text if char in "-_" or not unicodedata.category(char).startswith(("P", "S")))
        return re.sub(r"\s", "-", text)

    def anchors(self, name: str) -> set[str]:
        if name in self.anchor_cache:
            return self.anchor_cache[name]
        # Keep inline code text in heading IDs, but remove fenced code blocks.
        content = self.text.get(name, "")
        fenced = re.sub(r"(?ms)^ {0,3}(`{3,}|~{3,})[^\n]*\n.*?^ {0,3}\1[^\n]*(?:\n|$)", "", content)
        anchors = {html.unescape(match.group(1)) for match in HTML_ANCHOR.finditer(fenced)}
        used: dict[str, int] = {}
        lines = fenced.splitlines()
        for index, line in enumerate(lines):
            heading = re.match(r"^ {0,3}#{1,6}\s+(.+?)\s*#*\s*$", line)
            text = heading.group(1) if heading else None
            if text is None and index + 1 < len(lines) and line.strip() and re.fullmatch(r" {0,3}(?:=+|-+)\s*", lines[index + 1]):
                text = line.strip()
            if text is None:
                continue
            slug = self.heading_slug(text)
            candidate = slug
            while candidate in used:
                used[slug] = used.get(slug, 0) + 1
                candidate = f"{slug}-{used[slug]}"
            used[candidate] = 0
            anchors.add(candidate)
        self.anchor_cache[name] = anchors
        return anchors

    def validate_target(self, source: str, target: str, line: int) -> None:
        target = html.unescape(re.sub(r"\\([()\[\] ])", r"\1", target))
        try:
            url = urlsplit(target)
        except ValueError:
            self.fail(source, "malformed link target", line)
            return
        if url.scheme in {"https", "http", "mailto", "tel"} or url.netloc:
            return
        if url.scheme:
            self.fail(source, f"unsupported link scheme: {url.scheme}", line)
            return
        self.local_links += 1
        link_path = unquote(url.path)
        if "\\" in link_path or link_path.startswith("/"):
            self.fail(source, f"local link must use a repository-relative POSIX path: {target}", line)
            return
        name = posixpath.normpath(posixpath.join(posixpath.dirname(source), link_path)) if link_path else source
        if name == ".." or name.startswith("../"):
            self.fail(source, f"local link leaves the repository: {target}", line)
            return
        if name not in self.files:
            if name == "." or any(item.startswith(name.rstrip("/") + "/") for item in self.files):
                if not url.fragment:
                    return
                name = posixpath.join(name, "README.md").removeprefix("./")
            if name not in self.files:
                self.fail(source, f"missing local link target (case-sensitive): {target}", line)
                return
        if url.fragment and name.lower().endswith((".md", ".markdown")):
            fragment = unquote(url.fragment)
            if fragment not in self.anchors(name):
                self.fail(source, f"missing Markdown heading or HTML anchor: {target}", line)

    def validate_links(self) -> None:
        for name, content in self.text.items():
            if not name.lower().endswith((".md", ".markdown")):
                continue
            stripped = self.without_code(content)
            definitions = {
                " ".join(match.group(1).split()).casefold()
                for match in re.finditer(r"(?m)^[ \t]{0,3}\[([^\]\n]+)\]:", stripped)
            }
            for match in re.finditer(r"!?\[([^\]\n]+)\]\[([^\]\n]*)\]", stripped):
                label = " ".join((match.group(2) or match.group(1)).split()).casefold()
                if label not in definitions:
                    self.fail(name, f"undefined Markdown link reference: {label}", stripped.count("\n", 0, match.start()) + 1)
            for pattern in (INLINE_LINK, REFERENCE_LINK, HTML_LINK):
                for match in pattern.finditer(stripped):
                    target = next((group for group in match.groups() if group is not None), "")
                    self.validate_target(name, target, stripped.count("\n", 0, match.start()) + 1)

    def run(self) -> int:
        self.inventory()
        metadata = self.validate_json()
        self.validate_metadata(metadata)
        self.validate_attribution()
        self.validate_links()
        if self.errors:
            print(f"FAIL: {len(self.errors)} issue(s) in {len(self.files)} repository file(s).")
            for error in self.errors:
                print(f"  - {error}")
            return 1
        print(
            f"PASS: {len(self.files)} files; {self.json_files} JSON files; "
            f"{self.local_links} local Markdown links; paper v1 metadata and seven authors verified."
        )
        print("Offline static checks only. External URL availability, full CFF/YAML semantics, numeric study claims, and experimental reproduction are not validated.")
        return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1], help="repository root (defaults to this script's checkout)")
    args = parser.parse_args()
    return Validation(args.root).run()


if __name__ == "__main__":
    sys.exit(main())
