import time
import webbrowser as web
import pyautogui as pg
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from PIL import Image
from selenium.webdriver.common.by import By
from io import BytesIO
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def gen_qr_code(driver):
    "Получает QR-код"
    driver.get("https://web.whatsapp.com/")
    # скриншот элемента страницы с QR-кодом
    qr_element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, "canvas[aria-label='Scan me!']"))
    )
    location = qr_element.location
    size = qr_element.size
    png = driver.get_screenshot_as_png()
    im = Image.open(BytesIO(png))  # создание PIL Image из байтов png-изображения
    left = location['x'] - 20
    top = location['y'] - 20
    right = location['x'] + size['width'] + 20
    bottom = location['y'] + size['height'] + 20
    im = im.crop((left, top, right, bottom))  # обрезка изображения по размерам элемента

    # сохранение изображения в файл
    im.save('qr_code.png')


def is_this_number_reg(driver):
    try:
        wrong_phone_div = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, ".f8jlpxt4 iuhl9who"))
        )
        if wrong_phone_div.text == "Неверный номер телефона.":
            return False
    except:
        return True
    return True


def send_msg(driver, phone_no, text):
    print(phone_no)
    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".lhggkp7q.qq0sjtgm.ebjesfe0.jxacihee.tkdu00h0"))
    )
    message = text
    driver.get(f"https://web.whatsapp.com/send?phone={phone_no}&text={message}")
    # time.sleep(500000000)
    if is_this_number_reg(driver):
        send_button = driver.find_element(By.CSS_SELECTOR, ".tvf2evcx.oq44ahr5.lb5m6g5c.svlsagor.p2rjqpw5.epia9gcq")
        send_button.click()
    else:
        print("Нет такого номера")


def is_login(driver):
    try:
        driver.find_element(By.CSS_SELECTOR, "._64p9P")
        return True
    except:
        return False


def login(driver):
    gen_qr_code(driver)
    count_attempt = 0
    max_attempt = 15
    sleep_time = 5
    while not is_login(driver) and count_attempt < max_attempt:
        time.sleep(sleep_time)
        count_attempt += 1

    if count_attempt < max_attempt:
        return True
    else:
        return False


def main():
    options = Options()
    driver = webdriver.Chrome(options=options)
    if login(driver):
        print("Вы успешно вошли")
        text = open("text.txt").read()
        f = open("base_of_numbers.txt")
        for number in f.readlines():
            send_msg(driver, number, text)
        # здесь непосредственно рассылка сообщений
    else:
        print("Войти не удалось")


if __name__ == "__main__":
    main()
