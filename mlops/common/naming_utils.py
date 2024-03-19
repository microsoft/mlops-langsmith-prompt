"""This module contains a few utility methods that allows us to initialize MLFlow and generate names for \
    for experiments and runs."""
import subprocess
import os
import uuid


def generate_run_name():
    """
    Generate a unique run name based on the current branch name.

    Returns:
        string: run name according to the pattern
    """
    git_branch = os.environ.get("BUILD_SOURCEBRANCHNAME")

    if git_branch is None:
        git_branch = subprocess.check_output(
            "git rev-parse --abbrev-ref HEAD", shell=True, universal_newlines=True
        ).strip()

    git_branch = git_branch.split("/")[-1]

    build = os.environ.get("BUILD_BUILDID")

    if build is None:
        build = f"local_{uuid.uuid4().hex}"

    return f"{git_branch}_{build}"
