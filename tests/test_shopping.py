from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # noqa


def test_shopping(driver):
    """Finds the price of an item of a specific color and with
    the most reviews on two different sites.

    :param driver: arg1
    :type driver: WebDriver

    :return: None
    """

    product = 'OnePlus 8T'
    color = 'Green'
    amazon_price = 0
    bestbuy_price = 100

    try:
        driver.get('https://www.amazon.com/')
        search_box = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//input[@id='twotabsearchtextbox']"
        )))
        search_box.send_keys(product, Keys.RETURN)

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
                By.XPATH,
                f"//*[@id='filters']/ul/li/span/a[@title='{color.capitalize()}']/span/div"
            ))).click()
        except Exception:
            raise Exception('This color does not exist')

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='a-autoid-0-announce']"
        ))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='s-result-sort-select_3']"
        ))).click()

        try:
            driver.find_element(By.XPATH, f"//a/span[contains(text(),'{product}')]").click()
        except Exception:
            raise Exception('Product not found')

        price = WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='corePrice_desktop']/div/table/tbody/tr/td[2]/span[1]/span[2]"
        ))).text
        amazon_price = float(price.lstrip('$'))

        driver.get('https://www.bestbuy.com/')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.XPATH, "//a[2]/img"))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='widgets-view-email-modal-mount']/div/div/div[1]/div/div/div/div/button"
        ))).click()

        WebDriverWait(driver, 10).until(EC.presence_of_element_located((
            By.XPATH, "//*[@id='gh-search-input']"
        ))).click()
        search_box = driver.find_element(By.XPATH, "//*[@id='gh-search-input']")
        search_box.send_keys(product)
        search_box.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, f"//li/div/div/div/label/span[1]/a/span[contains(text(),'{color.capitalize()}')]"
        ))).click()
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='sort-by-select']"
        ))).click()
        driver.find_element(By.XPATH, "//*[@id='sort-by-select']/option[5]").click()
        price = driver.find_element(
                By.XPATH, "//div[@class='priceView-hero-price priceView-customer-price']/span[1]"
            ).text
        bestbuy_price = float(price.lstrip('$'))

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()

    assert amazon_price > bestbuy_price


if __name__ == '__main__':
    test_shopping(webdriver.Chrome())
