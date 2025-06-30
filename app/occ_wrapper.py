"""Wrapper around the OCC (Open Camera Configurator) command line utility."""

from __future__ import annotations

import subprocess
from typing import Dict, List, Optional

# Location of the OCC binary on the system
OCC_BINARY = "/usr/bin/occ"

# Default timeout in seconds for OCC calls
DEFAULT_TIMEOUT = 5


class OCCError(Exception):
    """Raised when an OCC command fails."""


def _run_occ(args: List[str], timeout: int = DEFAULT_TIMEOUT) -> str:
    """Execute the OCC binary with the supplied arguments.

    Parameters
    ----------
    args : List[str]
        Arguments passed to the OCC binary.
    timeout : int, optional
        Time in seconds to wait for the command to finish.

    Returns
    -------
    str
        The standard output from the OCC command.

    Raises
    ------
    OCCError
        If the OCC binary is missing, times out or exits with a non-zero status.
    """

    cmd = [OCC_BINARY] + args
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


def list_cameras() -> List[str]:
    """Return a list of connected camera identifiers."""
    output = _run_occ(["list"])
    return [line.strip() for line in output.splitlines() if line.strip()]


def configure_camera(camera_id: str, *, codec: str, port: int) -> bool:
    """Configure a camera using OCC."""
    _run_occ(["configure", camera_id, "--codec", codec, "--port", str(port)])
    return True


def get_camera_config(camera_id: str) -> Optional[str]:
    """Return the configuration for *camera_id* or ``None`` if unavailable."""
    try:
        return _run_occ(["show", camera_id])
    except OCCError:
        return None


def reset_camera(camera_id: str) -> bool:
    """Reset *camera_id* to factory defaults."""
    _run_occ(["reset", camera_id])
    return True


def _parse_kv(text: str) -> Dict[str, str]:
    """Parse ``key=value`` output from OCC into a dictionary."""
    if "=" in text:
        key, value = text.split("=", 1)
        return {key.strip(): value.strip()}
    return {"output": text}


def read_parameter(parameter: str) -> Dict[str, str]:
    """Read a parameter from the camera."""
    output = _run_occ(["get", parameter])
    return _parse_kv(output)


def set_parameter(parameter: str, value: str) -> Dict[str, str]:
    """Set a parameter on the camera."""
    _run_occ(["set", parameter, str(value)])
    return {"status": "ok"}
