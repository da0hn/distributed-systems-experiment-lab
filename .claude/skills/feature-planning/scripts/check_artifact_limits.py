#!/usr/bin/env python3
"""Validate the character budgets for feature-planning artifacts."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


LIMITS_BY_NAME = {
    "feature-card.md": 5500,
    "example-mapping.md": 4500,
    "behavior.feature": 3500,
    "implementation-plan.md": 7000,
}
LIMITS_BY_PATH = {
    Path("docs/architecture/integrations.md"): 12000,
}
MARKDOWN_LIMIT = 4000
ADR_LIMIT = 9000
CONTRACT_LIMIT = 16000


def parse_limit(value: str) -> tuple[Path, int]:
    try:
        raw_path, raw_limit = value.rsplit("=", 1)
        limit = int(raw_limit)
    except ValueError as error:
        raise argparse.ArgumentTypeError(
            "Use <caminho>=<limite-positivo>."
        ) from error
    if not raw_path or limit <= 0:
        raise argparse.ArgumentTypeError(
            "Use <caminho>=<limite-positivo>."
        )
    return Path(raw_path), limit


def resolve_inside(root: Path, relative_path: Path) -> Path:
    candidate = (root / relative_path).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as error:
        raise ValueError(f"Fora da raiz: {relative_path}") from error
    return candidate


def default_limit(relative_path: Path) -> int:
    if relative_path in LIMITS_BY_PATH:
        return LIMITS_BY_PATH[relative_path]
    if relative_path.name in LIMITS_BY_NAME:
        return LIMITS_BY_NAME[relative_path.name]
    if relative_path.parts[:2] == ("docs", "adr") and relative_path.suffix == ".md":
        return ADR_LIMIT
    if relative_path.suffix in {".yaml", ".yml", ".json"}:
        return CONTRACT_LIMIT
    if relative_path.suffix == ".md":
        return MARKDOWN_LIMIT
    raise ValueError(f"Sem limite definido para: {relative_path}")


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Valida limites de caracteres dos artefatos de planejamento."
    )
    parser.add_argument("--root", required=True, type=Path)
    parser.add_argument("--file", action="append", dest="files", required=True, type=Path)
    parser.add_argument(
        "--limit",
        action="append",
        default=[],
        type=parse_limit,
        metavar="CAMINHO=LIMITE",
        help="Sobrescreve o limite de um arquivo especifico.",
    )
    args = parser.parse_args()

    root = args.root.resolve()
    overrides = {path: limit for path, limit in args.limit}
    failed = False

    for requested in args.files:
        relative_path = requested if not requested.is_absolute() else requested.relative_to(root)
        try:
            file_path = resolve_inside(root, relative_path)
            if not file_path.is_file():
                raise ValueError(f"Arquivo ausente: {relative_path}")
            limit = overrides.get(relative_path, default_limit(relative_path))
            size = len(file_path.read_text(encoding="utf-8").strip())
            state = "OK" if size <= limit else "EXCEDE"
            print(f"{state}: {relative_path} — {size}/{limit} caracteres")
            failed = failed or size > limit
        except (OSError, ValueError) as error:
            print(f"ERRO: {error}", file=sys.stderr)
            failed = True

    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
