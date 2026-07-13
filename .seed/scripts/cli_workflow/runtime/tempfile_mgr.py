"""Auto temp files for workflow list inputs/outputs (S1)."""

from __future__ import annotations

import tempfile
from pathlib import Path
from typing import List, Optional


class TempFileManager:
    def __init__(self, *, prefix: str = "sf_wf_"):
        self.prefix = prefix
        self._paths: List[Path] = []

    def write_line_text(self, values: List[str], *, suffix: str = ".txt") -> Path:
        fh = tempfile.NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            prefix=self.prefix,
            suffix=suffix,
            delete=False,
        )
        try:
            for v in values:
                fh.write(f"{v}\n")
            fh.flush()
            path = Path(fh.name)
            self._paths.append(path)
            return path
        finally:
            fh.close()

    def allocate_output(self, *, suffix: str = ".out") -> Path:
        fh = tempfile.NamedTemporaryFile(
            prefix=self.prefix,
            suffix=suffix,
            delete=False,
        )
        fh.close()
        path = Path(fh.name)
        self._paths.append(path)
        return path

    def cleanup(self) -> None:
        for p in self._paths:
            try:
                p.unlink(missing_ok=True)
            except OSError:
                pass
        self._paths.clear()
