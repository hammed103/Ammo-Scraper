#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import urllib
import numpy as np

from tkinter import ttk
import tkinter as tk
from time import sleep
from tkinter.messagebox import showinfo

import itertools
from urllib.request import urlretrieve
import selenium
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException ,StaleElementReferenceException
from selenium.common.exceptions import NoSuchElementException,ElementClickInterceptedException,ElementNotInteractableException
from webdriver_manager.chrome import ChromeDriverManager as CM
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd
from time import sleep
from selenium.webdriver import ActionChains
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from joblib import Parallel, delayed

import dill as pickle
chrome_options = Options()
chrome_options.add_argument('--lang=en_US') 
chrome_options.add_argument("--headless")
chrome_options.add_argument('--window-size=1920,1080')



f = open("path.txt",'r')
dpath = f.read()


#chrome_options.headless = True # also works
chrome_options.add_argument('disable-blink-features=AutomationControlled')
chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36")


# In[2]:


def trueshot():
    try: 
        driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)
        print('lol')
        driver.delete_all_cookies()
        #driver = webdriver.Chrome(r"Chromeedriver")
        driver.get("https://trueshotgunclub.com/")
        sleep(5)

        def collector():
            page = driver.find_element_by_css_selector('ul[class *="products elementor-grid columns"]')
            ot = page.find_elements_by_css_selector('li')
            pagex = [i.find_element_by_css_selector('a').get_attribute('href') for i in  ot]

            return pagex

        opc = driver.find_element_by_css_selector('nav[class="elementor-nav-menu--main elementor-nav-menu__container elementor-nav-menu--layout-horizontal e--pointer-text e--animation-none"]')

        bod = [i.get_attribute('href') for i in opc.find_elements_by_css_selector('a')]

        bodn = [i.text for i in opc.find_elements_by_css_selector('a')]

        bod = bod[1:]
        #bodn = bodn[1:]

        bodx = bod[:-2]

        bodx

        def lamba(bad) :



            driver = webdriver.Chrome( executable_path=r"Chromeedriver", 
                                  options=chrome_options)

            driver.get(bad)

            all_links = []

            lo = True
            while lo:
                try:
                    page = driver.find_element_by_css_selector('ul[class *="products elementor-grid columns"]')
                    ot = page.find_elements_by_css_selector('li')
                    pagex = [i.find_element_by_css_selector('a').get_attribute('href') for i in  ot]
                    all_links += pagex
                    print(len(all_links))
                except:
                    page = driver.find_element_by_css_selector('ul[class *="products elementor-grid columns"]')
                    ot = page.find_elements_by_css_selector('li')
                    pagex = [i.find_element_by_css_selector('a').get_attribute('href') for i in  ot]
                    all_links += pagex
                    print(len(all_links))
                try:
                    driver.find_element_by_css_selector('div[data-value="next"]').click()
                    sleep(6)
                except:
                    lo = False

            boxed = []
            for jj in range(len(all_links)):
                box = []
                box.append(bad.split('/')[-2])
                url = all_links[jj]
                driver.get(url)
                try:
                    section = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/section[1]')
                except:
                    continue



                pname = section.find_element_by_css_selector('h1[class="product_title entry-title elementor-heading-title elementor-size-default"]').text

                box.append(pname)

                sleep(3)

                box.append(url)
                try:

                    section = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/section[2]')
                    sleep(3)
                    images = section.find_element_by_css_selector('div[class="smv-ss"]')

                    images = [i.get_attribute('src') for i in images.find_elements_by_css_selector('img')]
                    if len(images) < 1 :
                        driver.refresh()
                        sleep(10)
                        section = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/section[2]')

                        images = section.find_element_by_css_selector('div[class="smv smv-selectors-bottom"]')

                        images = [i.get_attribute('src') for i in images.find_elements_by_css_selector('img')] 
                        if len(images) < 1:
                            driver.refresh()
                            sleep(7)
                            section = driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/section[2]')
                            images = section.find_element_by_css_selector('div[class="smv smv-selectors-bottom"]')
                            images = [i.get_attribute('data-src') for i in images.find_elements_by_css_selector('div[data-type="zoom"]')] 
                        else:
                            pass
                    else:
                        pass
                except:
                    images = []


                sleep(6)
                #section = driver.find_element_by_css_selector('section[class="elementor-section elementor-top-section elementor-element elementor-element-b91ab66 elementor-section-full_width elementor-section-content-top elementor-section-height-default elementor-section-height-default"]')
                box.append(images)
                ppr = section.find_elements_by_css_selector('span[class="woocommerce-Price-amount amount"]')

                reg = ppr[0].text
                box.append(reg)
                try:
                    spec = ppr[1].text
                except:
                    spec = ''
                box.append(spec)
                try:
                    vid = section.find_element_by_css_selector('div[class="premium-video-box-video-container"]')

                    video = vid.find_element_by_css_selector('a').get_attribute('href')
                except:
                    video = ''
                box.append(video)
                try:
                    sale = section.find_element_by_css_selector('span[class="jet-listing-dynamic-field__content"]').text
                except:
                    try:
                       sale = section.find_element_by_css_selector('div[class="jet-listing-dynamic-field__content"]').text 
                    except:
                        sale = ''
                box.append(sale)
                try:
                    details = driver.find_element_by_css_selector('div[class="woocommerce-product-details__short-description"]').text
                except:
                    details = ''
                box.append(details)
                try:
                    av = driver.find_element_by_css_selector('p[class="stock out-of-stock"]').text
                except:
                    av = ''
                box.append(av)
                try:
                    sku   =  driver.find_element_by_xpath('//*[@id="content"]/div/div[2]/div/section[2]/div/div/div[2]/div/div/section[3]/div/div/div/div/div/div[2]/div/h1').text
                except:
                    sku = ''
                box.append(sku)
                tab = driver.find_element_by_xpath('//*[@id="uael-table-id-14285d37"]')
                tab = driver.find_element_by_css_selector('tbody')
                keys = [i.find_elements_by_css_selector('td')[0].text for i in tab.find_elements_by_css_selector('tr')[1:]]
                box.append(keys)
                values = [i.find_elements_by_css_selector('td')[1].text for i in tab.find_elements_by_css_selector('tr')[1:]]
                box.append(values)
                boxed.append(box)
                print(jj)


            driver.close()
            return boxed



        ping = Parallel(n_jobs= 4 )(delayed(lamba)(bad) for bad in bodx) #execute parallel for all urls

        from copy import deepcopy

        baba = deepcopy(ping)

        import itertools

        boxed = (list(itertools.chain.from_iterable(ping)))

        df = pd.DataFrame(boxed)

        poll = df[[11,12]].apply(lambda x: dict(zip(x[11],x[12])),axis=1)

        police = pd.json_normalize(poll)

        police

        df.head(50)

        rest = df[[0,1,2,4,5,6,7,8,9,10]]
        rest.columns = ['Category','Product Name','Url','Price','Sale_Price','Videos','Price_Per_Round','Description','Availability','SKU']

        images = pd.DataFrame(df[3].to_list())

        images.columns = ['image' + str(i) for i in range(1,images.shape[1] + 1)]

        df2 = rest.join(police)

        df3 = df2.join(images)

        df3['Price_Per_Round'] = df3['Price_Per_Round'].str.lstrip('SALE:').str.rstrip('PER ROUND')

        df3.loc[df3['Availability'] == '','Availability'] = 'In Stock'

        df3.to_excel(dpath+ 'Fresh_Trueshot.xlsx')

        df3.columns

        reorg = df3[[ 'Price', 'Sale_Price', 'Price_Per_Round', 'Availability']]

        df3 = df3.drop(columns = reorg.columns )

        df3[reorg.columns ] = reorg

        df3.head(2)

        pd.set_option('display.max_colwidth',300)

        df3  = df3.drop_duplicates('Url')

        try:

            old = pd.read_excel(dpath+ 'Newly_Updated_Trueshot.xlsx')

            old  =  old.drop_duplicates('Url')

            lamb = df3.merge(old, on =  ['Url','Product Name'],how='outer' , )

            tbd = [i for i in lamb if i.endswith('_y')]

            lamb = lamb.drop(columns = tbd)

            aa = [i for i in lamb if i.endswith('_x')]

            aaa = [i.replace('_x','') for i in lamb if i.endswith('_x')]

            lamb = lamb.rename(columns = dict(zip(aa,aaa)))
        except:
            lamb = df3


        from datetime import date

        td = str(date.today())

        td

        lamb = lamb.rename(columns = {'Price':'Price '+td,'Price_per_Round':'Price_per_Round '+td,'Stock':'Stock '+td,'Availablility':'Availablility '+td,})

        lamb.columns





        lamb.to_excel(dpath+ 'Newly_Updated_Trueshot.xlsx',index=False)
        showinfo(message= 'The Progress has been Completed')
    except:
        showinfo(message= 'The Progress has been Interrupted')


# In[3]:


def ammoo():
    try :

        def pickery(non):
            cat = driver.find_element_by_css_selector('ol[class="b-category-product-list p-category__products js-category-products"]')
            otp = cat.find_elements_by_css_selector('li[class="b-product-list-item b-category-product-list__item"]')
            joba = otp[non]
            #print('.')
            boxn = []

            #box.append(opl)
            boxn.append(opo)
            a = driver.current_url
            boxn.append(a)
            pil = joba.find_element_by_css_selector('img[class="b-image__img"]')

            imgs = [pil.get_attribute('src')]
            boxn.append(imgs)

            name = joba.find_element_by_css_selector('h2[class="b-product-list-item__product-name"]').text
            boxn.append(name)

            price = joba.find_element_by_css_selector('span[class *="price"]').text
            boxn.append(price)
            try:
                price2 = joba.find_element_by_css_selector('ul[class="b-product-list-item__attributes-short"]').text
            except:
                price2 = ''
            boxn.append(price2)

            availability =  joba.find_element_by_css_selector('p[class="b-availability__in-stock"]').text
            boxn.append(availability)


            tb = joba.find_elements_by_css_selector('span[class="b-attributes__item-label"]')

            td = joba.find_elements_by_css_selector('span[class="b-attributes__item-value"]')

            th = [i.get_attribute('innerHTML').strip('\n ') for i in tb]

            boxn.append(th)
            td = [i.get_attribute('innerHTML').strip('\n ') for i in td]
            boxn.append(td)
            #print(box)
            boxed.append(boxn)




        def sleepery():
            try:
                peep = driver.find_element_by_css_selector('div[class="page-title"]')
                sleeping = peep.find_element_by_css_selector('h1').text == "Service Temporarily Unavailable"
                while sleeping :
                    print('Sleeping')
                    sleep(30)
                    driver.refresh()
                    sleep(2)
                    peep = driver.find_element_by_css_selector('div[class="page-title"]')
                    sleeping = peep.find_element_by_css_selector('h1').text == "Service Temporarily Unavailable"
            except :
                pass

        def boxery():
            try:
                bro = driver.find_element_by_css_selector('select[class="e-input b-limiter__select"]')
                bro.find_elements_by_css_selector('option')[-1].click()
                sleep(2)
                cat = driver.find_element_by_css_selector('ol[class="b-category-product-list p-category__products js-category-products"]')
                otp = cat.find_elements_by_css_selector('li[class="b-product-list-item b-category-product-list__item"]')
                for non in range(len(otp)):
                    try:
                        pickery(non)
                    except:
                        sleepery()
                        pickery(non)
            except NoSuchElementException :
                pass






        driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)
        driver.delete_all_cookies()
        #driver = webdriver.Chrome(r"Chromedriver")
        driver.get("https://ammo.com/")
        sleep(5)

        driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[3]').click()

        job = driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[3]')

        job = job.find_element_by_css_selector('ul[class="b-top-menu__sub-list"]')

        groups = job.find_elements_by_css_selector('li[class="b-top-menu__item b-top-menu__item--has-children"]')

        box = [i.find_element_by_css_selector('a').get_attribute('href') for i in  groups]







        driver.get("https://ammo.com/")
        driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[3]').click()
        job = driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[3]')
        job = job.find_element_by_css_selector('ul[class="b-top-menu__sub-list"]')

        groups = job.find_elements_by_css_selector('li[class="b-top-menu__item b-top-menu__item--has-children"]')
        groups = [i.find_element_by_css_selector('a').get_attribute('href') for i in  groups]
        boxed = []
        for d in range(len(groups)) :

            driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[3]').click()
            job = driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[3]')
            job = job.find_element_by_css_selector('ul[class="b-top-menu__sub-list"]')

            groups = job.find_elements_by_css_selector('li[class="b-top-menu__item b-top-menu__item--has-children"]')
            groups = [i.find_element_by_css_selector('a').get_attribute('href') for i in  groups]
            events = driver.get(groups[d])
            sleep(4)
            box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')

            for j in range(len(box)) :
                try:
                    events = driver.get(groups[d])
                    sleep(4)
                    box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')
                    box[j].click()
                    sleep(4)
                    opo = driver.find_element_by_css_selector('h1[class="e-heading-page p-category__title"]').text
                    boxery()
                    print(opo)
                except:
                    sleepery()
                    box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')
                    box[j].click()
                    sleep(4)
                    opo = driver.find_element_by_css_selector('h1[class="e-heading-page p-category__title"]').text
                    boxery()
                    print(opo)







        driver.get("https://ammo.com/")
        driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[5]').click()
        job = driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[5]')
        groups = job.find_elements_by_css_selector('a')[-1].get_attribute('href')
        events = driver.get(groups)
        box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')   
        for j in range(len(box)) :
            try:
                box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')
                box[j].click()
                sleep(4)
                opo = driver.find_element_by_css_selector('h1[class="e-heading-page p-category__title"]').text
                boxery()
                print(opo)
                driver.back()
                sleep(4)
            except:
                sleepery()
                box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')
                box[j].click()
                sleep(4)
                opo = driver.find_element_by_css_selector('h1[class="e-heading-page p-category__title"]').text
                boxery()
                print(opo)
                driver.back()
                sleep(4)


        driver.get("https://ammo.com/")
        driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[6]').click()
        job = driver.find_element_by_xpath('//*[@id="js-top-menu"]/div/div/ul[1]/li[6]')
        groups = job.find_elements_by_css_selector('a')[-1].get_attribute('href')


        events = driver.get(groups)
        sleep(4)

        box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')

        for j in range(len(box)) :
            try:
                box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')
                box[j].click()
                sleep(4)
                opo = driver.find_element_by_css_selector('h1[class="e-heading-page p-category__title"]').text
                boxery()
                print(opo)
                driver.back()
            except:
                sleepery()
                box = driver.find_elements_by_css_selector('a[class="e-badge-button b-popular-ammo__item "]')
                box[j].click()
                sleep(4)
                opo = driver.find_element_by_css_selector('h1[class="e-heading-page p-category__title"]').text
                boxery()
                print(opo)
                driver.back()



        from copy import deepcopy

        bb = deepcopy(boxed)

        pd.DataFrame(boxed)

        df = pd.DataFrame(boxed)

        df.to_csv('boxed_amoo.csv')

        df.head()

        def vion(test_keys,test_values) :
            teset_values = deepcopy(test_values)
            res = {}
            for key in test_keys:
                for value in teset_values:
                    res[key] = value
                    teset_values.remove(value)
                    break  
            return res

        images = pd.DataFrame(df[2].to_list())

        images.columns = ['image' + str(i) for i in range(1,images.shape[1] + 1)]

        poll = df[[7,8]].apply(lambda x: vion(x[7], x[8]),axis =1)

        poll

        pd.json_normalize(poll).columns

        police = pd.json_normalize(poll)

        police.head()

        df.head(1)

        rest = df[[0,1,3,4,5,6]]

        rest.columns = ['Category','Url','Product Name','Price','Price_per_Round','Stock']

        df2 = rest.join(police)

        df3 = df2.join(images)

        df3.columns

        df3['Type']  =  df3.Url.apply(lambda x: x.split('/')[-2]).str.capitalize()

        df3['Quantity']   = df3.Price_per_Round.apply(lambda x: ' '.join(x.split(' ')[:2]))

        df3.loc[df3['Manufacturer'].isna(),'Manufacturer']   =  df3.loc[df3['Manufacturer'].isna(),'Price_per_Round'].apply(lambda x: ' '.join(x.split(' ')[5:]))  

        df3.Price_per_Round = df3.Price_per_Round.apply(lambda x: ' '.join(x.split(' ')[2:5]))

        df3

        df3['Availablility'] = df3['Stock'].apply(lambda x: ' '.join(x.split(' ')[1:]))
        df3['Stock'] = df3['Stock'].apply(lambda x: x.split(' ')[0])

        df3

        df3 = df3.rename(columns = {'Bullet type':'Bullet Type','Casing Type':'Ammo Casing','Muzzle Velocity':'Muzzle Velocity (fps)','Muzzle Energy':'Muzzle Energy (ft lbs)','Category':'Subcategory','Type':'Category'})

        df3.loc[df3['Bullet Type'].notna(),'Ammo Caliber']  = df3.loc[df3['Bullet Type'].notna(),'Url'].apply(lambda x: x.split('/')[-1])

        df3.columns

        df3['Subcategory']  = df3['Subcategory'].str.replace('Ammo For Sale','')

        df3['Price_per_Round']  = df3['Price_per_Round'].str.replace('per round','')

        df3 = df3[['Category','Subcategory', 'Url', 'Product Name', 'Price', 'Price_per_Round','Stock', 'Quantity', 'Availablility', 'Bullet Type', 'Primer Type', 'Ammo Casing', 'Condition',
               'Muzzle Velocity (fps)', 'Muzzle Energy (ft lbs)', 'Sizes Available','Design', 'Manufacturer', 'Article Type', 'image1', 
               'Ammo Caliber']]

        reorg = df3[[ 'Price',
               'Price_per_Round', 'Quantity', 'Stock', 'Availablility']]

        df3 = df3.drop(columns = reorg.columns )

        df3[reorg.columns ] = reorg

        df3.head(50)

        df3.to_excel(dpath+ 'Fresh_Amoo.xlsx',index=False)

        try:

            old = pd.read_excel(dpath+ 'Newly_Updated_Amoo.xlsx')

            old['Quantity'] = old['Quantity'].fillna('')

            df3['Quantity'] = df3['Quantity'].fillna('')

            lamb = df3.merge(old, on =  [ 'Category', 'Subcategory', 'Url', 'Product Name',
                'image1',],how='outer' , )

            tbd = [i for i in lamb if i.endswith('_y')]

            lamb = lamb.drop(columns = tbd)

            aa = [i for i in lamb if i.endswith('_x')]

            aaa = [i.replace('_x','') for i in lamb if i.endswith('_x')]

            lamb = lamb.rename(columns = dict(zip(aa,aaa)))
        except:
            lamb = df3

        lamb





        from datetime import date

        td = str(date.today())

        lamb = lamb.rename(columns = {'Price':'Price '+td,'Price_per_Round':'Price_per_Round '+td,'Stock':'Stock '+td,'Availablility':'Availablility '+td,})

        lamb.columns

        lamb

        lamb.to_excel(dpath+ 'Newly_Updated_Amoo.xlsx',index=False)
        
        showinfo(message= 'The Progress has been Completed')
        
    except:
        showinfo(message= 'The Progress has been Interrupted')


# In[4]:


def lucky():
    
    try :

        driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)
        driver.delete_all_cookies()
        print("loaded")

        def sleeper():
            try:
                peep = driver.find_element_by_css_selector('div[class="page-title"]')
                sleeping = peep.find_element_by_css_selector('h1').text == "We're Sorry."
                while sleeping :
                    print('Sleeping')
                    sleep(30)
                    driver.refresh()
                    sleep(2)
                    peep = driver.find_element_by_css_selector('div[class="page-title"]')
                    sleeping = peep.find_element_by_css_selector('h1').text == "We're Sorry."
            except :
                pass

        def picker(non):
            cat = driver.find_element_by_css_selector('ol[class="products-list"]')
            otp = cat.find_elements_by_css_selector('li[class *="item"]')
            otp[non].find_element_by_css_selector('a').click()
            #print('.')
            box = []

            box.append(opl)
            box.append(opo)
            a = driver.current_url
            box.append(a)
            pil = driver.find_element_by_css_selector('ul[id="imageGallery"]')

            imgs = [i.get_attribute('data-src') for i in pil.find_elements_by_css_selector('li[class *="lslide"]')]
            box.append(imgs)

            name = driver.find_element_by_css_selector('h1[class="product-name"]').text
            box.append(name)

            price = driver.find_element_by_css_selector('div[class *="price"]').text
            box.append(price)

            price2 = driver.find_element_by_css_selector('div[class="col-cprc"]').text
            box.append(price2)

            availability =  driver.find_element_by_css_selector('p[class="availability"]').text
            box.append(availability)

            s_desc = driver.find_element_by_css_selector('div[id="js-short-description-content"]').text

            box.append(s_desc)

            tb = driver.find_element_by_css_selector('table[class="data-table"]')

            th = [i.text for i in tb.find_elements_by_css_selector('th')]
            box.append(th)

            td = [i.text for i in tb.find_elements_by_css_selector('td')]
            box.append(td)
            try:
                use_type = driver.find_element_by_css_selector('div[class *="product-attribute-use-type-specs"]').text
            except:
                use_type = ''
            box.append(use_type)

            full_desc = driver.find_element_by_css_selector('div[id="js-col-details"]').text
            box.append(full_desc)
            driver.back()
            sleep(3)
            #print(box)
            boxed.append(box)
            print('.')

        def boxer():
            try:

                sleep(2)
                cat = driver.find_element_by_css_selector('ol[class="products-list"]')
                otp = cat.find_elements_by_css_selector('li[class *="item"]')
                print(len(otp))
                for non in range(len(otp)):
                    try:
                        picker(non)
                    except:
                        sleeper()
                        picker(non)
            except NoSuchElementException:
                pass



        #driver = webdriver.Chrome(r"Chromedriver")
        driver.get("https://www.luckygunner.com")
        sleep(5)

        #driver.find_element_by_css_selector('a[id *="more"]').click()
        oj = driver.find_element_by_css_selector('a[id *="more"]').text == '+ More Handgun Calibers...'
        if oj:
            driver.find_element_by_css_selector('a[id *="more"]').click()
        groups = driver.find_elements_by_css_selector('li[class *="dropdown subcat cat"]')
        boxed = []


        def lamba(d) :

            def sleeper():
                try:
                    peep = driver.find_element_by_css_selector('div[class="page-title"]')
                    sleeping = peep.find_element_by_css_selector('h1').text == "We're Sorry."
                    while sleeping :
                        print('Sleeping')
                        sleep(30)
                        driver.refresh()
                        sleep(2)
                        peep = driver.find_element_by_css_selector('div[class="page-title"]')
                        sleeping = peep.find_element_by_css_selector('h1').text == "We're Sorry."
                except :
                    pass


            def picker(non):
                cat = driver.find_element_by_css_selector('ol[class="products-list"]')
                otp = cat.find_elements_by_css_selector('li[class *="item"]')
                otp[non].find_element_by_css_selector('a').click()
                #print('.')
                box = []

                box.append(opl)
                box.append(opo)
                a = driver.current_url
                box.append(a)
                pil = driver.find_element_by_css_selector('ul[id="imageGallery"]')

                imgs = [i.get_attribute('data-src') for i in pil.find_elements_by_css_selector('li[class *="lslide"]')]
                box.append(imgs)

                name = driver.find_element_by_css_selector('h1[class="product-name"]').text
                box.append(name)

                price = driver.find_element_by_css_selector('div[class *="price"]').text
                box.append(price)

                price2 = driver.find_element_by_css_selector('div[class="col-cprc"]').text
                box.append(price2)

                availability =  driver.find_element_by_css_selector('p[class="availability"]').text
                box.append(availability)

                s_desc = driver.find_element_by_css_selector('div[id="js-short-description-content"]').text

                box.append(s_desc)

                tb = driver.find_element_by_css_selector('table[class="data-table"]')

                th = [i.text for i in tb.find_elements_by_css_selector('th')]
                box.append(th)

                td = [i.text for i in tb.find_elements_by_css_selector('td')]
                box.append(td)
                try:
                    use_type = driver.find_element_by_css_selector('div[class *="product-attribute-use-type-specs"]').text
                except:
                    use_type = ''
                box.append(use_type)

                full_desc = driver.find_element_by_css_selector('div[id="js-col-details"]').text
                box.append(full_desc)
                driver.back()
                sleep(3)
                #print(box)
                boxed.append(box)
                print('.')

            def boxer():
                try:

                    cat = driver.find_element_by_css_selector('ol[class="products-list"]')
                    otp = cat.find_elements_by_css_selector('li[class *="item"]')
                    print(len(otp))
                    for non in range(len(otp)):
                        try:
                            picker(non)
                        except:
                            sleeper()
                            picker(non)
                except NoSuchElementException:
                    pass




            driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)

            driver.get("https://www.luckygunner.com")
            sleep(5)

            #driver.find_element_by_css_selector('a[id *="more"]').click()
            oj = driver.find_element_by_css_selector('a[id *="more"]').text == '+ More Handgun Calibers...'
            if oj:
                driver.find_element_by_css_selector('a[id *="more"]').click()
            groups = driver.find_elements_by_css_selector('li[class *="dropdown subcat cat"]')
            boxed = []

            try:

                groups = driver.find_elements_by_css_selector('li[class *="dropdown subcat cat"]')

                opl = groups[d].find_element_by_css_selector('a').text

                event = groups[d].find_elements_by_css_selector('li')

            except:
                sleeper()
                sleep(2)
                oj = driver.find_element_by_css_selector('a[id *="more"]').text == '+ More Handgun Calibers...'
                if oj:
                    driver.find_element_by_css_selector('a[id *="more"]').click()
                groups = driver.find_elements_by_css_selector('li[class *="dropdown subcat cat"]')

                opl = groups[d].find_element_by_css_selector('a').text

                event = groups[d].find_elements_by_css_selector('li')
            box  = [k.get_attribute('href') for i in event for k in i.find_elements_by_css_selector('a')]
            box = [i for i in box if len(i.split('/')) > 4]
            print(len(box))
            for j in box :

                try:
                    driver.get(j+'?limit=all')  
                    sleep(2)
                    opo = driver.find_element_by_css_selector('div[class="category-title"]').text
                    boxer()
                except :
                    sleeper()
                    driver.get(j+'?limit=all')
                    sleep(2)
                    opo = driver.find_element_by_css_selector('div[class="category-title"]').text
                    boxer()

                print(opo)

            return boxed

        [(i, j) for i, j in enumerate(groups)]



        ping = Parallel(n_jobs= 6 )(delayed(lamba)(bad) for bad,lost in enumerate(groups)) #ex

        from copy import deepcopy

        baba = deepcopy(ping)

        import itertools

        boxed = (list(itertools.chain.from_iterable(ping)))

        pd.DataFrame(boxed)

        df = pd.DataFrame(boxed)

        df.to_csv(dpath +'boxed.csv')

        df.head()

        def vion(test_keys,test_values) :
            teset_values = deepcopy(test_values)
            res = {}
            for key in test_keys:
                for value in teset_values:
                    res[key] = value
                    teset_values.remove(value)
                    break  
            return res

        images = pd.DataFrame(df[3].to_list())

        images.columns = ['image' + str(i) for i in range(1,images.shape[1] + 1)]

        poll = df[[9,10]].apply(lambda x: vion(x[9], x[10]),axis =1)

        poll

        pd.json_normalize(poll).columns

        police = pd.json_normalize(poll)

        police.head()

        df.head(1)

        rest = df[[0,1,2,4,5,6,7,8,11,12]]

        rest.columns = ['Category','Type','Url','Product Name','Price','Price_per_Round','Stock','Short Description','Use Type','Full Description']

        df2 = rest.join(police)

        df3 = df2.join(images)

        df3.columns

        df3  = df3.rename(columns = {'Price': 'Original Price'})

        df3['Regular Price'] = df3['Original Price'].apply(lambda x: x.split('\n')[0].strip('regular price: '))

        df3['Special Price']   =  df3['Original Price'].apply(lambda x: x.split('\n')[1] if len(x.split('\n')) > 2  else np.nan)

        df3['Availablility'] = df3['Stock'].apply(lambda x: x.split('\n')[1])
        df3['Stock'] = df3['Stock'].apply(lambda x: x.split('\n')[0])

        df3['Use Type'] = df3['Use Type'].apply(lambda x: ', '.join(x.split('\n')[1:]))

        df3['Price_per_Round'] = df3['Price_per_Round'].str.strip('()per round')

        df3.columns

        new = df3.copy()

        reorg = new[[  'Regular Price', 'Special Price', 'Price_per_Round', 'Availablility',
               'Quantity', 'Stock','Cost Per Round',]]

        new = new.drop(columns = reorg.columns )

        new[reorg.columns ] = reorg

        new.to_excel(dpath+ 'Fresh_Lucky.xlsx',index=False)

        try:

            old = pd.read_excel(dpath+ 'Newly_Updated_Lucky.xlsx')
        

            old = old.drop(columns = ['Original Price'])

            old.columns

            from datetime import date



            old.columns

            for i in new.columns:
                new[i] = new[i].astype(str)

            for i in old.columns:
                old[i] = old[i].astype(str)

            

            lamb = new.merge(old, on = 'Url' ,how='outer' , )

            tbd = [i for i in lamb if i.endswith('_y')]

            lamb = lamb.drop(columns = tbd)

            aa = [i for i in lamb if i.endswith('_x')]

            aaa = [i.replace('_x','') for i in lamb if i.endswith('_x')]

            lamb = lamb.rename(columns = dict(zip(aa,aaa)))
        except:
            lamb = df3


        lamb


        lamb.shape

        td = str(date.today())



        lamb = lamb.rename(columns = {'Regular Price':'Regular Price '+td,'Special Price':'Special Price '+td,'Price_per_Round':'Price_per_Round '+td,'Quantity':'Quantity '+td,'Stock':'Stock '+td,
                                    'Availablility':'Availablility '+td,'Cost Per Round':'Cost Per Round '+td})

        lamb.shape

        lamb = lamb.loc[:,~lamb.columns.duplicated()]

        lamb.to_excel(dpath+ 'Newly_Updated_Lucky.xlsx',index=False)
        
        showinfo(message= 'The Progress has been Completed')
        
    except:
        showinfo(message= 'The Progress has been Interrupted')


# In[5]:


def freedom():
    
    try :

        driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)
        driver.delete_all_cookies()
        #driver = webdriver.Chrome(r"Chromedriver")
        driver.get("https://www.freedommunitions.com/ammunition.html")
        sleep(5)

        age = driver.find_element_by_css_selector('div[class="age-action"]')

        age.find_element_by_css_selector('button[class="primary"]').click()

        #driver.find_element_by_xpath('//*[@id="narrow-by-list"]/div[1]/div[1]').fi

        #driver.find_element_by_css_selector('div[class="filter-options-content"]').click()

        driver.get("https://www.freedommunitions.com/ammunition.html")
        sleep(8)
        groups = driver.find_elements_by_css_selector('ul[class="items items-children level-1 -folding"]')

        len(groups)

        import time

        def picker(non):
            cat = driver.find_elements_by_css_selector('a[class="product-item-link"]')
            cat[non].click()
            box = []
            print('s')
            timeout = time.time() + 20   # 5 minutes from now
            while True:

                if driver.current_url  or time.time() > timeout:
                    if time.time() > timeout :
                        print('x')
                        fgdffd
                        sleep(4)
                        print('xx')
                    else:
                        url = driver.current_url
                        print('ss')
                        break


            box.append(pol)
            box.append(opo)                                          
            box.append(url)
            sleep(3)

            while True:
                try:
                    joko = driver.find_element_by_css_selector('div[class="fotorama__stage__frame fotorama__active fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img"]')
                    break
                except: 
                    try:
                        sleep(15)
                        joko = driver.find_element_by_css_selector('div[class="fotorama__stage__frame fotorama__active fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img"]')
                        break
                    except:
                        if driver.current_url == 'https://www.freedommunitions.com/' :
                            break
                        else:
                            driver.refresh()
                            sleep(10)
                            print('l')
                            pass
            if driver.current_url == 'https://www.freedommunitions.com/' :
                boxed.append([])
            else:

                img = joko.get_attribute('href')
                box.append(img)
                name = driver.find_element_by_css_selector('h1[class="page-title"]').text
                box.append(name)
                try:
                    price = driver.find_element_by_css_selector('span[class="price-total"]').text
                except:
                    price = driver.find_element_by_css_selector('span[class="price-wrapper "]').text
                box.append(price)
                try:
                    price2 = driver.find_element_by_css_selector('span[class="regular-price"]').text
                except:
                    price2 = ''
                box.append(price2)

                try:
                    rounds = driver.find_element_by_css_selector('label[for ="qty"]').text
                except:
                    rounds = ''
                box.append(rounds)
                try:
                    availability =  driver.find_element_by_css_selector('div[class="custom-available-qty"]').text
                except:
                    availability = ''
                box.append(availability)

                try:
                    s_desc = driver.find_element_by_css_selector('div[class="value show-more-height"]').text
                except:
                    s_desc = ''

                box.append(s_desc)
                try:
                    tb = driver.find_element_by_css_selector('table[class="data table additional-attributes"]')

                    th = [i.text for i in tb.find_elements_by_css_selector('th')]
                    box.append(th)

                    td = [i.text for i in tb.find_elements_by_css_selector('td')]
                except:
                    td = []
                box.append(td)

                try:
                    full_desc = driver.find_element_by_css_selector('div[class="value"]').text
                except:
                    full_desc = ''
                box.append(full_desc)
                driver.back()
                sleep(3)
                #print(box)
                boxed.append(box)

        def boxer():
            sleep(2)
            bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
            bro.find_element_by_css_selector('option[value="200"]').click()
            mn = driver.find_element_by_css_selector('option[selected="selected"]').text
            while mn != '200' :
                driver.refresh()
                sleep(2)
                bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
                bro.find_element_by_css_selector('option[value="200"]').click()
                mn = driver.find_element_by_css_selector('option[selected="selected"]').text
            sleep(3)
            print(driver.find_element_by_css_selector('span[class="toolbar-number"]').text)
            sleep(2)
            cat = driver.find_elements_by_css_selector('a[class="product-item-link"]')
            for non in range(len(cat)):
                try:
                    picker(non)
                except:
                    sleep(5)
                    driver.back()

                    sleep(5)
                    picker(non)


        def lamba(d) :
            def picker(non):
                cat = driver.find_elements_by_css_selector('a[class="product-item-link"]')
                cat[non].click()
                box = []
                print('s')
                timeout = time.time() + 20   # 5 minutes from now
                while True:

                    if driver.current_url  or time.time() > timeout:
                        if time.time() > timeout :
                            print('x')
                            fgdffd
                            sleep(4)
                            print('xx')
                        else:
                            url = driver.current_url
                            print('ss')
                            break


                box.append(pol)
                box.append(opo)                                          
                box.append(url)
                sleep(3)

                while True:
                    try:
                        joko = driver.find_element_by_css_selector('div[class="fotorama__stage__frame fotorama__active fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img"]')
                        break
                    except: 
                        try:
                            sleep(15)
                            joko = driver.find_element_by_css_selector('div[class="fotorama__stage__frame fotorama__active fotorama_vertical_ratio fotorama__loaded fotorama__loaded--img"]')
                            break
                        except:
                            if driver.current_url == 'https://www.freedommunitions.com/' :
                                break
                            else:
                                driver.refresh()
                                sleep(10)
                                print('l')
                                pass
                if driver.current_url == 'https://www.freedommunitions.com/' :
                    boxed.append([])
                else:

                    img = joko.get_attribute('href')
                    box.append(img)
                    name = driver.find_element_by_css_selector('h1[class="page-title"]').text
                    box.append(name)
                    try:
                        price = driver.find_element_by_css_selector('span[class="price-total"]').text
                    except:
                        price = driver.find_element_by_css_selector('span[class="price-wrapper "]').text
                    box.append(price)
                    try:
                        price2 = driver.find_element_by_css_selector('span[class="regular-price"]').text
                    except:
                        price2 = ''
                    box.append(price2)

                    try:
                        rounds = driver.find_element_by_css_selector('label[for ="qty"]').text
                    except:
                        rounds = ''
                    box.append(rounds)
                    try:
                        availability =  driver.find_element_by_css_selector('div[class="custom-available-qty"]').text
                    except:
                        availability = ''
                    box.append(availability)

                    try:
                        s_desc = driver.find_element_by_css_selector('div[class="value show-more-height"]').text
                    except:
                        s_desc = ''

                    box.append(s_desc)
                    try:
                        tb = driver.find_element_by_css_selector('table[class="data table additional-attributes"]')

                        th = [i.text for i in tb.find_elements_by_css_selector('th')]
                        box.append(th)

                        td = [i.text for i in tb.find_elements_by_css_selector('td')]
                    except:
                        td = []
                    box.append(td)

                    try:
                        full_desc = driver.find_element_by_css_selector('div[class="value"]').text
                    except:
                        full_desc = ''
                    box.append(full_desc)
                    driver.back()
                    sleep(3)
                    #print(box)
                    boxed.append(box)

            def boxer():
                sleep(2)
                bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
                bro.find_element_by_css_selector('option[value="200"]').click()
                mn = driver.find_element_by_css_selector('option[selected="selected"]').text
                while mn != '200' :
                    driver.refresh()
                    sleep(2)
                    bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
                    bro.find_element_by_css_selector('option[value="200"]').click()
                    mn = driver.find_element_by_css_selector('option[selected="selected"]').text
                sleep(3)
                print(driver.find_element_by_css_selector('span[class="toolbar-number"]').text)
                sleep(2)
                cat = driver.find_elements_by_css_selector('a[class="product-item-link"]')
                for non in range(len(cat)):
                    try:
                        picker(non)
                    except:
                        sleep(5)
                        driver.back()

                        sleep(5)
                        picker(non)





            driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)
            driver.delete_all_cookies()


            driver.get("https://www.freedommunitions.com/ammunition.html")
            sleep(8)
            try:
                age = driver.find_element_by_css_selector('div[class="age-action"]')

                age.find_element_by_css_selector('button[class="primary"]').click()
            except:
                pass
            groups = driver.find_elements_by_css_selector('ul[class="items items-children level-1 -folding"]')

            event = groups[d].find_elements_by_css_selector('li[class="item     -is-expanded   -filter-parent "]')

            box = [k.get_attribute('href') for i in event for k in i.find_elements_by_css_selector('a')]
            boxed = []
            for j in range(len(box)) :

                driver.get(box[j])
                sleep(2)
                try:
                    pol = driver.find_elements_by_css_selector('li[class *="item category"]')[-2].find_element_by_css_selector('a').get_attribute('innerHTML')
                except:
                    pol = driver.find_element_by_xpath('//*[@id="html-body"]/div[2]/div[2]/ul/li[3]').text
                opo = driver.find_element_by_css_selector('h1[class="page-title"]').text
                print(pol,opo)
                boxer()
            return boxed


        from joblib import Parallel, delayed

        import dill as pickle
        ping = Parallel(n_jobs= 4 )(delayed(lamba)(bad) for bad,lost in enumerate(groups[:4])) #ex

        boxed = ping.copy()

        boxed = list(itertools.chain.from_iterable(boxed))

        driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)
        driver.delete_all_cookies()


        driver.get("https://www.freedommunitions.com/gear.html")

        sleep(4)
        try:
            age = driver.find_element_by_css_selector('div[class="age-action"]')

            age.find_element_by_css_selector('button[class="primary"]').click()
        except:
            pass
        groups = driver.find_elements_by_css_selector('ul[class="items items-children level-1 -folding"]')
        for d in range(len(groups)) :


            driver.get("https://www.freedommunitions.com/gear.html")
            sleep(8)
            groups = driver.find_elements_by_css_selector('ul[class="items items-children level-1 -folding"]')

            event = groups[d].find_elements_by_css_selector('li[class="item     -is-expanded   -filter-parent "]')

            box = [k.get_attribute('href') for i in event for k in i.find_elements_by_css_selector('a')]

            for j in range(len(box)) :

                driver.get(box[j])
                sleep(2)
                try:
                    pol = driver.find_elements_by_css_selector('li[class *="item category"]')[-2].find_element_by_css_selector('a').get_attribute('innerHTML')
                except:
                    pol = driver.find_element_by_xpath('//*[@id="html-body"]/div[2]/div[2]/ul/li[3]').text
                opo = driver.find_element_by_css_selector('h1[class="page-title"]').text
                print(pol,opo)

                sleep(3)
                bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
                bro.find_element_by_css_selector('option[value="200"]').click()
                mn = driver.find_element_by_css_selector('option[selected="selected"]').text
                while mn != '200' :
                    driver.refresh()
                    sleep(15)
                    bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
                    bro.find_element_by_css_selector('option[value="200"]').click()
                    mn = driver.find_element_by_css_selector('option[selected="selected"]').text
                sleep(3)
                print(driver.find_element_by_css_selector('span[class="toolbar-number"]').text)
                sleep(2)
                cat = driver.find_elements_by_css_selector('a[class="product-item-link"]')
                for non in range(len(cat)):
                    try:
                        picker(non)
                    except:
                        sleep(5)
                        driver = webdriver.Chrome( executable_path=r"Chromedriver", 
                                  options=chrome_options)
                        driver.delete_all_cookies()
                        driver.get(box[j])
                        sleep(2)
                        try:
                            age = driver.find_element_by_css_selector('div[class="age-action"]')

                            age.find_element_by_css_selector('button[class="primary"]').click()
                        except:
                            pass
                        try:
                            pol = driver.find_element_by_xpath('//*[@id="html-body"]/div[2]/div[3]/ul/li[3]').text
                        except:
                            pol = driver.find_element_by_xpath('//*[@id="html-body"]/div[2]/div[2]/ul/li[3]').text
                        opo = driver.find_element_by_css_selector('h1[class="page-title"]').text
                        print(pol,opo)

                        sleep(3)
                        bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
                        bro.find_element_by_css_selector('option[value="200"]').click()
                        mn = driver.find_element_by_css_selector('option[selected="selected"]').text
                        while mn != '200' :
                            driver.refresh()
                            sleep(5)
                            bro = driver.find_element_by_css_selector('select[class="limiter-options"]')
                            bro.find_element_by_css_selector('option[value="200"]').click()
                            mn = driver.find_element_by_css_selector('option[selected="selected"]').text
                        sleep(3)
                        print(driver.find_element_by_css_selector('span[class="toolbar-number"]').text)
                        sleep(2)
                        cat = driver.find_elements_by_css_selector('a[class="product-item-link"]')

                        sleep(5)
                        picker(non)

        from copy import deepcopy

        bb = deepcopy(boxed)

        pd.DataFrame(boxed)

        df = pd.DataFrame(boxed)

        df.to_csv('boxed_freedom2.csv')

        df.head()

        def vion(test_keys,test_values) :
            teset_values = deepcopy(test_values)
            res = {}
            for key in test_keys:
                for value in teset_values:
                    res[key] = value
                    teset_values.remove(value)
                    break  
            return res

        df = df.dropna(subset = [10])

        df.shape

        poll = df[[10,11]].apply(lambda x: vion(x[10], x[11]),axis =1)

        poll

        pd.json_normalize(poll).columns

        police = pd.json_normalize(poll)

        police.head()

        df.head(1)

        rest = df[[0,1,2,3,4,5,6,7,8,9,12]]

        rest.columns = ['Categories','Subcategory','Url','Images','Product Name','Price','Price_per_Round','Quantity','Stock','Short Description','Full Description']

        df2 = rest.join(police)

        df2.columns

        df2

        df2['Availablility'] = df2['Stock'].apply(lambda x: ' '.join(x.split(' ')[1:]))
        df2['Stock'] = df2['Stock'].apply(lambda x: x.split(' ')[0])

        df2.columns

        df2 = df2.rename(columns = {'BULLET WEIGHT':'Bullet Weight','CALIBER':'Ammo Caliber','CASING TYPE':'Ammo Casing','MANUFACTURER':'MANUFACTURER','SKU':'Manufacturer SKU','VELOCITY AVG':'Muzzle Velocity (fps)'})

        df2.iloc[:,:15]

        df2['Price_per_Round']  =  df2['Price_per_Round'].apply(lambda x: x.split('\n')[0])

        df2['Quantity'] = df2['Quantity'].str.extract('(\d+)')

        new = df2.copy()

        reorg = new[[ 'Price',
               'Price_per_Round', 'Quantity', 'Stock', 'Availablility']]

        new = new.drop(columns = reorg.columns )

        new[reorg.columns ] = reorg

        new.to_excel(dpath+ 'Fresh_Freedom.xlsx',index=False)


        try:

            old = pd.read_excel(dpath+ 'Newly_updated_freedom.xlsx')

            old.columns

            from datetime import date

            old.columns

            #new = new.fillna('')

            new

            for i in new.columns:
                new[i] = new[i].astype(str)

            for i in old.columns:
                old[i] = old[i].astype(str)

            old[['Short Description', 'Full Description',]]  = old[['Short Description', 'Full Description',]].replace('nan','')
            new[['Short Description', 'Full Description',]]  = new[['Short Description', 'Full Description',]].replace('nan','')
            old[['Short Description', 'Full Description',]]  = old[['Short Description', 'Full Description',]].replace('None','')
            new[['Short Description', 'Full Description',]]  = new[['Short Description', 'Full Description',]].replace('None','')





            lamb = new.merge(old, on =  [ 'Url' ],how='outer' , )

            tbd = [i for i in lamb if i.endswith('_y')]

            lamb = lamb.drop(columns = tbd)

            aa = [i for i in lamb if i.endswith('_x')]

            aaa = [i.replace('_x','') for i in lamb if i.endswith('_x')]

            lamb = lamb.rename(columns = dict(zip(aa,aaa)))
        except:
            lamb = df3
        lamb

        lamb.columns

        lambo = lamb.copy()

        reorg = lambo[[ 'Price',
               'Price_per_Round', 'Quantity', 'Stock', 'Availablility']]

        lambo = lambo.drop(columns = reorg.columns )

        lambo[reorg.columns ] = reorg

        td = str(date.today())

        lambo = lambo.rename(columns = {'Price':'Price '+td,'Price_per_Round':'Price_per_Round '+td,'Quantity':'Quantity '+td,'Stock':'Stock '+td,'Availablility':'Availablility '+td,})

        lambo.columns

        lambo.to_excel(dpath+ 'Newly_updated_freedom.xlsx',index=False)
        
        showinfo(message= 'The Progress has been Completed')
        
    except:
        showinfo(message= 'The Progress has been Interrupted')



# %%time
# freedom()
# 
# 
# %%time
# lucky()
# 
# 
# %%time
# ammoo()
# 
# 
# %%time
# trueshot()

# In[6]:


import requests

import urllib.request

from tqdm.notebook import tqdm
tqdm.pandas()

import dropbox, sys, os
#tok = 'sl.BQzOy915S8p3htnQVCvqLW4uzb5GHm6JV-EatO0naENdVION17k-yEuyrGVtBiT9P0ZKhI4o6p8rDb0-W2nJXrVScGU4UQp8jgSiq99gYHqPgPGCqYkgjmrKy9iqHVHxZo3qtx5ihBrI'
#dbx = dropbox.Dropbox(tok)

# from config.dev import CONTENT_IMAGE_UPLOAD
headers = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36"}
    


# In[7]:


def starch(a,b,bingo,num):
    print('l')
    tok = token_var.get()
    dbx = dropbox.Dropbox(tok,ca_certs="trusted-certs.crt")
    try :
        b = b.replace('*','')
        b = b.replace('"','')
        b = b.replace('/','__')
        if num == 0:
            numx = ''
        else:
            numx = '_' + str(num)
        pra = bingo+ b+ numx + '.jpg'

        if not os.path.isfile(pra) :
            print('a')
            try:
                if a.startswith('http'):
                    a = a
                else:
                    a = 'https:' + a
                resp = requests.get(a, headers=headers,timeout=40).content
                with open(pra, "wb") as f:
                    f.write(resp)
                print("image is saved")
            except Exception as e:
                print(e)
            print('aa')
            file_path = pra
            dest_path = os.path.join('/' +pra)
            dest_path = dest_path.replace(dpath,"")
            print ('Uploading %s to %s' % (file_path, dest_path))
            with open(file_path ,'rb') as f:
                print('aaa')
                dbx.files_upload(f.read(), dest_path, mute=True)
                print('aaaa')
            look = dbx.sharing_create_shared_link(dest_path).url

        else :
            try:
                print('Found')
                file_path = pra
                dest_path = os.path.join('/'+pra)
                dest_path = dest_path.replace(dpath,'')
                print('s')
                look = dbx.sharing_create_shared_link(dest_path).url
            except:
                try:
                    if a.startswith('http'):
                        a = a
                    else:
                        a = 'https:' + a
                    resp = requests.get(a, headers=headers,timeout=40).content
                    with open(pra, "wb") as f:
                        f.write(resp)
                    print("image is saved")
                except Exception as e:
                    print(e)
                file_path = pra
                dest_path = os.path.join('/' +pra)
                dest_path = dest_path.replace(dpath,"")
                print ('Uploading %s to %s' % (file_path, dest_path))
                with open(file_path ,'rb') as f:
                    dbx.files_upload(f.read(), dest_path, mute=True)
                look = dbx.sharing_create_shared_link(dest_path).url
                
    except:
        sleep(10)
        print('sleeping')
        b = b.replace('*','')
        b = b.replace('"','')
        b = b.replace('/','__')
        if num == 0:
            numx = ''
        else:
            numx = '_' + str(num)
        pra = bingo+ b+ numx + '.jpg'

        if not os.path.isfile(pra) :
            print('a')
            try:
                if a.startswith('http'):
                    a = a
                else:
                    a = 'https:' + a
                resp = requests.get(a, headers=headers,timeout=40).content
                with open(pra, "wb") as f:
                    f.write(resp)
                print("image is saved")
            except Exception as e:
                print(e)
            print('aa')
            file_path = pra
            dest_path = os.path.join('/' +pra)
            dest_path = dest_path.replace(dpath,"")
            print ('Uploading %s to %s' % (file_path, dest_path))
            with open(file_path ,'rb') as f:
                print('aaa')
                dbx.files_upload(f.read(), dest_path, mute=True)
                print('aaaa')
                
            try:
                look = dbx.sharing_create_shared_link(dest_path).url
            except Exception as e:
                showinfo(message= e)   

        else :
            try:
                #print('Found')
                file_path = pra
                dest_path = os.path.join('/'+pra)
                dest_path = dest_path.replace(dpath,"")
                look = dbx.sharing_create_shared_link(dest_path).url
            except:
                try:
                    if a.startswith('http'):
                        a = a
                    else:
                        a = 'https:' + a
                    resp = requests.get(a, headers=headers,timeout=40).content
                    with open(pra, "wb") as f:
                        f.write(resp)
                    print("image is saved")
                except Exception as e:
                    print(e)
                file_path = pra
                dest_path = os.path.join('/' +pra)
                dest_path = dest_path.replace(dpath,"")
                print ('Uploading %s to %s' % (file_path, dest_path))
                with open(file_path ,'rb') as f:
                    dbx.files_upload(f.read(), dest_path, mute=True)
                try:
                    look = dbx.sharing_create_shared_link(dest_path).url
                except Exception as e:
                    showinfo(message= e)


        

    return look


# In[9]:


def swap_ammoo():
    try:

        a = pd.read_excel(dpath+ 'Newly_Updated_Amoo.xlsx',na_values=['None','nan','na'])
        b = [i for i in a.columns if i.startswith('imag')]
        i = 0
        a[b[i]] = a.apply(lambda x: starch(x[b[i]],x['Product Name'],dpath+'Ammo/' ,i),axis=1)

        a.to_excel(dpath+ 'Newly_Updated_Amoo.xlsx',index=False)
        showinfo(message= 'The Progress has been Completed')
    except:
        showinfo(message= 'The Progress has been Interrupted')




# In[10]:


def swap_freedom():
    try:
        sr = pd.read_excel(dpath+ 'Newly_updated_freedom.xlsx',na_values=['None','nan','na'])

        sr = sr.dropna(subset = ['Product Name'])

        b = [i for i in sr if i.startswith('Imag')]

        for i in range(len(b)) :
            sr[b[i]] = sr.apply(lambda x: starch(x[b[i]],x['Product Name'],dpath+'Freedom/' ,i),axis=1)

        sr.to_excel(dpath+ 'Newly_updated_freedom.xlsx',index=False)
        showinfo(message= 'The Progress has been Completed')
        
    except:
        showinfo(message= 'The Progress has been Interrupted')


# In[ ]:





# In[11]:


def swap_lucky():
    try:
        dr = pd.read_excel(dpath+ 'Newly_Updated_Lucky.xlsx',na_values=['None','nan','na'])

        b = [i for i in dr if i.startswith('imag')]

        for i in range(len(b)) :
            dr.loc[dr[b[i]].notna(),b[i]] = dr.loc[dr[b[i]].notna()].apply(lambda x: starch(x[b[i]],x['Product Name'],dpath+'Lucky/' ,i),axis=1)

        dr.to_excel(dpath+ 'Newly_Updated_Lucky.xlsx',index=False)
        showinfo(message= 'The Progress has been Completed')
    except:
        showinfo(message= 'The Progress has been Interrupted')


# In[12]:


def swap_trueshot():
    try:
        tt = pd.read_excel(dpath+ 'Newly_Updated_Trueshot.xlsx',na_values=['None','nan','na'])

        b = [i for i in tt if i.startswith('imag')]

        for i in range(len(b)) :
            tt.loc[tt[b[i]].notna(),b[i]] = tt.loc[tt[b[i]].notna()].apply(lambda x: starch(x[b[i]],x['Product Name'],dpath+'Trueshot/' ,i),axis=1)

        tt.to_excel(dpath+ 'Newly_Updated_Trueshot.xlsx',index=-False)
        showinfo(message= 'The Progress has been Completed')
    except:
        showinfo(message= 'The Progress has been Interrupted')


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[13]:


import threading
import sys
stop_event = threading.Event()
import time

def run_freedom():
    execute_thread = threading.Thread(target=print_cf)
    execute_thread.start()


def print_cf(event = None):

    pb.start()
    freedom()
    pb.stop()
    
def run_lucky():
    execute_thread = threading.Thread(target=print_cl)
    execute_thread.start()


def print_cl(event = None):

    pb1.start()
    lucky()
    pb1.stop()
    
    
def run_ammoo():
    execute_thread = threading.Thread(target=print_ca)
    execute_thread.start()


def print_ca(event = None):

    pb2.start()
    ammoo()
    pb2.stop()
    

def run_trueshot():
    execute_thread = threading.Thread(target=print_ct)
    execute_thread.start()


def print_ct(event = None):

    pb3.start()
    trueshot()
    pb3.stop()
    
def run_all():
    execute_thread = threading.Thread(target=print_call)
    execute_thread.start()


def print_call(event = None):

    pb4.start()
    freedom()
    lucky()
    ammoo()
    #trueshot()
    pb4.stop()
  
def run_swapfreedom():
    execute_thread = threading.Thread(target=print_csf)
    execute_thread.start()


def print_csf(event = None):

    pb5.start()
    swap_freedom()
    pb5.stop()

    
    
def run_swaplucky():
    execute_thread = threading.Thread(target=print_csl)
    execute_thread.start()


def print_csl(event = None):

    pb6.start()
    swap_lucky()
    pb6.stop()

def run_swapammoo():
    execute_thread = threading.Thread(target=print_csa)
    execute_thread.start()


def print_csa(event = None):

    pb7.start()
    swap_ammoo()
    pb7.stop()
    

def run_swaptrue():
    execute_thread = threading.Thread(target=print_cst)
    execute_thread.start()


def print_cst(event = None):

    pb8.start()
    swap_trueshot()
    pb8.stop()

    
def run_swapall():
    execute_thread = threading.Thread(target=print_swall)
    execute_thread.start()


def print_swall(event = None):

    pb9.start()
    swap_freedom()
    swap_lucky()
    swap_ammoo()
    swap_trueshot()
    pb9.stop()

       
def stop():
    pb.stop()
    pb1.stop()
    pb2.stop()
    pb3.stop()
    pb4.stop()
    pb5.stop()
    pb6.stop()
    pb7.stop()
    pb8.stop()
    pb9.stop()
    sys.exit()


# In[27]:



from tkinter import ttk
import tkinter as tk
from time import sleep
from tkinter.messagebox import showinfo

driver = None
# root window
root = tk.Tk()
root.geometry('700x600')
root.title('Scraper!!!')


token_var =tk.StringVar()



# creating a label for
# name using widget Label
name_label = tk.Label(root, text = 'Insert DropBox Token', font=('calibre',10, 'bold'))
  
# creating a entry for input
# name using widget Entry
name_entry = tk.Entry(root,textvariable = token_var, font=('calibre',10,'normal'))

name_label.grid(row=60,column=0)
name_entry.grid(row=60,column=2, columnspan = 2, sticky = tk.W+tk.E)
###Freedom

# progressbar
pb = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb.grid(column=0, row=0, columnspan=2, padx=10, pady=20)


download = ttk.Button(
    root,
    text='Update Freedom ',
    command = run_freedom
)
download.grid(column=0, row=2, padx=3, pady=5,)





##Lucky
download = ttk.Button(
    root,
    text='Update Lucky ',
    command = run_lucky
)
download.grid(column=0, row=6, padx=3, pady=5,)




# progressbar
pb1 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb1.grid(column=0, row=4, columnspan=2, padx=10, pady=20)



##Update Ammo

download = ttk.Button(
    root,
    text='Update Ammo ',
    command = run_ammoo
)
download.grid(column=0, row=10, padx=3, pady=5,)




# progressbar
pb2 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb2.grid(column=0, row=8, columnspan=2, padx=10, pady=20)





##Trueshot

download = ttk.Button(
    root,
    text='Update Trueshot ',
    command = run_trueshot
)
download.grid(column=0, row=14, padx=3, pady=5,)


# progressbar
pb3 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb3.grid(column=0, row=12, columnspan=2, padx=10, pady=20)




##ALL

download = ttk.Button(
    root,
    text='Update ALL ',
    command = run_all
    
)
download.grid(column=0, row=20, padx=3, pady=5,)



# progressbar
pb4 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb4.grid(column=0, row=18, columnspan=2, padx=10, pady=20)

#################################




download = ttk.Button(
    root,
    text='Swap FreedomUrl',
    command = run_swapfreedom
)
download.grid(column=2, row=2, padx=3, pady=5,)



# progressbar
pb5 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb5.grid(column=2, row=0, columnspan=2, padx=10, pady=20)



download = ttk.Button(
    root,
    text='Swap LuckyUrl',
    command = run_swaplucky
)
download.grid(column=2, row=6, padx=3, pady=5,)



# progressbar
pb6 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb6.grid(column=2, row=4, columnspan=4, padx=10, pady=20)



download = ttk.Button(
    root,
    text='Swap AmmooUrl',
    command = run_swapammoo
)
download.grid(column=2, row=10, padx=3, pady=5,)



# progressbar
pb7 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb7.grid(column=2, row=8, columnspan=2, padx=10, pady=20)



download = ttk.Button(
    root,
    text='Swap TrueshotUrl',
    command = run_swaptrue
)
download.grid(column=2, row=14, padx=3, pady=5,)



# progressbar
pb8 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb8.grid(column=2, row=12, columnspan=2, padx=10, pady=20)



download = ttk.Button(
    root,
    text='Swap AllUrl',
    command = run_swapall
)
download.grid(column=2, row=20, padx=3, pady=5,)



# progressbar
pb9 = ttk.Progressbar(
    root,
    orient='horizontal',
    mode='indeterminate',
    length=280
)
# place the progressbar
pb9.grid(column=2, row=18, columnspan=2, padx=10, pady=20)





stopz = ttk.Button(
    root,
    text='  STOP ',
    command = stop
)
stopz.grid(column=0, row=50,columnspan=4,rowspan =4, padx=10, pady=10,)


root.mainloop()


# In[ ]:





# In[ ]:




