


# %% Set Up

# Importing Libraries
# General
import pandas as pd
import time as t
# Selenium
from selenium import webdriver
# Others
import regex as re


## Normal
# Defining the Browser
browser = webdriver.Chrome()
# Go to Page
browser.get('URL')
# Implicit wait
browser.implicitly_wait(30)


# %% 

# Saving all Selenium elements with ids
id_path = browser.find_elements_by_xpath(
      '//div[@class="businesses_list"]/*[@id]'
      )
t.sleep(1)
# Creating empty list
id_list = []
# Filling it with ids
for n in range(len(id_path)):
   id_element = id_path[n].get_attribute('id')
   id_list.append(id_element)

# %% Short Option: withput Date

## General

# Start time
start_time = t.time()
# Creating Empty DF
final_df = pd.DataFrame({})

for id in range(len(id_list)) :
   # Scraping main info
   local = browser.find_elements_by_id(
      id_list[id]
      )[0] \
      .text \
      .split('\n')
   # Specifing empty values
   local[2] = re.sub(r'[0-9]+ ', '', local[2])
   if not 'Telefon:' in local[3]:
      local.insert(3,'no Phone') 
   else :
      local[3] = local[3].replace('Telefon:','')
   if not 'Fax:' in local[4]:
      local.insert(4,'no Fax')
   else :
      local[4] = local[4].replace('Fax:','')
   if not '@' in local[5]:
      local.insert(5,'no Mail') 
   # Adding new column
   final_df[local[0]] = local[0:6]

# End time
end_time = t.time()
total_time = round((end_time-start_time), 1)
print("--- %s seconds ---" % (total_time))

# Building DF
basi_Gase_df = final_df \
   .T \
   .reset_index(drop=True) \
   .rename(columns={
      0 : 'Distributor',
      1 : 'Address',
      2 : 'City',
      3 : 'Telephone',
      4 : 'Fax',
      5 : 'Mail'
   }) 
basi_Gase_df.insert(loc=0,
                    column='Enterprise', 
                    value='Basi')
basi_df = basi_Gase_df[['Enterprise','Distributor','City','Address']]
# Exporting Results
basi_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/basi_df.xlsx', 
   index = False
   )

# %%
