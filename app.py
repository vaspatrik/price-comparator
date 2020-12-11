import threading
import queue
from threading import Thread

from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

from urllib.request import urlopen
from bs4 import BeautifulSoup as bs

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///price-cmp.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Competitor(db.Model):
	username = db.Column(db.String(200), primary_key=True, nullable=False)
	comment = db.Column(db.String(255))

class Product(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)
	keywords = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Numeric(10,2))
	tacked_items = db.relationship('TrackedItem', backref='product', lazy=True, order_by="TrackedItem.price")


class TrackedItem(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)
	web_id = db.Column(db.String(200), nullable=False)
	seller = db.Column(db.String(200), nullable=False)
	url = db.Column(db.String(1200), nullable=False)
	shipping = db.Column(db.String(1200), nullable=False)
	price = db.Column(db.Numeric(10,2))
	product_id = db.Column(db.Integer, db.ForeignKey('product.id'), nullable=False)


@app.route('/')
@app.route('/new_product')
def index():
	return render_template('index.html')

@app.route('/view_tracked_products')
def view_tracked_products():
	trackedProducts = Product.query.all()
	return render_template('view_tracked_products.html', products=trackedProducts)


@app.route('/competitors', methods=['POST', 'GET'])
def competitors():
	if request.method == 'POST':
		username = request.form['username']
		comment = request.form['comment']
		c = Competitor(username=username, comment=comment)
		db.session.add(c)
		db.session.commit()
	comps = Competitor.query.all()
	return render_template('competitors.html', competitors=comps)


@app.route('/save-search', methods=['POST'])
def save_search():
	keywords = [s.strip() for s in request.form['keywords'].split(',')]
	name = request.form['name']
	price = request.form['price'] if request.form['price'] else 0 
	search = save_related_products(name, keywords, price)
	return redirect('related_products?search_id=' + str(search.id))

@app.route('/related_products', methods=['GET'])
def search_products():
	sid = request.args.get('search_id')
	search = Product.query.filter_by(id=sid).first()
	return render_template('related_products.html', product=search)


def save_related_products(name, keywords, price):
	result = get_all_related_products(keywords)
	search = Product(name=name, keywords=', '.join(keywords), price=price)
	search.tacked_items = result
	db.session.add(search)
	db.session.commit()

	return search

def get_unique_items(items):
	res = []
	ids = set()
	while (not items.empty()):
		prod = items.get()
		if (prod.web_id not in ids):
			res.append(prod)
			ids.add(prod.web_id)
	return res

def get_all_related_products(keywords):
	threads = []
	result = queue.Queue()
	for search_term in keywords:
		search_url = 'https://www.trademe.co.nz/Browse/SearchResults.aspx?buy=buynow&condition=new&v=List&searchString=' + search_term.replace(' ', '+')
		page_soup = bs(urlopen(search_url).read(), 'html.parser')
		count_span = page_soup.find(id="totalCount")
		if (count_span):
			total_count = count_span.text
			for item in page_soup.find_all('div', attrs={'data-listingid' : True}):
				t = getProcessProductItemThreads(item, result)
				t.start()
				threads.append(t)

			for t in threads:
				t.join()
	return get_unique_items(result)

def get_product_data(url, product, result):
	page_content = bs(urlopen(url).read(), 'html.parser')
	seller_tag = page_content.find('a', {'class': 'seller-name'})
	shippingPrices = None
	seller = None
	if (seller_tag):
		seller = seller_tag.text
		shippingUL = page_content.find('ul', {'id': 'ShippingDetails_CustomShippingOptionList'})
		shippingPrices = '/'.join([sp.text for sp in shippingUL.findAll('span', {'class': 'custom-shipping-price'})])
	else:
		seller = page_content.find('section', {'class': 'member-summary-box'}).find('h3').text
		shippingTag = page_content.find('tm-listing-shipping-details')
		shippingPrices = '/'.join([sp.text for sp in shippingTag.findAll('td', {'class': 'h-text-align-right'})])

	product.seller =  seller
	product.shipping = shippingPrices
	result.put(product)

def getProcessProductItemThreads(item, result):
	id = item['data-listingid']
	name = item.find('div', {'class': 'title'}).text.strip()
	price = item.find('div', {'class': 'listingBuyNowPrice'}).text.strip()[1:]
	price = price.split('-')[0].replace(',','')
	url = 'https://www.trademe.co.nz/' + item.parent['href'].split('?')[0]
	product = TrackedItem(web_id=id, name=name, price=price, url=url)
	return Thread(target=get_product_data, args = (url, product, result))

if __name__ == '__main__':
	app.run(debug=True)
