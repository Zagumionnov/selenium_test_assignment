import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # noqa
from selenium.webdriver.common.keys import Keys

product = 'OnePlus 8T'
color = 'green'

browser = webdriver.Chrome()


def test_shopping(driver):
    amazon_price = 0
    bestbuy_price = 0

    try:
        driver.get('https://www.amazon.com/')

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//input[@id='twotabsearchtextbox']"
        )))
        elem = driver.find_element(By.XPATH, "//input[@id='twotabsearchtextbox']")
        elem.send_keys(product)
        elem.send_keys(Keys.RETURN)

        try:
            WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
                By.XPATH, "//*[@id='p_n_feature_two_browse-bin-title']/span"
            )))
            driver.find_element(
                By.XPATH,
                f"//*[@id='filters']/ul/li/span/a[@title='{color.capitalize()}']/span/div"
            ).click()
        except Exception as ex:
            print(ex)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='a-autoid-0-announce']"
        )))
        driver.find_element(By.XPATH, "//*[@id='a-autoid-0-announce']").click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='s-result-sort-select_3']"
        )))
        driver.find_element(By.XPATH, "//*[@id='s-result-sort-select_3']").click()

        driver.find_element(
            By.XPATH, f"//a/span[contains(text(),'{product}')]"
        ).click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='corePrice_desktop']/div/table/tbody/tr/td[2]/span[1]/span[2]"
        )))
        price = driver.find_element(
            By.XPATH, "//*[@id='corePrice_desktop']/div/table/tbody/tr/td[2]/span[1]/span[2]"
        ).text
        amazon_price = float(price.lstrip('$'))

        driver.get('https://www.bestbuy.com/')
        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//a[2]/img"
        )))
        driver.find_element(By.XPATH, "//a[2]/img").click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='widgets-view-email-modal-mount']/div/div/div[1]/div/div/div/div/button"
        )))
        driver.find_element(By.XPATH, "//*[@id='widgets-view-email-modal-mount']/div/div/div[1]/div/div/div/div/button").click()

        time.sleep(5)
        elem = driver.find_element(By.XPATH, "//*[@id='gh-search-input']")
        elem.send_keys(product)
        elem.send_keys(Keys.RETURN)

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='main-filters']/div[3]/div[2]/section[8]"
        )))
        driver.find_element(
                By.XPATH, f"//li/div/div/div/label/span[1]/a/span[contains(text(),'{color.capitalize()}')]"
        ).click()

        WebDriverWait(driver, 10).until(EC.visibility_of_element_located((
            By.XPATH, "//*[@id='sort-by-select']"
        )))
        driver.find_element(By.XPATH, "//*[@id='sort-by-select']").click()
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
    test_shopping(browser)
