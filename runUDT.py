import pytest
import sys


def run_tests():
    # 1. Define where the tests are located
    # This points to your specific test file or folder
    test_path = "tests/test_puke_domains.py"

    # 2. Define where the report should be saved
    # The WeTest plugin looks for this file!
    report_file = "result.xml"

    print(f"--- Starting UDT Test Execution: {test_path} ---")

    # 3. Run pytest programmatically
    # -v: verbose output
    # --junitxml: creates the report file the plugin needs
    exit_code = pytest.main([
        "-v",
        f"--junitxml={report_file}",
        test_path
    ])

    print(f"--- Tests Finished with exit code: {exit_code} ---")

    # Exit with the same code pytest gave (0 for success, 1+ for failure)
    sys.exit(exit_code)


if __name__ == "__main__":
    run_tests()
