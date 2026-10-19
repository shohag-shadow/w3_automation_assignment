import pytest
from playwright.sync_api import sync_playwright
from pathlib import Path
import shutil

@pytest.fixture(scope="session", autouse=True)
def prepare_artifact_dirs():
    for d in ("test-results", "allure-results", "screenshots", "videos", "traces"):
        Path(d).mkdir(exist_ok=True)
    yield


@pytest.fixture(scope="function", autouse=True)
def copy_playwright_artifacts(request):
    yield
    # After each test, copy Playwright's per-test output into category folders.
    # Playwright writes to test-results/<test-name>/ by default.
    node_name = request.node.name
    src = Path("test-results") / node_name
    if not src.exists():
        return

    for sub in src.iterdir():
        if sub.suffix == ".png":
            dest = Path("screenshots") / f"{node_name}.png"
        elif sub.suffix == ".webm":
            dest = Path("videos") / f"{node_name}.webm"
        elif sub.suffix == ".zip" and "trace" in sub.name.lower():
            dest = Path("traces") / f"{node_name}.zip"
        else:
            continue
        if not dest.exists():
            shutil.copy2(sub, dest)