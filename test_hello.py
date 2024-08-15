import io
import sys
from main import main


def test_main():
    # Capture the output of the main function
    captured_output = io.StringIO()  # Create StringIO object
    sys.stdout = captured_output  # Redirect stdout to the StringIO object
    main()  # Call the function
    sys.stdout = sys.__stdout__  # Reset redirect to the original stdout

    # Check if the output is as expected
    assert "Main" in captured_output.getvalue(), "Test failed: 'Main' was not printed"


# Call the test function
if __name__ == "__main__":
    test_main()
    print("Test passed!")
