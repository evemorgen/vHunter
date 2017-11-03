import platform
import subprocess

from utils import Config


def check_python():
    min_python = int(Config().min_python.replace(".", ""))
    cur_python = int(platform.python_version().replace(".", ""))
    if cur_python < min_python:
        raise SystemError(
            "Minimal version of Python to run vHunter is: {}, but used version is: {}"
            .format(min_python, cur_python)
        )


def detect_distro():
    config = Config()
    distro_dict = {
        'mac_os': platform.mac_ver(),
        'linux': platform.linux_distribution(),
        'windows': platform.win32_ver(),
        'java': platform.java_ver()
    }
    for dist, ver in distro_dict.items():
        if ver[0] != '' and dist not in config.supported_platforms:
            raise SystemError(
                "The OS you are currently using ({}) is not supported yet"
                .format(dist)
            )
        elif ver[0] != '' and dist in config.supported_platforms:
            return {'distro': dist, 'version': ver}

    #  grepped_distros = subprocess.run(config.fallback_distro_command, shell=True)
    #  print(grepped_distros.stdout)
