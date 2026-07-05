from __future__ import annotations

import base64
import json
import os
import platform
from pathlib import Path
from typing import Any


class SecretsStore:
    """Stores provider secrets locally.

    On Windows this attempts to use DPAPI via ctypes. On non-Windows systems it
    falls back to a local file with restrictive permissions. This is not equal to
    a full credential manager, but it keeps secrets out of source files and logs.
    """

    def __init__(self, root: Path) -> None:
        self.path = root / "storage" / "secrets" / "provider_secrets.json"
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self.path.write_text("{}", encoding="utf-8")
            try:
                os.chmod(self.path, 0o600)
            except OSError:
                pass

    def _encrypt(self, plaintext: str) -> str:
        if platform.system() != "Windows":
            return base64.b64encode(plaintext.encode("utf-8")).decode("ascii")
        try:
            import ctypes
            import ctypes.wintypes as wintypes

            crypt32 = ctypes.windll.crypt32
            kernel32 = ctypes.windll.kernel32

            class DATA_BLOB(ctypes.Structure):
                _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

            raw = plaintext.encode("utf-8")
            buffer = ctypes.create_string_buffer(raw, len(raw))
            in_blob = DATA_BLOB(len(raw), buffer)
            out_blob = DATA_BLOB()
            if not crypt32.CryptProtectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob)):
                raise OSError("CryptProtectData failed")
            try:
                data = ctypes.string_at(out_blob.pbData, out_blob.cbData)
                return base64.b64encode(data).decode("ascii")
            finally:
                kernel32.LocalFree(out_blob.pbData)
        except Exception:
            return base64.b64encode(plaintext.encode("utf-8")).decode("ascii")

    def _decrypt(self, payload: str) -> str:
        raw = base64.b64decode(payload.encode("ascii"))
        if platform.system() != "Windows":
            return raw.decode("utf-8")
        try:
            import ctypes
            import ctypes.wintypes as wintypes

            crypt32 = ctypes.windll.crypt32
            kernel32 = ctypes.windll.kernel32

            class DATA_BLOB(ctypes.Structure):
                _fields_ = [("cbData", wintypes.DWORD), ("pbData", ctypes.POINTER(ctypes.c_char))]

            buffer = ctypes.create_string_buffer(raw, len(raw))
            in_blob = DATA_BLOB(len(raw), buffer)
            out_blob = DATA_BLOB()
            if not crypt32.CryptUnprotectData(ctypes.byref(in_blob), None, None, None, None, 0, ctypes.byref(out_blob)):
                raise OSError("CryptUnprotectData failed")
            try:
                return ctypes.string_at(out_blob.pbData, out_blob.cbData).decode("utf-8")
            finally:
                kernel32.LocalFree(out_blob.pbData)
        except Exception:
            return raw.decode("utf-8")

    def set_secret(self, name: str, value: str) -> None:
        data = self.load_all()
        data[name] = self._encrypt(value)
        self.path.write_text(json.dumps(data, indent=2), encoding="utf-8")

    def get_secret(self, name: str) -> str:
        data = self.load_all()
        payload = data.get(name, "")
        if not payload:
            return ""
        return self._decrypt(payload)

    def load_all(self) -> dict[str, Any]:
        try:
            return json.loads(self.path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
