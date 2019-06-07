import subprocess

def git_root():
    return subprocess.check_output(
        "git rev-parse --show-toplevel",
        shell=True).decode('utf-8').strip()
