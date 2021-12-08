import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC # noqa
from selenium.webdriver.common.keys import Keys

product = 'OnePlus 8T'  # Samsung Galaxy S21 Ultra
color = 'Green'

browser = webdriver.Chrome()


def test_shopping(driver):
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
        print(amazon_price, type(amazon_price))

    except Exception as ex:
        print(ex)
    finally:
        driver.close()
        driver.quit()


if __name__ == '__main__':
    test_shopping(browser)


    # assert amazon_price > bestbuy_price
