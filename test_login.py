from playwright.sync_api import Page, expect

BASE_URL = "https://www.saucedemo.com"
INVENTORY_URL = f"{BASE_URL}/inventory.html"
CART_URL = f"{BASE_URL}/cart.html"
USERNAME = "standard_user"
PASSWORD = "secret_sauce"
PRODUCT_NAME = "Sauce Labs Backpack"


def submit_login(page: Page, password: str = PASSWORD) -> None:
    page.goto(BASE_URL)
    page.get_by_test_id("username").fill(USERNAME)
    page.get_by_test_id("password").fill(password)
    page.get_by_test_id("login-button").click()


def add_backpack(page: Page) -> None:
    submit_login(page)
    expect(page.get_by_test_id("inventory-container")).to_be_visible()
    page.get_by_test_id("add-to-cart-sauce-labs-backpack").click()


def test_login_page_is_displayed(page: Page):
    page.goto(BASE_URL)
    expect(page.get_by_test_id("username")).to_be_visible()
    expect(page.get_by_test_id("password")).to_be_visible()
    expect(page.get_by_test_id("login-button")).to_be_visible()


def test_successful_login(page: Page):
    submit_login(page)
    expect(page).to_have_url(INVENTORY_URL)
    expect(page.get_by_test_id("inventory-container")).to_be_visible()


def test_catalog_and_cart_badge(page: Page):
    add_backpack(page)
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")


def test_add_product_to_cart(page: Page):
    add_backpack(page)
    expect(page.get_by_test_id("shopping-cart-badge")).to_have_text("1")
    page.get_by_test_id("shopping-cart-link").click()
    expect(page).to_have_url(CART_URL)
    cart_item = page.get_by_test_id("inventory-item")
    expect(cart_item).to_have_count(1)
    expect(cart_item.get_by_test_id("inventory-item-name")).to_have_text(PRODUCT_NAME)
    expect(cart_item.get_by_test_id("item-quantity")).to_have_text("1")


def test_login_with_invalid_password(page: Page):
    submit_login(page, "wrong_password")
    error = page.get_by_test_id("error")
    expect(error).to_be_visible()
    expect(error).to_contain_text("Username and password do not match")
    expect(page).to_have_url(f"{BASE_URL}/")
    expect(page.get_by_test_id("inventory-container")).to_have_count(0)
