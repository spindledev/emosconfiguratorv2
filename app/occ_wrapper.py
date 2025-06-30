"""Wrapper functions for invoking the OCC command-line utility."""
from __future__ import annotations

import subprocess
from typing import Dict, List

class OCCError(Exception):
    """Raised when the OCC command fails."""


def _run_occ(args: List[str], timeout: int = 5) -> str:
    """Run an OCC command and return its stdout.

    Parameters
    ----------
    args: List[str]
        Arguments passed to the ``occ`` binary.
    timeout: int
        Maximum time in seconds to wait for the command.

    Returns
    -------
    str
        The command's standard output.

    Raises
    ------
    OCCError
        If the command could not be executed or exited with a non-zero status.
    """
    cmd = ["occ"] + args
    try:
        completed = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=False,
        )
    except FileNotFoundError as exc:
        raise OCCError("OCC binary not found") from exc
    except subprocess.TimeoutExpired as exc:
        raise OCCError("OCC command timed out") from exc

    if completed.returncode != 0:
        stderr = completed.stderr.strip()
        raise OCCError(stderr or "OCC command failed")

    return completed.stdout.strip()


def _parse_kv(text: str) -> Dict[str, str]:
    """Parse ``key=value`` pairs from OCC output."""
    if "=" in text:
        key, value = text.split("=", 1)
        return {key.strip(): value.strip()}
    return {"output": text}


def read_parameter(parameter: str) -> Dict[str, str]:
    """Read a parameter from the camera using OCC."""
    output = _run_occ(["get", parameter])
    return _parse_kv(output)


def set_parameter(parameter: str, value: str) -> Dict[str, str]:
    """Set a camera parameter using OCC."""
    _run_occ(["set", parameter, str(value)])
    return {"status": "ok"}
=======
# Wrapper around OCC binary
