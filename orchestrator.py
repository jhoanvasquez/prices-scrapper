import os
import subprocess
import sys

VENV_PATH = os.path.join(os.path.dirname(__file__), "venv")

SCRAPER_FOLDER = os.path.dirname(__file__)

def get_activate_command():
    """Get the correct command to activate the virtual environment based on OS."""
    if os.name == "nt":  # Windows
        return os.path.join(VENV_PATH, "Scripts", "activate")
    else:  # Unix/Linux/Mac
        return f"source {os.path.join(VENV_PATH, 'bin', 'activate')}"

def run_scraper(script_name):
    """Run a scraper script within the virtual environment."""
    script_path = os.path.join(SCRAPER_FOLDER, script_name)

    activate_command = get_activate_command()

    command = f"{activate_command} && python {script_path}"
    print(f"Running {script_name}...")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{script_name} ran successfully.")
    else:
        print(f"Error running {script_name}:")
        print(result.stderr)

def main():
    scrapers = [
        "scrape_olimpica.py"
    ]

    for scraper in scrapers:
        run_scraper(scraper)

if __name__ == "__main__":
    main()