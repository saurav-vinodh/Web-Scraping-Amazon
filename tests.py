from django.test import TestCase
from cgi import print_form
from curses.ascii import isdigit
from hashlib import new
from bs4 import BeautifulSoup
import json
#from brisque import BRISQUE
import requests
import json 

# Function to extract Product Title
def get_title(soup):
	
	try:
		# Outer Tag Object
		title = soup.find("span", attrs={"id":'productTitle'})

		# Inner NavigableString Object
		title_value = title.string

		# Title as a string value
		title_string = title_value.strip()

		# # Printing types of values for efficient understanding
		# print(type(title))
		# print(type(title_value))
		# print(type(title_string))
		# print()
	except AttributeError:
		title_string=""	
	return title_string

# Function to extract Product Price
def get_desc(soup):
	try:
		title=soup.findAll("ul",attrs={"class":'a-unordered-list a-vertical a-spacing-mini'})
		for a in title:
			str = a.text
			str1 = str.replace("    ", ". ")
			string = str1.replace("   ", ".")
	except AttributeError:
		string=" "
	return string

def get_price(soup):

	try:
		price = soup.find("span", attrs={'id':'priceblock_ourprice'}).string.strip()
	except AttributeError:
		try:
			price = soup.find("span", attrs={'class':'a-offscreen'}).string.strip()
		except AttributeError:
			price=""
	return price

# Function to extract Product Rating
def get_rating(soup):

	try:
		rating = soup.find("i", attrs={'class':'a-icon a-icon-star a-star-4-5'}).string.strip()
		
	except AttributeError:
		
		try:
			rating = soup.find("span", attrs={'class':'a-icon-alt'}).string.strip()
		except:
			rating = ""	

	return rating

# Function to extract Number of User Reviews
def get_review_count(soup):
	try:
		review_count = soup.find("span", attrs={'id':'acrCustomerReviewText'}).string.strip()
		
	except AttributeError:
		review_count = ""	

	return review_count

# Function to extract Availability Status
def get_availability(soup):
	try:
		available = soup.find("div", attrs={'id':'availability'})
		available = available.find("span").string.strip()

	except AttributeError:
		available = " "	

	return available	

# Function to get number of verified reviews

def get_verifiedreviews(newsoup):
	try:
		number_verified_reviews = newsoup.find("div", attrs={'data-hook':"cr-filter-info-review-rating-count",'class':"a-row a-spacing-base a-size-base"}).string.strip()

	except AttributeError:
		number_verified_reviews =''

	return number_verified_reviews

def get_imagequality(soup):
		img_div = soup.find(id="imgTagWrapperId")

		imgs_str = img_div.img.get('data-a-dynamic-image')  # a string in Json format

		# convert to a dictionary
		imgs_dict = json.loads(imgs_str)
		#each key in the dictionary is a link of an image, and the value shows the size (print all the dictionay to inspect)
		num_element = 0 
		first_link = list(imgs_dict.keys())[num_element]
		url = "https://api.apilayer.com/image_quality/url?url="+first_link
		payload = {}
		headers= {
		"apikey": "7gIJdyHYaCo6NzOEJFQ4IjMKOpHLY64r"
		}

		response = requests.request("GET", url, headers=headers, data = payload)

		status_code = response.status_code
		result = json.loads(response.text)
		
	

		return result['score']

def spell_check(str):

	url = "https://dnaber-languagetool.p.rapidapi.com/v2/check"

	text=str.replace(" ","%20")
	payload = "language=en-US&text="+text
	headers = {
		"content-type": "application/x-www-form-urlencoded",
		"X-RapidAPI-Key": "426b0f0f11msh2760a629b1db798p1490e6jsn14ee7e1e0d80",
		"X-RapidAPI-Host": "dnaber-languagetool.p.rapidapi.com"
	}

	response = requests.request("POST", url, data=payload, headers=headers)

	dict=json.loads(response.text)
	count=len(dict["matches"])
	return count

def number_of_verified(verified_reviews):
	count=-1
	i=0
	number=0
	for j in verified_reviews:
		if (verified_reviews[i].isdigit() or verified_reviews[i]==','):
			if (verified_reviews[i]==' '):
				break
			if (verified_reviews[i].isdigit()):
				count=count+1
			i=i+1
	i=0
	for j in verified_reviews:
		if (verified_reviews[i].isdigit() or verified_reviews[i]==','):
			if (verified_reviews[i]==' '):
				break
			if (verified_reviews[i].isdigit()):
				number=((10**count)*int(verified_reviews[i]))+number
				count=count-1
			i=i+1
	return number



	



















if __name__ == '__main__':

	# Headers for request
	HEADERS = ({'User-Agent':
	            'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36',
	            'Accept-Language': 'en-US, en;q=0.5'})

	# The webpage URL
	URL = "https://www.amazon.in/New-Apple-iPhone-12-128GB/dp/B08L5TNJHG/ref=cm_cr_arp_d_product_top?ie=UTF8"
	
	#Verified Reviews URL
	replacement1="/dp/"
	review_title="/product-reviews/"
	newurl1=URL.replace(replacement1,review_title)
	index=newurl1.find("/ref=")
	newurl2=newurl1[0:index+5]+"cm_cr_arp_d_viewopt_rvwer?ie=UTF8&reviewerType=avp_only_reviews&pageNumber=1"
	print(newurl2)
	new_webpage=requests.get(newurl2, headers=HEADERS)
	newsoup = BeautifulSoup(new_webpage.content, "lxml")


	# HTTP Request
	webpage = requests.get(URL, headers=HEADERS)

	# Soup Object containing all data
	soup = BeautifulSoup(webpage.content, "lxml")

	#Function calls to display all necessary product information
	print("Product Title =", get_title(soup))
	print("Product Price =", get_price(soup))
	print("Product Rating =", get_rating(soup))
	verified_number=number_of_verified(get_verifiedreviews(newsoup))
	review_number=number_of_verified(get_review_count(soup))
	print("Number of Product Reviews =", review_number)
	print("Number of Verified reviews =", verified_number)


	image=get_imagequality(soup)
	check_title=spell_check(get_title(soup))
	check_product=spell_check(get_desc(soup))
	print(image)
	print(check_title)
	print(check_product)
	count=0
	if image<100:
		count=count+1
	if (verified_number/review_number)>0.5:
		count=count+1
	
	length_title=len(get_title(soup).split())
	length_desc=len(get_desc(soup).split())
	
	if (check_title/length_title)<0.5:
		count=count+1
	if (check_product/length_desc)<0.5:
		count=count+1
	
	percentage=(count/4)*100
	print("Percentage is ",percentage)

	print()


