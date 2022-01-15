import requests 
from bs4 import BeautifulSoup
import re
import itertools
import pandas as pd

# place the page link here -- if local html file change this to the file path
URL = "https://accounts.clickbank.com/mkplSearchResult.htm?dores=true&includeKeywords=remote+jobs"

#page = open(URL) # if local file, uncomment this line; else, comment out
#soup = BeautifulSoup(page.read()) # if local file, uncomment this line; else, comment out

page = requests.get(URL) # if link, uncomment this line; else, comment out
soup = BeautifulSoup(page.content, "html.parser") # if link, uncomment this line; else comment out

results = soup.find(class_ = "page_content marketplace")

product_elements = results.find_all("tr", class_ = "result")
product_stats = results.find_all("td", class_ = "stats")

print('PRODUCT ELEMENTS LENGTH: ', str(len(product_elements)))
print('PRODUCT STATS LENGTH: ', str(len(product_stats)))

# get top 1 data to create a dataframe
product_element_init = product_elements[1]
product_title = product_element_init.find("a")
product_title = ' '.join(product_title.text.split())
product_description = product_element_init.find("div", class_ = "description")
product_description = ' '.join(product_description.text.split())
product_commission = product_element_init.find("span", class_ = "commission")
product_commission = ' '.join(product_commission.text.split())
product_stat_init = product_stats[1]
current_stats_init = product_stat_init.find_all("span", class_ = "stat")

if (len(current_stats_init) == 2):
    product_init_conversion = ""
    product_rebill = ""
    product_gravity = ' '.join(current_stats_init[0].text.split())
    product_category = ' '.join(current_stats_init[1].text.split())
elif (len(current_stats_init) == 3):
    product_init_conversion = ' '.join(current_stats_init[0].text.split())
    product_rebill = ' '.join(current_stats_init[1].text.split())
    product_gravity = ' '.join(current_stats_init[2].text.split())
    product_category = ""
elif (len(current_stats_init) == 4):
    product_init_conversion = ' '.join(current_stats_init[0].text.split())
    product_rebill = ' '.join(current_stats_init[1].text.split())
    product_gravity = ' '.join(current_stats_init[2].text.split())
    product_category = ' '.join(current_stats_init[3].text.split())

final_dat = pd.DataFrame([[product_title, product_description, product_commission, product_init_conversion, product_rebill, product_gravity, product_category]],
                            columns=['product_title', 'product_description', 'product_commission', 'product_init_conversion', 'product_rebill', 'product_gravity', 'product_category'])

# scrape the rest of the product results
for i in range(1,len(product_elements)):
    product_element = product_elements[i]
    product_title = product_element.find("a")
    product_title = ' '.join(product_title.text.split())
    product_description = product_element.find("div", class_ = "description")
    product_description = ' '.join(product_description.text.split())
    product_commission = product_element.find("span", class_ = "commission")
    product_commission = ' '.join(product_commission.text.split())

    print('\n\n')
    print('PRODUCT TITLE            :', str(product_title))
    print('PRODUCT DESCRIPTION      :', str(product_description))
    print('COMMISSION               :', str(product_commission))

    product_stat = product_stats[i]

    product_init_conversion = ""
    product_rebill = ""
    product_gravity = ""
    product_category = ""

    current_stats = product_stat.find_all("span", class_ = "stat")
    #print('CURRENT STATS LENGTH: ', str(len(current_stats)))

    if (len(current_stats) == 2):
        product_init_conversion = ""
        product_rebill = ""
        product_gravity = ' '.join(current_stats[0].text.split())
        product_category = ' '.join(current_stats[1].text.split())
    elif (len(current_stats) == 3):
        product_init_conversion = ' '.join(current_stats[0].text.split())
        product_rebill = ' '.join(current_stats[1].text.split())
        product_gravity = ' '.join(current_stats[2].text.split())
        product_category = ""
    elif (len(current_stats) == 4):
        product_init_conversion = ' '.join(current_stats[0].text.split())
        product_rebill = ' '.join(current_stats[1].text.split())
        product_gravity = ' '.join(current_stats[2].text.split())
        product_category = ' '.join(current_stats[3].text.split())

    print('PRODUCT INITIAL CONVERSTION      : ', str(product_init_conversion))
    print('PRODUCT REBILL                   : ', str(product_rebill))
    print('PRODUCT GRAVITY                  : ', str(product_gravity))
    print('PRODUCT CATEGORY                 : ', str(product_category))

    values = [product_title, product_description, product_commission, product_init_conversion, product_rebill, product_gravity, product_category]
    columns = ['product_title', 'product_description', 'product_commission', 'product_init_conversion', 'product_rebill', 'product_gravity', 'product_category']
    new_click = dict(zip(columns, values))
    print('NEW CLICK')
    print(new_click)
    final_dat = final_dat.append(new_click, True)

# export the results as a CSV file    
final_dat.to_csv('test_clickbank_file.csv')
