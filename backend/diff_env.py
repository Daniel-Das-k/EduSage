import subprocess
import os
PATH_TO_ENV= r"C:\Users\fazil\OneDrive\Desktop\Projects\verbique\diffenv"
# Path to the alternate virtual environment's Python executable
ALT_ENV_PYTHON = os.path.join(PATH_TO_ENV, 'Scripts', 'python.exe')

# Flask app path
FLASK_APP_PATH = r"C:\Users\fazil\OneDrive\Desktop\Projects\verbique\backend\demo.py"

def run_flask_app():
    try:
        # Run Flask app with Python from the alternate virtual environment
        subprocess.run([ALT_ENV_PYTHON, FLASK_APP_PATH], check=True)
    except subprocess.CalledProcessError as e:
        print(f"Error running Flask app: {e}")

if __name__ == "__main__":
    run_flask_app()