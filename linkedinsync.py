from selenium import webdriver
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup


def define_limit_page(driver, url):
    driver.get(url)
    time.sleep(5)

    last_height = driver.execute_script(
        "return document.body.scrollHeight")

    while True:
        driver.execute_script(
            "window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(2)
        new_height = driver.execute_script(
            "return document.body.scrollHeight")

        if new_height == last_height:
            break
        last_height = new_height

    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')

    ul = soup.find('ul', class_='artdeco-pagination__pages')

    print(ul)
    limit_page = ul.find_all('li')[-1].text
    return int(limit_page)


def connect_with_relations(driver, url):
    driver.get(url)
    time.sleep(5)
    page = driver.page_source
    soup = BeautifulSoup(page, 'html.parser')
    links = soup.find_all('li', class_='reusable-search__result-container')
    for link in links:
        try:
            wait = WebDriverWait(driver, 10)
            connect_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'Invitez')]")))
            connect_button.click()
            send_button = wait.until(EC.element_to_be_clickable(
                (By.XPATH, "//button[contains(@aria-label, 'Envoyer maintenant')]")))
            send_button.click()
            time.sleep(5)
        except:
            pass


def main():
    user_input = input(
        "Entrer le lien de la liste de relations d'un profil LinkedIn : ")
    user_login = input("Entrer votre login LinkedIn : ")
    user_password = input("Entrer votre mot de passe LinkedIn : ")
    driver = webdriver.Chrome()
    driver.get("https://linkedin.com/uas/login")
    time.sleep(5)
    username = driver.find_element(By.ID, "username")
    username.send_keys(user_login)
    password = driver.find_element(By.ID, "password")
    password.send_keys(user_password)
    driver.find_element(By.XPATH, "//button[@type='submit']").click()

    time.sleep(25)

    limit_page = define_limit_page(driver, user_input)

    for i in range(1, limit_page + 1):
        page_url = f"{user_input}&page={i}"
        connect_with_relations(driver, page_url)


main()
