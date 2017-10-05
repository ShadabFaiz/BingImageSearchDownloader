from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import urllib.request as Request
import os

print("Beginning BingImageSearchDownloader.....")

# initializi    ng chrome instances
browser = webdriver.Chrome("F:\\Drivers\\Chrome\\chromedriver.exe")
header = {}
img_size = ["_640_480", "_800_600", "_1024_768", "_1600_1200", "_2272_1704", "_2816_2112"]
waitTime = 10


def saveError_To_TxtFile(error):
    errorFile = open("./logs.txt", "a")
    errorFile.write(error+"\n")
    errorFile.close()


def setHeader():
    header["User-Agent"] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64)AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36"


def searchImage(img_to_search, Bing_ImageSearch_url, size):
    # Navigating to the given url by setting img_to_search and its image size.
    browser.get(Bing_ImageSearch_url[0] + img_to_search + Bing_ImageSearch_url[1]
                + img_size[size])
    print(browser.title)
    img_found = False
    refresh_counter = 10
    while (img_found is not True):
        try:
            # Finding the div tag of first image in the result
            first_div_class = browser.find_element_by_xpath("//ul/li/div/div/a/div"
                                                            + "[@class=\"img_cont hoff\"]")
            img_found = True
        except NoSuchElementException:
            # If refresh counter reaches to zero,then exit the program.
            if(refresh_counter == 0):
                print("Could not found any images for ", img_to_search)
                break
            else:
                browser.refresh()
                refresh_counter -= 1

    return img_found, first_div_class


def get_OriginalImageLink():
    refresh_counter = 5
    link = "null"
    while(link == "null" and refresh_counter > -1):
        try:
            element = WebDriverWait(browser, waitTime).until(EC.presence_of_element_located(
                (By.XPATH, "//img[@class=\"mainImage accessible nofocus\"]")))
            element = browser.find_element_by_xpath("//img[@class=\"mainImage accessible nofocus\"]")
            link = element.get_property("src")
        except TimeoutException:
            print("Trying to refresh the page due to TimeoutException.")
            browser.refresh()
            refresh_counter -= 1
    return link


# Checking if the directory exists or not.If not, then create the directory
# to save images in it.
def createDirectory(img_to_search):
    if(os.path.exists("./"+img_to_search)):
        print("Directory " + str(img_to_search) + " already exists.")
    else:
        print("Creating new directory (" + str(img_to_search) + ")")
        os.mkdir("./"+img_to_search)


def saveImageToLocalDisk(img_to_search, counter, image_request):
    # Sending image url to net.
    Image = Request.urlopen(image_request).read()
    print("Saving image..")
    fileName = img_to_search + "/" + img_to_search + "_" + str(counter) + ".jpg"
    tempFile = open(fileName, "wb")
    tempFile.write(Image)
    tempFile.close()


def go_To_NextImage():
    try:
        next_image_btn = browser.find_element_by_xpath("//a[@id=\"iol_navr\"]")
        ActionChains(browser).move_to_element(next_image_btn).click(next_image_btn).perform()
    except TimeoutException:
        saveError_To_TxtFile("Trying to refresh the page due to TimeoutException.")
        browser.refresh()


def startDownload(first_div_class, img_to_search):
    # Clicking the the fisrt image in the result.
    ActionChains(browser).move_to_element(first_div_class).click(first_div_class).perform()
    counter = 1
    # Continue downloading images untill we get required number of images.
    while(counter <= image_quantity_required):
        try:
            # Getting the url of the images's original size.
            img_link = get_OriginalImageLink()
            if(img_link != "null"):
                print(counter, ". ", img_link)
                image_request = Request.Request(img_link, headers=header)
                saveImageToLocalDisk(img_to_search, counter, image_request)
                go_To_NextImage()
                counter += 1
        except Exception as ex:
            print(ex)
            saveError_To_TxtFile(str(counter) + img_link + " \n" + ex)
            go_To_NextImage()


def startSearching(imagesToSearch, sizes, image_quantity_required):
    setHeader()
    Bing_ImageSearch_url = ["https://www.bing.com/images/search?q=",
                            "&qft=+filterui:imagesize-custom"]

    for img_to_search in imagesToSearch:
        imageFound, first_div_class = searchImage(img_to_search, Bing_ImageSearch_url, size)
        if imageFound is False:
            continue
        else:
            createDirectory(img_to_search)
            startDownload(first_div_class, img_to_search)
            print("Success")


imgs_to_search = ["dog", "Human", "wood", "Tree"]
size = 1
image_quantity_required = 700
startSearching(imgs_to_search, size, image_quantity_required)
