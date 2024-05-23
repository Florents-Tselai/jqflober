import os
import sys
import sysconfig


def find_jq_bin() -> str:
    """Return the whisper binary path."""

    jq_exe = "jq" + sysconfig.get_config_var("EXE")

    path = os.path.join(sysconfig.get_path("scripts"), jq_exe)
    if os.path.isfile(path):
        return path

    if sys.version_info >= (3, 10):
        user_scheme = sysconfig.get_preferred_scheme("user")
    elif os.name == "nt":
        user_scheme = "nt_user"
    elif sys.platform == "darwin" and sys._framework:
        user_scheme = "osx_framework_user"
    else:
        user_scheme = "posix_user"

    path = os.path.join(sysconfig.get_path("scripts", scheme=user_scheme), jq_exe)
    if os.path.isfile(path):
        return path

    raise FileNotFoundError(path)


if __name__ == "__main__":
    jqflober = os.fsdecode(find_jq_bin())
    if sys.platform == "win32":
        import subprocess

        completed_process = subprocess.run([jqflober, *sys.argv[1:]])
        sys.exit(completed_process.returncode)
    else:
        os.execvp(jqflober, [jqflober, *sys.argv[1:]])
