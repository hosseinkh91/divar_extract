from selenium import webdriver
from mysql.connector import connect
from selenium.webdriver.common.by import By
from unidecode import unidecode
from random import randint
# import time

driver = webdriver.Firefox()
driver.maximize_window()  # For maximizing window
driver.implicitly_wait(20)  # Gives an implicit wait for 60 seconds
web_page = "https://divar.ir/s/tehran/car/peugeot/206/2?price=1-"
driver.get(web_page)

# i = 0
# while i < 5:
#     new_driver = driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
#     time.sleep(3)
#     i = i+1

"""
This is Divar's Dom

        <div class="post-card-item kt-col-6 kt-col-xxl-4">
            <a class="kt-post-card kt-post-card--outlined" href="/v/پژو-206-تیپ-۲-مدل-۱۳۹۷_سواری-و-وانت_تهران_رباط-کریم_دیوار/gY-YC3An">
            </a>
        </div>
"""


div_XPath = '//div[@class="post-card-item kt-col-6 kt-col-xxl-4"]'
search_all_divs = driver.find_elements(by=By.XPATH, value=div_XPath)
cars_link = []

for element in search_all_divs:
    find_a = element.find_element(by=By.TAG_NAME, value='a')
    href_value = find_a.get_attribute('href')
    cars_link.append(href_value)
print(len(cars_link))
# Now we have a list named cars_link and in this list we have every links of cars for extract data such as price and mileage from them

all_cars = []  # this list will include some other lists that have price, model and mileage
print('Extracting data from', web_page)
print('wait a couple minutes...')
for link in cars_link:
    # time.sleep(1)
    single_link = driver.get(str(link))
    kilometer_xpath = '//span[@class="kt-group-row-item__value"]'
    year_xpath = '//span[@class="kt-group-row-item__value"]'
    price_xpath = '//p[@class="kt-unexpandable-row__value"]'
    body_xpath = '//*[@id="app"]/div[3]/div[1]/div[1]/div/div[4]/div[6]/div[2]/p'
    search_bar = driver.find_elements(by=By.XPATH, value=kilometer_xpath)
    search_bar1 = driver.find_elements(by=By.XPATH, value=price_xpath)
    search_bar2 = driver.find_element(by=By.XPATH, value=body_xpath)
    car_spec = []
    for item in search_bar1:
        find_class = str(item.text).find('تومان')
        if find_class != -1:
            price = item.text
            car_spec.append(price)
            insurance_time = search_bar2.text
            car_spec.append(insurance_time)
            for text in search_bar:
                car_spec.append(text.text)
    all_cars.append(car_spec)

print(len(all_cars), 'cars information received !')
print(all_cars)

# print("creating to db...")
#
# mydb = connect(
#   host="127.0.0.1",
#   user="root",
#   password=""
# )
#
#
# db_cursor = mydb.cursor()
# random_number = randint(1, 100)
# database_name = 'hossein_kharazi%i' % random_number
# create_query = 'CREATE DATABASE %s' % database_name
# db_cursor.execute(create_query)
# cnx = connect(user='root', password='', host='127.0.0.1', database=database_name)
# db_cursor = cnx.cursor()
# use_query = 'USE %s' % database_name
# db_cursor.execute(use_query)
# db_cursor.execute('CREATE TABLE Specifications(model int(4), mileage int(15), price int(20));')
#
# print("connected to db.")
# for car in all_cars:
#     query = 'INSERT INTO Specifications VALUES (\'%i\', \'%i\', \'%i\') ;' % (car[2], car[1], car[0])
#     cursor = cnx.cursor()
#     cursor.execute(query)
#     cnx.commit()
# cnx.close()
# print('database %s created and updated.' % database_name)
#
driver.close()
