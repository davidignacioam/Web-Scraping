


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

# %% General Loop

# Saving Objects
regions = [
   'Berlin','Bayern' ,'Niedersachsen',
   'Baden-Württemberg','Rheinland-Pfalz' 
   'Sachsen','Thüringen','Hessen',
   'Nordrhein-Westfalen','Sachsen-Anhalt',
   'Brandenburg','Mecklenburg-Vorpommern',
   'Hamburg','Schleswig-Holstein'
   'Saarland','Bremen'
]
final_df = pd.DataFrame({})

# Starting time
start_time = t.time()

for region in range(len(regions)):
   input_region = browser.find_elements_by_id(
      'dl__input__address'
      )[0]
   input_region.clear()
   t.sleep(1)
   input_region.send_keys(regions[region])
   t.sleep(3)
   input_region.send_keys(Keys.DOWN)
   t.sleep(1)
   input_region.send_keys(Keys.ENTER)
   t.sleep(1)
   browser.find_elements_by_xpath(
         '//button[@class="dl__startSearch"]'
         )[0] \
         .click()
   t.sleep(5)
   dataindex = browser.find_elements_by_xpath(
         '//div[@class="dl__results"]/*[@data-index]'
         )
   for index in range(len(dataindex)):
      # Show More Click
      t.sleep(1)
      specific_index = dataindex[index].get_attribute('data-index')
      string_span = f'//div[@class="dl__dealer" and @data-index={specific_index}]/div[@class="dl__icon"]/span'
      browser.find_elements_by_xpath(
            string_span
            )[0].click()
      # Scraping Data
      t.sleep(3)
      local = browser.find_elements_by_xpath(
            '//div[@class="dl__dealerDetail dl__dealerDetail__visible"]'
            )[0] \
            .text \
            .split('\n')
      # Conditions
      if 'Telefon' in local:
         local.remove('Telefon')
      else:
         local.insert(2,'no Phone')
      if 'Fax' in local:
         local.remove('Fax')
      else:
         local.insert(3,'no Fax')
      if 'E-Mail' in local:
         local.remove('E-Mail')
      else:
         local.insert(4,'no Mail')
      # Inserting Region
      local.insert(1,regions[region])
      # Appending the DF
      final_df[local[0]] = local[0:6]
      # Back to results
      t.sleep(1)
      browser.find_elements_by_xpath(
            '//button[@class="dl__back"]'
            )[0] \
            .click()
      t.sleep(1)

# Ending time
end_time = t.time()
total_time = round((end_time-start_time)/60, 1)
print("--- %s minutes ---" % (total_time))

# Building DF
nippon_df = final_df \
   .T \
   .reset_index(drop=True) \
   .rename(columns={
      0 : 'Distributor',
      1 : 'Federal State',
      2 : 'Address',
      3 : 'Telephone',
      4 : 'Fax',
      5 : 'Mail',
   }) 
nippon_df.insert(loc=0,
                 column='Enterprise', 
                 value='Nippon Gases')
nippon_df = nippon_df[['Enterprise','Distributor','Federal State','Address']]
# Exporting Results
nippon_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/nippon_df.xlsx', 
   index = False
   )
# %%

DF = pd.read_excel(
    '/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/nippon_df.xlsx'
    ) 

address = DF['Address']

city_list = []

for element in range(len(address)):
   city_list.insert(element,address[element].split(' ')[-1]) 

DF['City'] = city_list

nippon_df = DF \
   .rename(columns={'Region' : 'Federal State'}) \
   [['Enterprise','Distributor','Federal State','City','Address']]

nippon_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/nippon_df.xlsx', 
   index = False
   )
# %%
