from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
import urllib.request as Request
import os
import time

print("Beginning BingImageSearchDownloader.....")

# initializing chrome instances
browser = webdriver.Chrome("F:\\Drivers\\Chrome\\chromedriver.exe")

# URL for bing image search
Bing_ImageSearch_url = "https://www.bing.com/images/search?q="

img_to_search = "SuperMan"
img_size = ["2mp", "4mp", "6mp", "8mp", "10mp", "12mp", "15mp", "20mp"]
image_quantity_required = 20

# Navigating to the given url by setting img_to_search and its image size.
browser.get(Bing_ImageSearch_url + img_to_search + "&FORM=HDRSC2")

print(browser.title)

# Finding the div tag of first image in the result
first_div_class = browser.find_element_by_xpath("//ul/li/div/div/a/div[@class=\"img_cont hoff\"]")

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
element = WebDriverWait(browser, waitTime).until(EC.presence_of_element_located(
    (By.XPATH, "//img[@class=\"mainImage accessible nofocus\"]")))

# Continue downloading images untill we get required number of images.
while(counter < image_quantity_required):
    if(counter > 1):
        print("Waiting for new image to loaded properly...")
        element = WebDriverWait(browser, waitTime).until(EC.presence_of_element_located(
            (By.XPATH, "//img[@class=\"mainImage accessible nofocus\"]")))
        element = browser.find_element_by_xpath("//img[@class=\"mainImage accessible nofocus\"]")

    # Getting the url of the images's original size.
    img_link = element.get_property("src")
    print(counter, ". ", img_link)

    # Sending image url to net.
    Image = Request.urlopen(img_link).read()
    print("Saving image..")
    fileName = img_to_search + "/" + img_to_search + "_" + str(counter) + ".jpg"
    tempFile = open(fileName, "wb")
    tempFile.write(Image)
    tempFile.close()
    print("Image saved.")
    next_image_btn = browser.find_element_by_xpath("//a[@id=\"iol_navr\"]")
    counter += 1
    print("Conitnue to next image...")

    # Click on "NExt img button.."
    ActionChains(browser).move_to_element(next_image_btn).click(next_image_btn).perform()
    time.sleep(waitTime)

print("Success")
