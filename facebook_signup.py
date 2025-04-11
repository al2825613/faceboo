
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import random
import string
import json
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

# إعداد المتصفح بدون واجهة GUI
options = Options()
options.add_argument("--headless")
options.add_argument("--disable-gpu")
options.add_argument("--no-sandbox")
driver = webdriver.Chrome(options=options)

# توليد بيانات الحساب
name = random_name()
password = random_password()
email = get_temp_email()
print("Email:", email)

# فتح فيسبوك
driver.get("https://mbasic.facebook.com/reg")

# ملء النموذج
time.sleep(2)
driver.find_element(By.NAME, "firstname").send_keys(name.split()[0])
driver.find_element(By.NAME, "lastname").send_keys(name.split()[1])
driver.find_element(By.NAME, "reg_email__").send_keys(email)
driver.find_element(By.NAME, "reg_passwd__").send_keys(password)
driver.find_element(By.NAME, "birthday_day").send_keys("1")
driver.find_element(By.NAME, "birthday_month").send_keys("1")
driver.find_element(By.NAME, "birthday_year").send_keys("2000")
driver.find_element(By.NAME, "sex").click()

# التالي
driver.find_element(By.NAME, "submit").click()
time.sleep(5)

# انتظار كود التفعيل
print("بانتظار كود التفعيل...")
tries = 0
code = ""
while tries < 10:
    out = message(EmailCheck=email, json_mode=True)
    try:
        data = json.loads(out)
        code = data.get("Code")
        if code:
            print("تم استلام الكود:", code)
            break
    except:
        pass
    tries += 1
    time.sleep(5)

# إدخال الكود (لو وصلك)
if code:
    try:
        input_box = driver.find_element(By.NAME, "code")
        input_box.send_keys(code)
        driver.find_element(By.NAME, "submit[Submit]").click()
        print("تم تفعيل الحساب.")
    except:
        print("لم يتم العثور على حقل الكود.")

# استخراج الكوكيز
cookies = driver.get_cookies()
c_user = next((c['value'] for c in cookies if c['name'] == 'c_user'), None)
xs = next((c['value'] for c in cookies if c['name'] == 'xs'), None)

if c_user and xs:
    print(f"كوكيز الحساب:
c_user={c_user}; xs={xs}")
else:
    print("فشل في استخراج الكوكيز.")

driver.quit()
