import pytest
import subprocess


@pytest.mark.login
def test_user_launch_chrome():
    pkg = "com.android.chrome"

    subprocess.run(["adb", "shell", "pm", "grant", pkg, "android.permission.ACCESS_FINE_LOCATION"])

    subprocess.run(["adb", "shell", f"echo 'chrome --no-first-run' > /data/local/chrome-command-line"])

    subprocess.run(["adb", "shell", "chmod", "777", "/data/local/chrome-command-line"])
    subprocess.run(["adb", "shell", "appops", "set", "com.android.chrome", "POST_NOTIFICATION", "ignore"])


    cmd = [
        "adb", "shell", "am", "start",
        "-n", "com.android.chrome/com.google.android.apps.chrome.Main",
        "--ez", "no-first-run", "true",
        "--ez", "skip-first-run-ui", "true",
        "--es", "args", "--disable-notifications",
        "-d", "about:blank"
    ]
    subprocess.run(cmd, check=True)
