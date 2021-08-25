


# %% Set Up

# Importing Libraries
# General
import pandas as pd
import time as t
# Selenium
from selenium import webdriver
from selenium.webdriver.support.select import Select
from selenium.webdriver.common.keys import Keys

## Normal
# Defining the Browser
browser = webdriver.Chrome()
# Go to Page
browser.get('URL')
# Implicit wait
browser.implicitly_wait(30)

## Preparing Page
t.sleep(4)
# Changing Language
Select(browser.find_element_by_id("edit-lang-switcher")) \
   .select_by_visible_text('English')
# Visualizing Regions
browser.find_elements_by_id(
   'plus-cities-regions-icon'
   )[0] \
   .click()
# Saving Regions
t.sleep(2)
regions = browser.find_elements_by_id(
   'top_searched_cities_regions'
   )[0] \
   .text \
   .split('Searched Regions :\n')[1] \
   .split('\n')


# %% First Option

## General

# Start time
start_time = t.time()
# Creating Empty DF
final_df = pd.DataFrame({})

# Loop
for region in range(len(regions)):
   # Saving Input
   input_region = browser.find_element_by_css_selector(
      'input[id="input_search_distributor_by_region"]'
      )
   # Sending input
   input_region.clear()
   t.sleep(1)
   input_region.send_keys(regions[region])
   t.sleep(2)
   input_region.send_keys(Keys.ENTER)
   # Saving List with Ids
   t.sleep(3)
   content_ids = browser.find_elements_by_xpath(
      '//div[@id="distributor-result-content"]/*[@id]'
      )
   # Loop for ID List
   id_list = []    
   for content in range(len(content_ids)):
      id_element = content_ids[content].get_attribute('id') 
      id_list.append(id_element) 
   # Loop for DF
   for id in range(len(id_list)):
      local = browser.find_elements_by_id(id_list[id])[0].text.split('\n')
      t.sleep(1)
      # Defining Title
      title = local[0] 
      # Loop for Page
      if '@' in local[4]: 
         local.insert(4,"no page")
      elif 'Monday:' in local[5]: 
         local.insert(4,"no page")
      else:
         # Page URL
         id_url_p = id_list[id].split('-')[2]
         string_p = f"distributor-web-site-{id_url_p}"
         string_url_p = f'div[id="{str(string_p)}"] > a'
         Page_url = browser.find_element_by_css_selector(
            str(string_url_p)
            ) \
            .get_attribute('href') 
         local[4] = Page_url
      if not '@' in local[5]: 
         local.insert(5,"no mail")   
      # Google URL
      id_url_g = id_list[id].split('-')[2]
      string_g = f"distributor-direction-{id_url_g}"
      string_url_g = f'div[id="{str(string_g)}"] > a'
      Google_url = browser.find_element_by_css_selector(
            str(string_url_g)
            ) \
            .get_attribute('href') 
      local[6] = Google_url
      # Deleting title
      del local[0]
      # Loop for Date
      if len(local) == 6:
         days = ['Monday','Tuesday','Wednesday',
                 'Thursday','Friday','Saturday']
         for day in days:
            local.append(f"{day}: no date")  
      if len(local) == 11:
         local.append('Saturday: not working')
      # Adding new column
      final_df[title] = local

# End time
end_time = t.time()
total_time = round((end_time-start_time)/60, 1)
print("--- %s minutes ---" % (total_time))
# Exporting Results
t.sleep(1)
final_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Selenium/webscraping.xlsx', 
   index = False
   )
# Page refresh
t.sleep(1)
browser.refresh()



# %%

DF = pd.read_excel(
    '/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/airliquide_df.xlsx'
    ) 

# %%

address = DF['Address']

list_city = []

for element in range(len(address)):
   list_city.insert(element,
                    address[element].split(', ')[-2].split(' ')[1])

DF['City'] = list_city

airliquide_df = DF \
   .rename(columns={'Region' : 'Federal State'}) \
   [['Enterprise','Distributor','Federal State','City','Address']]

airliquide_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/airliquide_df.xlsx', 
   index = False
   )

# %%
