from selenium import webdriver
from mysql.connector import connect
from selenium.webdriver.common.by import By
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
This is Diver's Dom

        <div class="post-card-item kt-col-6 kt-col-xxl-4">
            <a class="kt-post-card kt-post-card--outlined" href="/v/پژو-206-تیپ-۲-مدل-۱۳۹۷_سواری-و-وانت_تهران_رباط-کریم_دیوار/gY-YC3An">
            </a>
        </div>
"""

xpaths = {'div': '//div[@class="post-card-item kt-col-6 kt-col-xxl-4"]',
              'mileage': '//span[@class="kt-group-row-item__value"]',
              'year': '//span[@class="kt-group-row-item__value"]',
              'price_insurance': '//p[@class="kt-unexpandable-row__value"]'
              }

search_all_divs = driver.find_elements(by=By.XPATH, value=xpaths['div'])
cars_links = []

for element in search_all_divs:
    find_a = element.find_element(by=By.TAG_NAME, value='a')
    href_value = find_a.get_attribute('href')
    cars_links.append(href_value)
# Now we have a list named cars_links
# and in this list we have every link of cars for extract data such as price and mileage from them

all_cars = []  # this list will include some other lists that have price, model and mileage
print('Extracting data from', web_page)
print('wait a couple minutes...')
for link in cars_links:
    # time.sleep(1)
    driver.get(str(link))
    search_mileage = driver.find_elements(by=By.XPATH, value=xpaths['mileage'])
    search_price_insurance = driver.find_elements(by=By.XPATH, value=xpaths['price_insurance'])

    car_spec = []

    for item in search_price_insurance:
        find_class_price = str(item.text).find('تومان')
        if find_class_price != -1:
            price = item.text
            car_spec.append(price)
            for text in search_mileage:
                car_spec.append(text.text)
    for item1 in search_price_insurance:
        find_insurance = str(item1.text).find('ماه')
        if find_insurance != -1:
            insurance_time = item1.text.replace('\u200c', ' ')
            car_spec.append(insurance_time)
    all_cars.append(car_spec)

# Delete cars that have incomplete information
for car in all_cars:
    if len(car) != 5:
        all_cars.remove(car)

print(len(all_cars), 'cars information received !')
print(all_cars)

print("connecting to db...")

mydb = connect(
  host="127.0.0.1",
  user="root",
  password="1234", auth_plugin='mysql_native_password'
)
db_cursor = mydb.cursor()
database_name = 'h_kh'

try:
    cnx = connect(user='root', password='1234', host='127.0.0.1', database=database_name, auth_plugin='mysql_native_password')

except (Exception,):
    create_query = 'CREATE DATABASE %s' % database_name
    db_cursor.execute(create_query)
    cnx = connect(user='root', password='1234', host='127.0.0.1', database=database_name, auth_plugin='mysql_native_password')

print("connected to db.")

db_cursor = cnx.cursor()
use_query = 'USE %s' % database_name
db_cursor.execute(use_query)

try:
    db_cursor.execute('CREATE TABLE cars (model varchar(6), mileage varchar(30),'
                      ' color varchar(15), insurance_time varchar(10), price varchar(30))'
                      ' CHARACTER SET utf8 COLLATE utf8_general_ci;')
except (Exception,):
    pass

# Change database setting for adding persian string
db_cursor.execute('ALTER TABLE cars CONVERT TO CHARACTER SET utf8 COLLATE utf8_general_ci;')
db_cursor.execute('ALTER TABLE cars DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci;')

# Check if data existed don't add to db
for car in all_cars:
    existing_query = 'SELECT * FROM cars WHERE model=\'%s\' AND mileage=\'%s\' AND color=\'%s\' ' \
                     'AND insurance_time=\'%s\' AND price=\'%s\'' % (car[2], car[1], car[3], car[4], car[0])
    db_cursor.execute(existing_query)
    existing_values = db_cursor.fetchall()
    if existing_values:
        pass
    else:
        insert_query = 'INSERT INTO cars VALUES (\'%s\', \'%s\', \'%s\', \'%s\', \'%s\');' \
                       % (car[2], car[1], car[3], car[4], car[0])
        cursor = cnx.cursor()
        cursor.execute(insert_query)
        cnx.commit()


cnx.close()

print('database %s updated.' % database_name)

driver.close()
