from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import urllib.request as Request
import os
import time

print("Beginning BingImageSearchDownloader.....")

# initializing chrome instances
browser = webdriver.Chrome("F:\\Drivers\\Chrome\\chromedriver.exe")

# URL for bing image search
Bing_ImageSearch_url = ["https://www.bing.com/images/search?q=",
                        "&qft=+filterui:imagesize-custom"]

img_to_search = "Cool"
img_size = ["_640_480", "_800_600", "_1024_768", "_1600_1200", "_2272_1704", "_2816_2112"]
image_quantity_required = 20

header = {}
header["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"

# Navigating to the given url by setting img_to_search and its image size.
browser.get(Bing_ImageSearch_url[0] + img_to_search + Bing_ImageSearch_url[1]
            + img_size[3])
print(Bing_ImageSearch_url[0] + img_to_search + Bing_ImageSearch_url[1] + img_size[3])
print(browser.title)
img_found = False
while img_found == False:
    try:
        # Finding the div tag of first image in the result
        first_div_class = browser.find_element_by_xpath("//ul/li/div/div/a/div[@class=\"img_cont hoff\"]")
        img_found = True
    except NoSuchElementException:

        # If not image is foound for the given word, thein it will refresh the browser.
        print("No image found.\nRefreshing Page")
        browser.refresh()


# Clicking the the fisrt image in the result.
ActionChains(browser).move_to_element(first_div_class).click(first_div_class).perform()
counter = 1

# Checking if the directory exists or not.If not, then create the directory
# to save images in it.
if(os.path.exists(img_to_search)):
    print("Directory " + str(img_to_search) + " already exists.")
else:
    print("Creating new directory (" + str(img_to_search) + ")")
    os.mkdir(img_to_search)

waitTime = 10

# Waiting for the image original size to appear.

# Continue downloading images untill we get required number of images.
while(counter < image_quantity_required):
    try:
        element = WebDriverWait(browser, waitTime).until(EC.presence_of_element_located(
            (By.XPATH, "//img[@class=\"mainImage accessible nofocus\"]")))
        element = browser.find_element_by_xpath("//img[@class=\"mainImage accessible nofocus\"]")

        # Getting the url of the images's original size.
        img_link = element.get_property("src")
        print(counter, ". ", img_link)

        image_request = Request.Request(img_link, headers=header)

        # Sending image url to net.
        Image = Request.urlopen(image_request).read()
        print("Saving image..")
        fileName = img_to_search + "/" + img_to_search + "_" + str(counter) + ".jpg"
        tempFile = open(fileName, "wb")
        tempFile.write(Image)
        tempFile.close()
        print("Image saved.")
        next_image_btn = browser.find_element_by_xpath("//a[@id=\"iol_navr\"]")
        counter += 1
        print("Conitnue to next image...")

        # Click on "Next img button.."
        ActionChains(browser).move_to_element(next_image_btn).click(next_image_btn).perform()
        time.sleep(5)
    except TimeoutException:
        print("Trying to refresh the page due to TimeoutException.")
        browser.refresh()

print("Success")
