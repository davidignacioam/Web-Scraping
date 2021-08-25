

# %% Set Up

# Importing Libraries
# General
import pandas as pd
import time as t
# Selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.alert import Alert

## Google Browser
# Defining the Browser
browser = webdriver.Chrome()
# Go to Page
browser.get('URL')
# Implicit wait
browser.implicitly_wait(10)
# For alerts
alert = Alert(browser)

## Google Maps Browser
# Defining the Browser
browserMaps = webdriver.Chrome()
# Go to Page
browserMaps.get('URL')
# Implicit wait
browserMaps.implicitly_wait(10)
# For alerts
alert = Alert(browserMaps)
# Setting English Language
t.sleep(15)
browserMaps.find_elements_by_xpath(
   '//button[@class="searchbox-button"]'
   )[0].click()
t.sleep(2)
browserMaps.find_elements_by_xpath(
   '//button[@class="KY3DLe-languages-QA0Szd-LgbsSe KY3DLe-settings-LgbsSe"]'
   )[0].click()
t.sleep(4)
browserMaps.find_elements_by_xpath(
   '//li[@jsinstance="10"]'
   )[0].click()
t.sleep(1)

## Global Data frame
# Importing Data
nippon_df = pd.read_excel(
    '/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/nippon_df.xlsx'
    )
airliquide_df = pd.read_excel(
    '/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/airliquide_df.xlsx'
    )
basi_df = pd.read_excel(
    '/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/basi_df.xlsx'
    )
linde_df = pd.read_excel(
    '/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/linde_df.xlsx'
    )
riessner_df = pd.read_excel(
    '/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/riessner_df.xlsx'
    )
# Building final DF
empty_df = pd.DataFrame()
final_df = empty_df \
   .append(nippon_df) \
   .append(airliquide_df) \
   .append(basi_df) \
   .append(linde_df) \
   .append(riessner_df)
# Filtering useless data
final_df = final_df[final_df['Distributor'] != 'Auslieferungslager']
# Exporting Results
final_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/final_df.xlsx', 
   index = False
   )

# %%

# Defining the main variable
Distributor = final_df['Distributor']
# Empty Objects
business_model = []

# Starting time
start_time = t.time()

for distributor in range(len(Distributor)):
   ########## General Google Search
   input_google = browser.find_elements_by_xpath(
      '//input[@class="gLFyf gsfi"]'
      )[0]
   input_google.clear()
   input_google.send_keys(Distributor[distributor])
   t.sleep(1)
   button_google = browser.find_elements_by_xpath(
      '//button[@class="Tg7LZd"]'
      )[0]
   button_google.click()
   t.sleep(3)
   text_field = browser.find_elements_by_xpath(
      '//span[@class="YhemCb"]'
      )
   if len(text_field) == 0:
      ########## Google Maps Scraping
      input_google = browserMaps.find_elements_by_xpath(
         '//input[@id="searchboxinput"]'
         )[0]
      input_google.clear()
      input_google.send_keys(Distributor[distributor])
      t.sleep(1)
      input_google.send_keys(Keys.ENTER)
      ####### Loop for First Text
      t.sleep(6)
      list_google_maps = browserMaps.find_elements_by_xpath(
         '//button[@class="widget-pane-link"]'
         )
      text_google_maps = []
      for text in range(len(list_google_maps)):
         text_value = list_google_maps[text].text
         if ('' == text_value) or ('review' in text_value):
            pass
         else:
            text_google_maps.append(text_value)
      t.sleep(1)
      ####### Condition for First Text
      if len(text_google_maps) == 0:
         hidden_space = browserMaps.find_elements_by_xpath(
            '//div[@class="lI9IFe" or @class="Z8fK3b"]'
            )
         ####### Condition for Second Text
         if len(hidden_space) == 0:
            business_model.insert(distributor,
                                  '')
         else:
            ####### Loop for Second Text
            hidden_values = []
            for hiden in range(len(hidden_space)):
               if not hidden_space[hiden].text == '':
                  hidden_values.append(hidden_space[hiden].text)
            hidden_text = hidden_values[0] \
               .split('\n')[2] \
               .split(' · ')[0]
            business_model.insert(distributor,
                                    hidden_text)
            hidden_text = []
      else:
         business_model.insert(distributor,
                               text_google_maps[0])
         text_google_maps = []
   else:
      text_google = text_field[0] \
         .text \
         .split(' in')[0]
      t.sleep(1)
      business_model.insert(distributor,
                            text_google)
      text_google = []

# Ending time
end_time = t.time()
total_time = round((end_time-start_time)/60, 1)
print("--- %s minutes ---" % (total_time))

# Adding Column
final_google_df = final_df
final_google_df['Business Model'] = business_model
final_google_df = final_google_df.reset_index(drop=True)
# Exporting Results
final_google_df.to_excel(
   r'/Users/usuario/Documents/Python/Evalueserve/PoC/Web Scraping/final_google_df.xlsx', 
   index = False
   )


# %%
