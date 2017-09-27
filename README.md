# BingImageSearchDownloader
Using this script, we can download as many images from Bing's image result as we want.  
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
Bing loads images in row wise. Each row is denoted by a ul.  
Each row/ul contains certain number of li with contains an image.
       
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

    <ul data-row=row number....>
        <li...data-idx=image_index_no..>
            .....
            <a class="iusc"...>
                <div class="img_cont hoff"..>
                    <img....> // We want this.

So we needed a regular expression to find that particular image attribute for us.
###    3. WORKFLOW
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
