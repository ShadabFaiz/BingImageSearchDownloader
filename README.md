# BingImageSearchDownloader
Using this script, we can download as many images from Bing's image result as we want.

# FEATURES
    * Download any number of images you want. Be it 1 image or 500 images or 1000+ images.
    * Download images of any size we want. Currently supports:  
        * 640*480
        * 800*600
        * 1024*768
        * 1600*1200
        * 2272*1704
        * 2816*2112
## UPDATES  
    Main.py is for downloading the images as thumbnails whereas Main_V2.py is for
    downloading images in their original size.
## WALKTHROUGH  
###    1. IDEAS
Earliest, the idea was to use Web Scrapping technique to download images.
But it was not a viable solution since the Bing loads only 35 images
by default. To load more images, we somehow needed to scroll down to load
more images, and also after loading 105 images, we need to click on "See more"
button to load more images. Web Scrapping does not provide us with ways to
interact with the browser.

So i switch to Selenium. It is an automation testing tool. It allowed us to
interact with the browser such as click on images, drag & drop support etc.
Now, we can scroll down and download images as many as we want.

###    2. HOW BING LOADS IMAGES
        Bing loads images first as thumbnails. When we click on the images, then the images will
        load in their original sizes. Main.py walkthrough is for thumbnails whereas Main_V2.py is
        for images of their original size.  

####   Main.py
        Bing loads images in row wise. Each row is denoted by a <ul>.
        Each row/ul contains certain number of <li> which contains an image.
        For ex:
            <ul ....> row 1.
                <li....> image 1 in row 1
                <li....> image 2 in row 1.
                        .
                        .
                        .
                        .
                <li...> image N in row 1.
            </ul>
            <ul...> row 2.
                <li....> image N+1 in row 2
                        .
                        .
                        .
                        .
                        .
                <li>
            </ul>

Each li contains a div class called img_cont hoff. This class has the images attributes with images link.

      <li> image 1
         <div..>
            .
            .
        <a class="iusc"..>    
            <div class="img_cont hoff" ...>
                <img...>
            </div>
                .
                .
            </div>
    </li>

Each "div class="img_cont hoff"" has 1 images.

Overall structure.

        So we needed a regular expression to find that particular image attribute for us.  

####    Main_V2.py  
        This WALKTHROUGH is for Bing loading the image of their original size.
        When all the image's thumbnails are loaded in their thumbnails form and we click on it,
        An image attribute with class "mainImage accessible nofocus" is made visible.
        This attribute represent only the images which is currently infocus or clicked, also
        contains the url for the image. Due to this, there is only 1 image attribute with
        such class. But before we search for it, we have to wait for this attribute to be visible.
        After it is visible, take the src from img(class=mainImage accessible nofocus).
        Now we have image url. We can send the url to net and retrieve the images.
###    3. WORKFLOW
####    Main.py
        * Initialize the browser instances.
                Here, we are using Chrome as a browser. You can use any other browser as long as
                it is supported by Selenium and its driver is available.
        * Creating the url with the image name.
        * Send the appropriate request with the url to the browser.
                In our case, image name.
        At this point of time, 35 images have been loaded in the browser.
        If you want more images, then scroll the page down with selenium or javascript.
        * Get the page source.
        * Check total no of images loaded. If enough of images are loaded, then go further else
          again scroll down and get page source.  
        * In page source, look for the image attribute we are interested in with regular expression.
        * Get the src of images.
        * Send the url to web, response will be an image.
        * Save the images.  

####    Main_V2.py
        * Initialize the browser instances.
                Here, we are using Chrome as a browser. You can use any other browser as long as
                it is supported by Selenium and its driver is available.
        * Creating the url with the image name.
        * Send the appropriate request with the url to the browser.
                In our case, image name.
        * Click the first image.
        * Wait for img(class="mainImage accessible nofocus") to become visible.
        * Take the url in the src of the above img attribute.
        * Send the url to the net.
        * Retrieved response will be an image.
        * Save the image.
        * Click on the "Next img" button to load the next image.
        * Repeat until we get required no of images.

# Prerequisites
####    1.Languages
        * Python 3.6 or above

####    2. Modules
        * Selenium  - for interacting with the browser.
        * urllib    - for sending images request.
        * re        - for extracting images url.
        * os        - for creating required directory and files on the disk.

####    3. Extra Files.
        * Chrome driver. (If you are using Firefox or any other browser, then their respective driver.)
                        Selenium interact with browser using their drivers.
