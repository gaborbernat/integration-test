import subprocess


def test_can_create(venv, tmp_path, versions):
    print(versions)
    subprocess.check_call([venv.exe, "-m", "pip", "install", "virtualenv"])
    subprocess.check_call([venv.exe, "-m", "virtualenv", str(tmp_path)])
