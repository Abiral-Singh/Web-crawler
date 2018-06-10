#"http://www.shilohtack.com/categories.php"

import requests
from bs4 import BeautifulSoup
import time
from csv import DictWriter

#cant provide website due to legal reasons send a pull request if you need
main_url = "http://www.**********.com/"
base_url = "http://www.**********.com/categories.php"
image_url = "http://www.**********.com/prodimages/"
def scrape_product():
	response = requests.get(base_url)
	if not response.status_code == 200:
	    raise Exception("Something went wrong !")
	soup = BeautifulSoup(response.text, "html.parser")
	targets = soup.find_all('td', class_="catname")
	target_url = ''
	all_products = []
	for target in targets:
	    time.sleep(2)
	    target_url = target.find_next(class_="ectlink")["href"]
	    print(f"now scraping {target_url}")
	    # print(target_url) #crawl inside each target_url for products
	    response = requests.get(main_url+target_url)
	    while True :
		    soup = BeautifulSoup(response.text, "html.parser")
		    # print(response.text)
		    product_descriptions = soup.find_all('td', class_="proddescription")
		    product_ids = soup.find_all('div', class_="prodname")
		    product_images = soup.find_all('td', class_="prodimage")
		    # print(product_descriptions)
		    for p_d, p_ids, p_images in zip(product_descriptions, product_ids, product_images):
		        #print('*'*20)
		        p_description = p_d.get_text().split('/*')[0]
		        p_id = p_ids.find_next().get_text()
		        p_link = p_ids.find_next(class_="ectlink")['href']
		        p_link = main_url + p_link
		        # work for images
		        try:
		            p_image = p_images.find_next('script').get_text().split("'|")[1]
		            p_image = p_image.split("';")[0]
		            p_image = p_image.split(">\\\\")
		            p_image.pop()
		            p_image = [thing.replace("|", "") for thing in p_image]
		            # making image links
		            p_image = [image_url+thing + ".jpg" for thing in p_image]
		        except:
		            p_image = p_images.find_next('img', class_="prodimage")["src"]
					p_image = main_url+p_image
		        # print(p_description)
		        # print('Product id : ')
		        # print(p_id)
		        # print("product link : ", p_link)
		        # print("product image link : ", p_image)
		        all_products.append({
		        	"product-descriptions":p_description,
		        	"id":p_id,
		        	"product-link":p_link,
		        	"image-link":p_image
		        	})
		    
		    #next page
		    #print(all_products) 
		    next_btn = soup.find('a', rel = "next")
		    if not next_btn :
		    	break
		    next_btn =next_btn["href"]
		    print(f"now scraping {main_url+next_btn}")
		    time.sleep(2)
		    response = requests.get(main_url+next_btn)
	return all_products


def write_products(all_products):
    with open("product_data.csv", "w") as file:
        headers = ["product-descriptions", "id", "product-link", "image-link"]
        csv_writer = DictWriter(file, fieldnames=headers)
        csv_writer.writeheader()
        try:
            for product in all_products:
                csv_writer.writerow(product)
        except :
            pass


products=scrape_product()
write_products(products)