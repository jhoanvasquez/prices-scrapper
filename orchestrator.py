import os
import subprocess
import sys

# Path to the virtual environment
VENV_PATH = os.path.join(os.path.dirname(__file__), "venv", "Scripts", "activate")

# Path to the scrapers folder
SCRAPER_FOLDER = os.path.join(os.path.dirname(__file__))

def run_scraper(script_name):
    """Run a scraper script within the virtual environment."""
    script_path = os.path.join(SCRAPER_FOLDER, script_name)

    # Command to activate the virtual environment and run the script
    command = f"{VENV_PATH} && python {script_path}"
    print(f"Running {script_name}...")

    result = subprocess.run(command, shell=True, capture_output=True, text=True)

    if result.returncode == 0:
        print(f"{script_name} ran successfully.")
    else:
        print(f"Error running {script_name}:")
        print(result.stderr)

def main():
    # List of scraper scripts to run
    scrapers = [
        "scrape_olimpica.py"
    ]

    # Run each scraper
    for scraper in scrapers:
        run_scraper(scraper)

if __name__ == "__main__":
    main()