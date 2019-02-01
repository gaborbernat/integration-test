import json
import os
import subprocess
from collections import namedtuple
from distutils.version import StrictVersion
from pathlib import Path

import pytest
import requests


def version(package_name):
    """gets versions from pypi"""
    url = "https://pypi.python.org/pypi/{}/json".format(package_name)
    data = requests.get(url).json()
    return sorted(list(data["releases"].keys()), key=StrictVersion, reverse=True)


@pytest.fixture()
def versions():
    """inject master versions as env var"""
    version_dict = {}
    master_wheels_base = os.environ.get("MASTER_WHEELS")
    if master_wheels_base is None:
        return version_dict

    for path in Path(master_wheels_base).glob("wheel-/*.whl"):
        parts = path.name.split("-")
        pypi_lastest = version(parts[0])[0]
        version_dict[parts[0]] = (parts[1], pypi_lastest)
    return version_dict


Venv = namedtuple("Venv", ["path", "exe"])


@pytest.fixture()
def venv(tmp_path):
    subprocess.check_call(["python3.7", "-m", "venv", str(tmp_path)])
    yield Venv(tmp_path, tmp_path / "bin" / "python")
