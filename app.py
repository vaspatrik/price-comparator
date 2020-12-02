from flask import Flask, render_template, request
from urllib.request import urlopen
import threading
import queue

from bs4 import BeautifulSoup as bs
from threading import Thread

app = Flask(__name__)



@app.route('/')
def hello_world():
	return render_template('index.html')

@app.route('/new-product', methods=['POST'])
def new_product():
	query = request.form['product']
	products = get_related_products(query)
	return render_template('related_products.html', query=query, products=products)


def get_related_products(query):
	search_url = 'https://www.trademe.co.nz/Browse/SearchResults.aspx?buy=buynow&v=List&searchString=' + query.replace(' ', '+')
	page_soup = bs(urlopen(search_url).read(), 'html.parser')
	totalCount = page_soup.find(id="totalCount").text
	
	result = queue.Queue()
	threads = [ getProcessProductItemThreads(item, result) for item in page_soup.find_all('div', attrs={'data-listingid' : True})]
	
	for t in threads:
		t.start()
	for t in threads:
		t.join()

	return list(result.queue)

def get_product_data(url, product, result):
	page_content = bs(urlopen(url).read(), 'html.parser')
	seller = page_content.find('a', {'class': 'seller-name'}).text
	shippingUL = page_content.find('ul', {'id': 'ShippingDetails_CustomShippingOptionList'})
	shippingPrices = '/'.join([sp.text for sp in shippingUL.findAll('span', {'class': 'custom-shipping-price'})])
	product['seller'] =  seller
	product['shipping'] = shippingPrices
	result.put(product)

def getProcessProductItemThreads(item, result):
	id = item['data-listingid']
	title = item.find('div', {'class': 'title'}).text.strip()
	price = item.find('div', {'class': 'listingBuyNowPrice'}).text.strip()
	link = 'https://www.trademe.co.nz/' + item.parent['href'].split('?')[0]
	product = {'id': id, 'title': title, 'price': price, 'link': link}
	return Thread(target=get_product_data, args = (link, product, result))

if __name__ == '__main__':
	app.run(debug=True)
