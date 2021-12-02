from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
import json

driver = webdriver.Firefox()

# List of Page
ListOfPages = ["https://www.facebook.com/ThePoliticalBroOfficial/photos/?ref=page_internal"]

counter = 0
posts = dict()

for page in ListOfPages:
    # Loading the page
    driver.get(page)

    # Scrolling to the bottom of page
    last_height = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
        time.sleep(5)
        curr_height = driver.execute_script("return document.body.scrollHeight")
        if(curr_height>last_height):
            last_height = curr_height
        else:
            break

    # Finding posts
    elem = driver.find_elements_by_xpath("//div[@class=' _2eea']//a[1]")

    List_Of_Posts = []

    if len(elem)>0:
        for e in elem:
            if e.get_attribute('href') is not None and e.get_attribute('href').split('/')[-1]=="?type=3":
                List_Of_Posts.append(e.get_attribute('href'))

    else:
        elem = driver.find_elements_by_xpath("//a[@role='link']")
        for e in elem:
            if e.get_attribute('href') is not None and e.get_attribute('href')[-6:]=='type=3':
                List_Of_Posts.append(e.get_attribute('href'))

    # Downloading image and caption for each post
    for post in List_Of_Posts:
        driver.get(post)
        time.sleep(5)

        caption_elem = driver.find_elements_by_xpath("//div[@class='a8nywdso j7796vcc rz4wbd8a l29c1vbm']//span[@class='d2edcug0 hpfvmrgz qv66sw1b c1et5uql b0tq1wua a8c37x1j keod5gw0 nxhoafnm aigsh9s9 d9wwppkn fe6kdd0r mau55g9w c8b282yb hrzyx87i jq4qci2q a3bd9o3v b1v8xokw oo9gr5id']")
        caption = ""
        if len(caption_elem)>0:
            caption = caption_elem[0].text

        elem = driver.find_elements_by_xpath("//img[@data-visualcompletion = 'media-vc-image']")
        elem = driver.find_elements_by_tag_name("img")

        posts[post] = {"Seq":counter, "Caption":caption}
        elem[0].screenshot("Images/{}.png".format(counter))
        counter += 1

# Saving captions in JSON file
with open("Posts.json", "w") as outfile:
    json.dump(posts, outfile)

# Ending Driver
driver.close()