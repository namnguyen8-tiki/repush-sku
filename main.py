# pylint: disable=E1136

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.select import Select

import requests
from bs4 import BeautifulSoup as bs 
import time
from assets import USER_AGENTS
import random
from tqdm import tqdm
import pandas as pd
import pandas_gbq

def get_sku_discrepancy():
    project_id = "tnsl-dwh"
    sql_sku_discrepancy = """
    select
    dp.sku
    from `tnsl-dwh.dwh.dim_product` dp
    left join `tiki-dwh.ecom.catalog_product` cp on dp.sku = cp.sku
    where 1 = 1
    and dp.cate2_erp = 'TNSL Partner'
    and cp.sku is null
    """
    print('Start querying SKU Discrepancy Data...')
    df_sku_discrepancy = pandas_gbq.read_gbq(sql_sku_discrepancy, project_id=project_id)
    return df_sku_discrepancy['sku'].tolist()

def chrome_driver():
    chrome_options = webdriver.ChromeOptions()
    # chrome_options.add_argument('--no-sandbox')
    # chrome_options.add_argument('--disable-dev-shm-usage')
    # chrome_options.add_argument('--disable-gpu')
    chrome_options.add_argument("--user-data-dir=chrome-data")
    chrome_options.add_argument('--headless') # Comment this line to see the browser
    chrome_options.add_argument(f'user-agent={random.choice(USER_AGENTS)}')
    return webdriver.Chrome(options=chrome_options)

def repush(list_sku):
    driver = chrome_driver()
    url = 'http://ops-api.tiki.vn/api/pegasus_repush_product?sku='
    
    for sku in tqdm(list_sku):
        driver.get(url + sku)
        driver.implicitly_wait(1)
        time.sleep(3)
        print(sku)

    driver.quit()
    
def main():
    repush(get_sku_discrepancy())

if __name__ == '__main__':
    main()