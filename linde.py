
# %% Set Up

# Importing Libraries
# General
import pandas as pd
import time as t
# Selenium
from selenium import webdriver

## Normal
# Defining the Browser
browser = webdriver.Chrome()
# Go to Page
browser.get('URL')
# Implicit wait
browser.implicitly_wait(30)


# %% General Loop

# Saving all Selenium elements 
info_box = browser.find_elements_by_xpath(
      '//div[@class="ubsf_locations-list-item ubsf_locations-list-item-with-hover-effect"]'
      )
# Loop for the List
local_list = []
for distributor in range(len(info_box)):
   local = info_box[distributor].text.split('\n')
   local[2] = local[2].split(' ')[1]
   local[3] = local[3].split(' km ')[1]
   local.insert(0,'Linde Gas')
   local_list.insert(distributor,
                     local[0:4])
# Building DF
linde_df = pd.DataFrame(local_list) \
   .rename(columns={
      0 : 'Enterprise',
      1 : 'Distributor',
      2 : 'Address',
      3 : 'Region'
   })
# Exporting Results
linde_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/linde_df.xlsx', 
   index = False
   )

# %%
