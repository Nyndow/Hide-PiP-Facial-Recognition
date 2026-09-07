import subprocess


def hide_pip():
    result = subprocess.run(
        ["wmctrl", "-l"],
        capture_output=True,
        text=True
    )

    for line in result.stdout.splitlines():
        if "Picture-in-Picture" in line:
            result = subprocess.run([
                "wmctrl",
                "-r",
                "Picture-in-Picture",
                "-b",
                "add,hidden"
            ])

            return result.returncode == 0

    return False
