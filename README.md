# Playwright Python Test Automation Suite

End-to-end browser tests for the Books to Scrape and Quotes to Scrape practice sites, written with Playwright, pytest, and Allure.

---

## Project Overview

This repository holds an automated UI test suite that drives a real Chromium browser against two public sandbox websites built for scraping and test practice:

- https://books.toscrape.com (an online bookstore catalog)
- https://quotes.toscrape.com (a quotes site with a login form)

The suite has six tests. They cover page load and layout checks, navigation to product detail pages, data consistency between listing and detail pages, link health, image integrity across paginated pages, and a login flow.

The tests run locally and in GitHub Actions. Every run produces a self-contained HTML report and Allure results. In CI the Allure report is also published to GitHub Pages.

## Features

- Six end-to-end tests covering navigation, content validation, link checking, pagination, and authentication.
- Randomized sampling of books in two tests, so different parts of the catalog get checked over time.
- A shared Playwright `page` fixture that gives every test a fresh browser context.
- Two report formats: a single-file pytest-html report and an Allure report.
- A GitHub Actions workflow that installs dependencies, runs the suite under a virtual display, builds the Allure report, uploads every artifact, and deploys the Allure report to GitHub Pages.
- Live log output in the terminal (`log_cli`) while tests run.
- Registered `smoke` and `regression` markers for grouping tests as the suite grows.

## Tech Stack

| Tool | Purpose |
| --- | --- |
| Python 3.10+ | Language (CI uses 3.12) |
| pytest | Test runner and fixtures |
| Playwright for Python | Browser automation (Chromium) |
| pytest-playwright | Playwright integration for pytest, provides the `Page` type and the `--slowmo`, `--screenshot`, `--video`, `--tracing` options |
| requests | HTTP calls used by the link checker test |
| pytest-html | Self-contained HTML report |
| allure-pytest | Writes Allure result files |
| Allure CLI | Turns Allure result files into a browsable report |
| GitHub Actions | Continuous integration |
| xvfb | Virtual display so the headed browser can run on the Linux CI runner |
| peaceiris/actions-gh-pages | Publishes the Allure report to GitHub Pages |

Python dependencies are listed in `requirements.txt`:

```
pytest
pytest-playwright
pytest-html
allure-pytest
requests
```

Pin exact versions (`pip freeze`) when you want reproducible installs.

## Installation Guide

### Prerequisites

- Python 3.10 or newer
- Git
- Node.js and npm (only needed to install the Allure CLI the same way CI does)
- Java 8 or newer (required by the Allure CLI)

### Steps

1. Clone the repository.

   ```bash
   git clone https://github.com/shohag-shadow/w3_automation_assignment.git
   cd w3_automation_assignment
   ```

2. Create and activate a virtual environment.

   ```bash
   python -m venv .venv

   # Linux / macOS
   source .venv/bin/activate

   # Windows (PowerShell)
   .venv\Scripts\Activate.ps1
   ```

3. Install the Python dependencies.

   ```bash
   pip install -r requirements.txt
   ```

4. Download the Chromium browser used by Playwright.

   ```bash
   python -m playwright install chromium
   ```

   On a fresh Linux machine, add the system libraries Chromium needs:

   ```bash
   python -m playwright install --with-deps chromium
   ```

5. Install the Allure CLI (needed only to build or open Allure reports locally).

   ```bash
   npm install -g allure-commandline
   ```

   Homebrew (`brew install allure`) and Scoop (`scoop install allure`) also work.

6. Check that everything is wired up.

   ```bash
   pytest --collect-only
   ```

   This should list six tests without opening a browser.


## Running Tests

Run these from the repository root with the virtual environment active.

```bash
# Whole suite
pytest

# One file
pytest tests/test_03.py

```

## Project Structure

```
.
├── .github/
│   └── workflows/
│       └── playwright.yml      # CI pipeline
├── tests/
│   ├── test_01.py              # Homepage baseline checks
│   ├── test_02.py              # Random book opens its detail page
│   ├── test_03.py              # Title and price match between pages
│   ├── test_04.py              # Homepage link health
│   ├── test_05.py              # Product image integrity across pages
│   └── test_06.py              # Login flow on Quotes to Scrape
├── conftest.py                 # Fixtures and artifact handling
├── pytest.ini                  # Runner configuration
├── requirements.txt            # Python dependencies
└── README.md
```

Generated at runtime (not committed):

| Folder | Contents |
| --- | --- |
| `test-results/` | `report.html` and Playwright per-test output |
| `allure-results/` | Raw Allure result files |
| `allure-report/` | Built Allure report (after `allure generate`) |
| `screenshots/` | Failure screenshots copied from `test-results` |
| `videos/` | Failure videos copied from `test-results` |
| `traces/` | Failure traces copied from `test-results` |

## Test Case Coverage

| Test | Site | What it verifies |
| --- | --- | --- |
| `test_01` | Books to Scrape | Homepage returns HTTP 200, the final URL is the requested one, the title is `All products \| Books to Scrape - Sandbox`, every h1 to h6 is visible and has text, and exactly one `section` element is present and visible |
| `test_02` | Books to Scrape | Homepage returns HTTP 200 and lists at least five books. Five random books are opened one at a time. Each detail page must show an h1 equal to the book title and a visible product information table. The test then goes back to the homepage |
| `test_03` | Books to Scrape | For five random books, the title on the homepage (trailing dots from truncation ignored) appears in the detail page h1, and the detail page price equals the homepage price |
| `test_04` | Books to Scrape | Every anchor on the homepage has a non-empty `href`, and every resolved URL answers HTTP 200 |
| `test_05` | Books to Scrape | Across up to five paginated pages, every product image is visible and has a non-empty `src`, a non-empty `alt`, and the `thumbnail` class |
| `test_06` | Quotes to Scrape | Login link is visible, leads to `/login`, credentials are typed with a delay, submit redirects to the homepage, and the Logout link is visible with `href="/logout"` |

### Details worth knowing

- `test_02` and `test_03` pick books with `random.sample`, so the books checked change from run to run.
- `test_02` reads the book title from the link's `title` attribute and falls back to the visible text if the attribute is empty.
- `test_04` uses a `requests.Session` outside the browser. It checks status codes only, not page content.
- `test_05` stops when the `next` link disappears or after five pages, whichever comes first.

## Report Generation Guide

Each run writes two kinds of output.

| Report | Written by | Location after a run | Extra step needed |
| --- | --- | --- | --- |
| HTML report | pytest-html | `test-results/report.html` | None |
| Allure results | allure-pytest | `allure-results/` | Build with the Allure CLI to get a readable report |

Typical local flow:

```bash
pytest --clean-alluredir                          # run tests, write both outputs
allure generate allure-results -o allure-report --clean
allure open allure-report                         # serve the built report
```

Or skip the build step and serve the results directly:

```bash
allure serve allure-results
```

Use `--clean-alluredir` (or delete `allure-results/` by hand) before a run. Allure appends new result files to the folder, so old runs would otherwise show up in the new report.

## HTML Report Guide

The HTML report is one file with its CSS and data embedded. You can open it by double-clicking, attach it to an email, or upload it anywhere.

**Location:** `test-results/report.html`

**Reading it:**

- The top of the page shows the environment, total duration, and counts for passed, failed, skipped, errors, and expected failures.
- The results table lists each test with its result, name, and duration. Click a row to expand it and see the captured log output and, for failures, the assertion message and traceback.
- The checkboxes in the summary filter the table by outcome. Clicking a column header sorts by it.

**Getting it from CI:** open the workflow run in the Actions tab, scroll to Artifacts, and download `html-report`. Unzip it and open `report.html`.

The file is overwritten on every run. Copy it elsewhere if you need to keep an older one.

## Allure Report Guide

### Building and opening locally

1. Run the tests so `allure-results/` exists.
2. Build the report:

   ```bash
   allure generate allure-results -o allure-report --clean
   ```

3. Open it:

   ```bash
   allure open allure-report
   ```

Opening `allure-report/index.html` directly from the file system usually shows a blank page, because the report loads its data over HTTP. Use `allure open` or `allure serve`.

### Reading the report

- **Overview:** pass rate, counts by status, and run duration.
- **Suites:** tests grouped by file, with steps, logs, and failure details for each.
- **Graphs:** status, severity, and duration charts.
- **Timeline:** when each test ran and how long it took.
- **Behaviors:** empty at the moment, because the tests do not use Allure labels such as `epic`, `feature`, or `story`.

### From CI

The workflow publishes the report to GitHub Pages at:

```
https://shohag-shadow.github.io/w3_automation_assignment/allure/
```

The same report is also attached to each run as the `allure-report` artifact, and the raw files as `allure-results`.

## GitHub Actions Setup

The workflow lives in `.github/workflows/playwright.yml` and is named **Playwright Tests**.

### Triggers

- Push to `main` or `master`
- Pull request targeting `main` or `master`

### Permissions

The workflow requests `contents: write` so it can push the Allure report to the `gh-pages` branch.

### What each step does

| Step | Purpose |
| --- | --- |
| Checkout | Gets the repository code |
| Set up Python 3.12 | Installs the interpreter |
| Install Python dependencies | Upgrades pip and installs `requirements.txt` |
| Install Playwright browsers | `playwright install --with-deps chromium` |
| Run tests | `xvfb-run -a pytest`, with `continue-on-error: true` |
| Install Allure CLI | `npm install -g allure-commandline` |
| Generate Allure report | Builds `allure-report/` from `allure-results/` if it exists |
| Upload artifacts | Seven uploads, listed below |
| Deploy to GitHub Pages | Publishes `allure-report/` to the `allure` folder of the `gh-pages` branch |

Every step after the test run uses `if: always()`, so reports are produced and published even when tests fail.

### Artifacts

| Artifact name | Contents |
| --- | --- |
| `html-report` | `test-results/report.html` |
| `allure-results` | Raw Allure files |
| `allure-report` | Built Allure report |
| `screenshots` | Files from `screenshots/` |
| `videos` | Files from `videos/` |
| `traces` | Files from `traces/` |
| `playwright-test-results` | Entire `test-results/` folder |

## Design Decisions

- **Custom `browser` and `page` fixtures.** `conftest.py` defines its own fixtures. One browser is started per session and a new context per test, so tests stay isolated without paying for a browser launch each time.
- **Headed browser everywhere.** The browser always runs headed so local runs and CI runs behave the same. The CI runner has no display, so the workflow wraps pytest in `xvfb-run`.
- **Two report formats.** The HTML report is a single file that is easy to share. The Allure report is better for browsing results and for hosting online.
- **Randomized book selection.** `test_02` and `test_03` sample five random books instead of always testing the same five. This widens coverage over many runs at the cost of run-to-run variation.
- **`requests` for link checking.** Checking status codes over HTTP is much faster than clicking through every link in the browser, and it reports the status code directly.
- **Plain test functions.** Locators sit inside the tests rather than in page objects. With six tests this keeps things easy to read. Move to page objects if the suite grows.
- **Locator choice.** Role-based locators (`get_by_role`) are used where the element has a clear role, and CSS selectors are used for site-specific structure such as `article.product_pod`.
- **Artifacts sorted by type.** `conftest.py` copies screenshots, videos, and traces into their own folders so CI can upload them as separate artifacts.
- **Reports always published.** Report and upload steps run with `if: always()` so a failing test never hides its own report.
- **Public sandbox sites.** Both sites exist for practice, are stable, and need no accounts or secrets.

## Known Limitations


- **Headless mode is not switchable from the command line.** It is hard-coded in `conftest.py`.
- **Depends on external websites.** The tests call live public sites. If a site is slow or down, tests fail for reasons unrelated to the code. There is no mocking or retry logic.
- **`test_04` is sequential.** It requests links one at a time, so it slows down as the number of links grows.
- **Markers are declared but unused.** `smoke` and `regression` are registered in `pytest.ini`, but no test is marked yet, so `pytest -m smoke` selects nothing.
- **Limited scope.** Only Chromium is used, tests run serially (no `pytest-xdist`), and URLs are hard-coded rather than configurable.
- **Login coverage is a happy path only.** `test_06` does not cover wrong credentials, empty fields, or logging out.