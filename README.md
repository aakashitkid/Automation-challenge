## How to Run This Project from GitHub

Follow these steps to set up and run the assignments after cloning this repository:

1. **Clone the repository**
   ```sh
   git clone https://github.com/your-username/your-repo-name.git
   cd your-repo-name
   ```

2. **Create and activate a virtual environment**
   ```sh
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install Python dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Install Playwright browsers**
   ```sh
   playwright install
   ```

5. **Run Assignment 1**
   ```sh
   pytest -s tests/assignment1.py
   ```

6. **Run Assignment 2**
   ```sh
   pytest -s tests/assignment2.py
   ```

---



You can also use Docker for a fully containerized setup.

## Running with Docker

1. **Build the Docker image**
   ```sh
   docker build -t qa-automation-challenge .
   ```

2. **Run Assignment 1**
   ```sh
   docker run --rm -it qa-automation-challenge pytest -s tests/assignment1.py
   ```

3. **Run Assignment 2**
   ```sh
   docker run --rm -it qa-automation-challenge pytest -s tests/assignment2.py
   ```

- The Dockerfile installs all dependencies and Playwright browsers.
- You can override the default command to run any test file as shown above.

---



## Headless mode (important)

The test runner respects the `HEADLESS` environment variable so you can control whether Playwright launches a visible browser window or runs in headless mode.

- Default behaviour:
  - Locally (when you clone and run the tests) the default is `HEADLESS=0` (headed) so you can see the browser UI.
  - Inside the Docker image the `Dockerfile` sets `ENV HEADLESS=1`, so containerized runs are headless by default.

- Run headed locally (show browser UI)
```bash
# headed run (explicit)
export HEADLESS=0
pytest -s tests/assignment1.py
pytest -s tests/assignment2.py
```

- Run headless locally
```bash
export HEADLESS=1
pytest -s tests/assignment1.py
pytest -s tests/assignment2.py
```

- Override Docker default to run headless explicitly (default) or headed (advanced)
```bash
# Default (headless inside container)
docker run --rm -it qa-automation-challenge pytest -s tests/assignment1.py

# Force headless inside container explicitly
docker run --rm -e HEADLESS=1 -it qa-automation-challenge pytest -s tests/assignment1.py


---



## Notes
- Requires Python 3.9+ and Playwright.
- All automation code is in the `pages/` and `tests/` folders.
