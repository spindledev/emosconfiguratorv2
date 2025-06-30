"""OCC (Open Camera Configurator) wrapper.

This module provides a thin interface around the OCC command line binary which
is used to configure EMOS cameras.  The real OCC tool is not part of this
repository; instead this file documents how the web application is expected to
interact with it.

Every helper function simply calls the OCC binary using :mod:`subprocess`.  All
output is returned verbatim and no parsing is performed.  The real OCC tool may
have a slightly different command line interface; these functions serve as
placeholders until the actual interface is finalised.
"""

from __future__ import annotations

import subprocess
from typing import List, Optional

# Path to the OCC binary.  This may need to be adjusted depending on the
# installation location on the target system.
OCC_BINARY = "/usr/bin/occ"

# Default timeout (in seconds) used for subprocess calls.
DEFAULT_TIMEOUT = 5


def _run(*args: str, timeout: int = DEFAULT_TIMEOUT) -> subprocess.CompletedProcess:
    """Run the OCC binary with the provided arguments.

    Parameters
    ----------
    *args : str
        Arguments to pass to the OCC binary.
    timeout : int, optional
        Timeout for the subprocess call.  Defaults to ``DEFAULT_TIMEOUT``.

    Returns
    -------
    subprocess.CompletedProcess
        The object returned by :func:`subprocess.run`.

    Raises
    ------
    RuntimeError
        If the OCC process exits with a non-zero status code or cannot be
        executed.
    """
    cmd = [OCC_BINARY, *args]
    try:
        result = subprocess.run(
          
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

    except Exception as exc:  # pragma: no cover - purely defensive
        raise RuntimeError(f"Failed to run OCC binary: {exc}") from exc

    if result.returncode != 0:
        raise RuntimeError(
            f"OCC command {' '.join(cmd)} failed: {result.stderr.strip()}"
        )
    return result


def list_cameras() -> List[str]:
    """Return a list of camera identifiers.

    The OCC binary is expected to support a ``list`` subcommand that outputs one
    camera ID per line.  The function simply splits the output on newlines and
    returns a list.  If no cameras are connected an empty list is returned.
    """
    proc = _run("list")
    return [line.strip() for line in proc.stdout.splitlines() if line.strip()]


def configure_camera(camera_id: str, *, codec: str, port: int) -> bool:
    """Configure a camera via OCC.

    Parameters
    ----------
    camera_id : str
        Identifier returned by :func:`list_cameras`.
    codec : str
        Desired video codec (e.g. ``"MJPEG"`` or ``"H264"``).
    port : int
        Streaming or multicast port.

    Returns
    -------
    bool
        ``True`` when the command completed without error.

    Notes
    -----
    The underlying OCC tool is assumed to accept a ``configure`` subcommand in
    the form ``occ configure <id> --codec <codec> --port <port>``.  Adjust this
    wrapper once the real command line interface is known.
    """
    _run("configure", camera_id, "--codec", codec, "--port", str(port))
    return True


def get_camera_config(camera_id: str) -> Optional[str]:
    """Retrieve the configuration for a specific camera.

    OCC is expected to return a textual representation of the configuration
    when invoked as ``occ show <id>``.  This function returns the raw text or
    ``None`` if the command fails.
    """
    try:
        proc = _run("show", camera_id)
    except RuntimeError:
        return None
    return proc.stdout


def reset_camera(camera_id: str) -> bool:
    """Reset a camera to factory defaults.

    This placeholder assumes a ``reset`` subcommand in OCC.  It returns ``True``
    if the command succeeds.
    """
    _run("reset", camera_id)
    return True


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

# Wrapper around OCC binary

