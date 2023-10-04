from time import sleep
import random

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pandas as pd

# --> 自動アクセスを実装してみる
options = Options()
options.add_argument('--incognito') # シークレットモードで開く

driver = webdriver.Chrome(options=options)

url = 'https://search.yahoo.co.jp/image'
driver.get(url)

sleep(3)

# --> STEP2 : プログラミングで検索する
query = 'かっこいいヒゲ'
search_box = driver.find_element_by_class_name('SearchBox__searchInput')
search_box.send_keys(query)
search_box.submit()

sleep(3)

# --> STEP3 : スクロールして表示件数を増やす
height = 1000
while height < 3000:
    driver.execute_script("window.scrollTo(0, {});".format(height))
    height += 200
    # print(height)
    sleep(1)

# --> STEP4 : 画像のURLを取得して、データフレームの形で保存しておく
elements = driver.find_elements_by_class_name('sw-Thumbnail')

# print(len(elements))

d_list = []
for i, e in enumerate(elements, start=1):
    name = f'{query}_{i}'
    raw_url = e.find_element_by_class_name('sw-ThumbnailGrid__details').get_attribute('href')
    yahoo_image_url = e.find_element_by_tag_name('img').get_attribute('src')
    title = e.find_element_by_tag_name('img').get_attribute('alt')

    d = {
        'filename': name,
        'raw_url': raw_url,
        'yahoo_image_url': yahoo_image_url,
        'title': title
    }

    d_list.append(d)

    sleep(2)
    sleep(random.randint(1, 10))

df = pd.DataFrame(d_list)
df.to_csv('image_urls.csv')

driver.quit()
