from panel.server import *
from panel.ui.modules.first_time.first_time import MakeFiles

from nicegui.testing import Screen

from selenium.webdriver.common.by import By


def test_build_page(screen: Screen) -> None:
    @ui.page("/builder")
    def builder_page() -> None:
        """Builder page for the stealer."""
        with frame():
            builder()

    builder_page()

    # change screensize
    screen.selenium.set_window_size(1920, 1080)

    screen.open("/builder")
    screen.should_contain("Builder page")

    element = screen.selenium.find_element(
        By.XPATH, '//*[@aria-label="TCP TUNNEL URL:PORT"]'
    )

    assert element.get_attribute("type") == "text"

    element.send_keys("example.com:12345")

    assert element.get_attribute("value") == "example.com:12345"

    screen.click("Build")

    if os.path.exists("kdot.ps1"):
        os.remove("kdot.ps1")
        assert True


def test_settings_page(screen: Screen) -> None:
    @ui.page("/settings")
    def settings() -> None:
        """Settings page for the stealer. (NEEDS TO BE REWORKED OR ATLEAST A NEW UI LMFAO)"""
        with frame(True):
            settings_stuff()

    settings()

    screen.selenium.set_window_size(1920, 1080)

    screen.open("/settings")

    screen.should_contain("text")
    screen.should_contain("tree")
    screen.should_contain("table")


def test_clients_page(screen: Screen) -> None:
    @ui.page("/clients")
    async def clients_page() -> None:
        """Clients page for the stealer"""
        with frame(True):
            await clients_page_stuff(db_path)

    clients_page()

    screen.selenium.set_window_size(1920, 1080)

    screen.open("/clients")
    screen.should_contain("Clients page")


def test_make_files() -> None:
    files = MakeFiles()
    files.make_all()

    all_found = False
    methods = [
        files.get_appdir_directory(),
        files.get_SQLiteDB_path(),
        files.get_config_file_path(),
        files.get_logs_directory(),
        files.get_build_ids_file_path(),
        files.get_key_path(),
        files.get_cert_path(),
    ]

    for file_path in methods:
        if os.path.exists(file_path):
            all_found = True
        else:
            all_found = False
            break

    assert all_found == True