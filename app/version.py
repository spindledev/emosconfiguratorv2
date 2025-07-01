"""Utilities for checking and updating the local version from GitHub."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Optional

import requests

# Path to the VERSION file in the repository root
VERSION_FILE = Path(__file__).resolve().parent.parent / "VERSION"

# Environment variable pointing to the GitHub repository, e.g. "user/repo"
GITHUB_REPO = os.environ.get("GITHUB_REPO")


def get_local_version() -> str:
    """Return the version string stored locally."""
    if VERSION_FILE.exists():
        return VERSION_FILE.read_text().strip()
    return "0.0.0"


def get_remote_version(repo: Optional[str] = None, timeout: int = 5) -> Optional[str]:
    """Return the latest release tag from GitHub.

    Parameters
    ----------
    repo : str, optional
        Repository in the form ``"owner/repo"``. If omitted, ``GITHUB_REPO`` is
        used. If that is also missing, ``None`` is returned.
    timeout : int, optional
        Timeout for the HTTP request in seconds.
    """
    repo = repo or GITHUB_REPO
    if not repo:
        return None

    url = f"https://api.github.com/repos/{repo}/releases/latest"
    try:
        response = requests.get(url, timeout=timeout)
        if response.status_code == 200:
            data = response.json()
            return data.get("tag_name")
    except requests.RequestException:
        pass
    return None


def update_available(local_version: Optional[str] = None, repo: Optional[str] = None) -> bool:
    """Return ``True`` if a newer version is available on GitHub."""
    local_version = local_version or get_local_version()
    remote_version = get_remote_version(repo=repo)
    if remote_version is None:
        return False
    return local_version != remote_version


def write_local_version(new_version: str) -> None:
    """Overwrite the local version file with *new_version*."""
    VERSION_FILE.write_text(new_version.strip() + "\n")
