from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import re
import time
import csv
# Create an instance of Chrome driver
driver_path = "/usr/local/bin/" 
browser = webdriver.Chrome(driver_path)
# Navigate to website Tiki.vn > Laptop category
browser.get("https://tiki.vn/laptop/c8095")
pagination = browser.find_element(By.CSS_SELECTOR, ".Pagination__Root-sc-cyke21-0.gNgpAR")
lastPage = int(pagination.find_elements(By.TAG_NAME, "a")[5].text)

with open('products.csv', 'w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(['Title', 'Brand', 'Price', 'Images', 'Details', 'Description'])
# Select all product items by CSS Selector
# last_page+1
    for page in range(1, lastPage + 2):
        url = f"https://tiki.vn/laptop/c8095?page={page}"
        browser.get(url)
        time.sleep(2)
        listProductLink = []
        products = browser.find_elements(By.CSS_SELECTOR, ".product-item")
        for product in products:
            outerHTML = product.get_attribute("outerHTML")
            productLink = re.search('href="(.*?)"', outerHTML).group(1)
        # productLink = "https://" + productLink
            listProductLink.append(productLink)

# Go to each product link
        for productLink in listProductLink:
            print("DEBUG: " + productLink)
            # time.sleep(1)
        # Go to product link
            try:
                browser.get("https://" + productLink)
            except:
                browser.get("https://tiki.vn" + productLink)

    # Extract product information by CSS Selector
            productTitle = browser.find_elements(By.CSS_SELECTOR, ".title")[1].text
            print("DEBUG TITLE: " + productTitle)

            productBrand = browser.find_elements(By.XPATH, "//a[@data-view-id='pdp_details_view_brand']")[0].text
            print("DEBUG BRAND: " + productBrand)

    # Extract product price
            productPriceElements = browser.find_elements(By.CSS_SELECTOR, ".product-price__current-price")
            if len( productPriceElements) > 0:
                productPrice =  productPriceElements[0].text
            else:
                productPprice = browser.find_elements(By.CSS_SELECTOR, ".styles__Price-sc-6hj7z9-1.jgbWJA")[0].text
            productPrice = re.search('^[\\d|\\.|\\,]+', productPrice).group(0)
            print("DEBUG PRICE: " + productPrice)

    # Extract product images
            productImages = []
            imageElements = browser.find_elements(By.CSS_SELECTOR, ".review-images__list .WebpImg__StyledImg-sc-h3ozu8-0.fWjUGo")
            for imageElement in imageElements:
                imageUrl = imageElement.get_attribute("src")
                productImages.append(imageUrl)
            print("DEBUG IMAGES: " + str(productImages))

    # Extract product details
            productDetails = {}
            detailsElements = browser.find_elements(By.CLASS_NAME, "content.has-table")
            for detailsElement in detailsElements:
                rows = detailsElement.find_elements(By.TAG_NAME, "tr")
                for row in rows:
                    cells = row.find_elements(By.TAG_NAME, "td")
                    key = cells[0].text.strip()
                    value = cells[1].text.strip()
                    productDetails[key] = value
    
            print("DEBUG DETAILS: " + str(productDetails))
    
    # Extract product description
            productDescription = browser.find_element(By.XPATH,'//div[contains(@class, "ToggleContent__View-sc-1dbmfaw-0 wyACs")]').get_attribute("innerHTML")
            print("DEBUG DESCRIPTION: " + productDescription)
    
            time.sleep(0.5)
            writer.writerow([productTitle, productBrand, productPrice, ', '.join(productImages), productDetails, productDescription])
# Close the browser
browser.quit()