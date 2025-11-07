import subprocess


def run_adb_command(command):
    """
    Runs an ADB command and returns its output and any errors.
    """
    # The command needs to be split into a list for subprocess
    # e.g., "adb shell dumpsys display"
    adb_command = command.split()

    try:
        result = subprocess.run(
            adb_command,
            capture_output=True,  # Captures stdout and stderr
            text=True,  # Decodes output as text (UTF-8)
            check=True  # Raises an error if the command fails
        )

        # Return the standard output
        return result.stdout.strip()

    except subprocess.CalledProcessError as e:
        # Handle cases where the adb command itself fails
        print(f"Error running command: {command}")
        print(f"Return code: {e.returncode}")
        print(f"Output (stderr): {e.stderr.strip()}")
        return None
    except FileNotFoundError:
        # Handle case where adb is not in the system PATH
        print("Error: 'adb' command not found.")
        print("Please ensure ADB is installed and in your system's PATH.")
        return None


def adb_type_text(text_to_type):
    """
    Types the given string using 'adb shell input text'.
    Replaces spaces with '%s' as required by the adb command.
    """
    # Replace spaces with %s for the adb command
    formatted_text = text_to_type.replace(" ", "%s")

    # Run the command
    command = f"adb shell input text \"{formatted_text}\""
    try:
        subprocess.run(command, shell=True, check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error while typing: {e}")
    except FileNotFoundError:
        print("Error: 'adb' command not found. Is it in your system's PATH?")


def adb_press_enter():
    """
    Simulates pressing the 'Enter' key.
    """
    try:
        subprocess.run("adb shell input keyevent 66", shell=True, check=True)
    except Exception as e:
        print(f"Error pressing Enter: {e}")