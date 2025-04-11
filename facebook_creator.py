import random
import string
import json
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from iraq import gen, message

def random_name():
    first = random.choice(["Ahmed", "Ali", "Mohamed", "Sara", "Laila", "Hassan"])
    last = random.choice(["Salem", "Mostafa", "Ibrahim", "Omar", "Yousef", "Nasser"])
    return f"{first} {last}"

def random_password(length=10):
    chars = string.ascii_letters + string.digits + "@#*"
    return ''.join(random.choice(chars) for _ in range(length))

def get_temp_email():
    output = gen(EmailType=1, json_mode=True)
    data = json.loads(output)
    return data.get("email")

def create_facebook_account():
    options = Options()
    options.add_argument("--headless")
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    driver = webdriver.Chrome(options=options)

    name = random_name()
    password = random_password()
    email = get_temp_email()

    driver.get("https://mbasic.facebook.com/reg")
    time.sleep(2)

    driver.find_element(By.NAME, "firstname").send_keys(name.split()[0])
    driver.find_element(By.NAME, "lastname").send_keys(name.split()[1])
    driver.find_element(By.NAME, "reg_email__").send_keys(email)
    driver.find_element(By.NAME, "reg_passwd__").send_keys(password)
    driver.find_element(By.NAME, "birthday_day").send_keys("1")
    driver.find_element(By.NAME, "birthday_month").send_keys("1")
    driver.find_element(By.NAME, "birthday_year").send_keys("2000")
    driver.find_element(By.NAME, "sex").click()
    driver.find_element(By.NAME, "submit").click()
    time.sleep(5)

    code = ""
    for _ in range(10):
        try:
            out = message(EmailCheck=email, json_mode=True)
            data = json.loads(out)
            code = data.get("Code")
            if code:
                break
        except:
            pass
        time.sleep(5)

    if code:
        try:
            input_box = driver.find_element(By.NAME, "code")
            input_box.send_keys(code)
            driver.find_element(By.NAME, "submit[Submit]").click()
        except:
            pass

    cookies = driver.get_cookies()
    c_user = next((c['value'] for c in cookies if c['name'] == 'c_user'), None)
    xs = next((c['value'] for c in cookies if c['name'] == 'xs'), None)

    driver.quit()

    return {
        'email': email,
        'password': password,
        'name': name,
        'c_user': c_user,
        'xs': xs
    }

# للتجربة المباشرة:
if __name__ == "__main__":
    acc = create_facebook_account()
    print("تم إنشاء الحساب:")
    print("الاسم:", acc['name'])
    print("البريد:", acc['email'])
    print("كلمة السر:", acc['password'])
    print("كوكيز:")
    print(f"c_user={acc['c_user']}; xs={acc['xs']};")
