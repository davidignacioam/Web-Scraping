
# %% Set Up

# Importing Libraries
# General
import pandas as pd
import time as t
# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys

## Normal
# Defining the Browser
browser = webdriver.Chrome()
# Go to Page
browser.get('URL')
# Implicit wait
browser.implicitly_wait(10)


# %%

# Saving Initial objects
map_input = browser.find_elements_by_xpath(
   '//div[@tabindex="-1"]'
   )
location_list = []

# Starting time
start_time = t.time()

for map in range(1,len(map_input)):
   # Clicking
   t.sleep(1)
   browser.execute_script("arguments[0].click();", 
                          map_input[map])
   t.sleep(3)
   # Saving list
   local = browser.find_elements_by_xpath(
      '//div[@class="col-md-4"]'
      )[0] \
      .text \
      .split('\n')[1:3]
   location = local[1].split(', ')
   # Condiitons for address
   if len(location) == 3:
      del location[1]
   del local[1]
   if len(location) == 1:
      local.insert(1,location[0].split(' ')[1])
      local.insert(2,'no address')
   else:
      local.insert(1,location[1].split(' ')[1])
      local.insert(2,location[0])
   # Specifing enterprise
   local.insert(0,'Riessner Gas')
   # Saving final information
   location_list.insert(map,local)

# Ending time
end_time = t.time()
total_time = round((end_time-start_time)/60, 1)
print("--- %s minutes ---" % (total_time))

# Building DF
riessner_df = pd.DataFrame(location_list)  \
   .rename(columns={
      0 : 'Enterprise',
      1 : 'Distributor',
      2 : 'City',
      3 : 'Address'
   }) \
   .reset_index(drop=True) 

# Exporting Results
riessner_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/riessner_df.xlsx', 
   index = False
   )

# %%






