import time
import webbrowser as web
import pyautogui as pg
f = open("base_of_numbers.txt")
f1 = open("text.txt", encoding="utf-8")
text = f1.read()
print(text)
for phone_no in f:
      message = text
      web.open(f"https://web.whatsapp.com/send?phone={phone_no}&text={message}")
      time.sleep(15)
      pg.click(1500,600)
      pg.press("enter")
      time.sleep(5)
      pg.hotkey('ctrl', 'w')
      time.sleep(3)


