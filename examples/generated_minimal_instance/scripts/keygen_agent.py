#!/usr/bin/env python3
"""Generate per-instance signing material for a protocol signer."""

from __future__ import annotations

import argparse
import base64
import json
import secrets
import sys
from pathlib import Path

try:
    from cryptography.hazmat.primitives import serialization
    from cryptography.hazmat.primitives.asymmetric import ed25519
except ImportError as exc:  # pragma: no cover - environment dependency
    raise SystemExit("ERROR: cryptography package is required") from exc


def slug(value: str) -> str:
    cleaned = "".join(ch.lower() if ch.isalnum() else "-" for ch in value.strip())
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    if not cleaned:
        raise ValueError("agent_id must contain at least one alphanumeric character")
    return cleaned


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate Ed25519 and HMAC keys for one signer.")
    parser.add_argument("--agent-id", required=True)
    parser.add_argument("--keyid", required=True)
    parser.add_argument("--root", default=".", help="Protocol instance root. Default: current directory.")
    parser.add_argument(
        "--secret-dir",
        default="protocol-secrets",
        help="Secret directory, relative to --root unless absolute. Default: protocol-secrets.",
    )
    parser.add_argument("--force", action="store_true", help="Overwrite existing key files.")
    parser.add_argument("--output", default="-", help="Portable public metadata JSON path, or '-' for stdout.")
    return parser.parse_args()


def resolve_secret_dir(root: Path, value: str) -> Path:
    allowed_root = (root / "protocol-secrets").resolve()
    path = Path(value)
    if not path.is_absolute():
        path = root / path
    resolved = path.resolve()
    if resolved != allowed_root and allowed_root not in resolved.parents:
        raise ValueError("--secret-dir must resolve under <root>/protocol-secrets")
    return resolved


def write_secret(path: Path, data: bytes, *, force: bool) -> None:
    if path.exists() and not force:
        raise FileExistsError(f"refusing to overwrite existing secret: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(data)


def public_key_text(private_key: ed25519.Ed25519PrivateKey) -> str:
    public_key = private_key.public_key()
    return public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo,
    ).decode("ascii")


def generate(args: argparse.Namespace) -> dict[str, object]:
    root = Path(args.root).resolve()
    agent_id = str(args.agent_id).strip()
    keyid = str(args.keyid).strip()
    if not agent_id:
        raise ValueError("agent_id is required")
    if not keyid:
        raise ValueError("keyid is required")
    secret_dir = resolve_secret_dir(root, args.secret_dir)
    name = slug(agent_id)
    private_path = secret_dir / f"{name}-ed25519-private.pem"
    hmac_path = secret_dir / f"{name}-eventauth.key"

    private_key = ed25519.Ed25519PrivateKey.generate()
    private_bytes = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption(),
    )
    hmac_secret = base64.urlsafe_b64encode(secrets.token_bytes(32)).rstrip(b"=") + b"\n"
    write_secret(private_path, private_bytes, force=args.force)
    write_secret(hmac_path, hmac_secret, force=args.force)
    return {
        "agent_id": agent_id,
        "keyid": keyid,
        "private_key_file": private_path.relative_to(root).as_posix()
        if private_path.is_relative_to(root)
        else str(private_path),
        "hmac_secret_file": hmac_path.relative_to(root).as_posix()
        if hmac_path.is_relative_to(root)
        else str(hmac_path),
        "public_key": public_key_text(private_key),
        "event_auth": {
            "key_id": f"{name}-hmac:v1",
            "secret_file": hmac_path.relative_to(root).as_posix() if hmac_path.is_relative_to(root) else str(hmac_path),
        },
    }


def main() -> int:
    args = parse_args()
    try:
        result = generate(args)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1
    text = json.dumps(result, indent=2, ensure_ascii=True, sort_keys=True) + "\n"
    if args.output == "-":
        print(text, end="")
    else:
        output = Path(args.output)
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(text, encoding="ascii", newline="\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
