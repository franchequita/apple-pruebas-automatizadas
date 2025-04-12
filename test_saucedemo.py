import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import os
from datetime import datetime

@pytest.fixture
def driver(request):
    driver = webdriver.Safari()
    driver.maximize_window()
    driver.get("https://www.saucedemo.com/")
    
    yield driver

    # Tomar screenshot después de cada prueba
    test_name = request.node.name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    # Guardar la captura en el directorio actual sin ninguna carpeta
    screenshot_name = f"{test_name}_{timestamp}.png"
    driver.save_screenshot(screenshot_name)
    
    driver.quit()

def test_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    assert "inventory" in driver.current_url

def test_failed_login(driver):
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("wrong_password")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    error = driver.find_element(By.XPATH, "//h3[@data-test='error']")
    assert "Epic sadface" in error.text

def test_add_to_cart(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    time.sleep(2)
    assert "sauce-labs-backpack" in driver.page_source

def test_remove_from_cart(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "remove-sauce-labs-backpack").click()
    time.sleep(2)
    assert "Your Cart" in driver.page_source

def test_checkout(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    driver.find_element(By.ID, "add-to-cart-sauce-labs-backpack").click()
    driver.find_element(By.CLASS_NAME, "shopping_cart_link").click()
    driver.find_element(By.ID, "checkout").click()
    driver.find_element(By.ID, "first-name").send_keys("Test")
    driver.find_element(By.ID, "last-name").send_keys("User")
    driver.find_element(By.ID, "postal-code").send_keys("12345")
    driver.find_element(By.ID, "continue").click()
    driver.find_element(By.ID, "finish").click()
    time.sleep(2)
    assert "Thank you for your order!" in driver.page_source

def test_logout(driver):
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()
    time.sleep(2)
    driver.find_element(By.ID, "react-burger-menu-btn").click()
    time.sleep(1)
    driver.find_element(By.ID, "logout_sidebar_link").click()
    time.sleep(2)
    assert "saucedemo.com" in driver.current_url
