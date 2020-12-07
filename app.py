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

class Search(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	search = db.Column(db.String(200), nullable=False)
	price = db.Column(db.Numeric(10,2))
	tacked_products = db.relationship('TrackedProduct', backref='Seach', lazy=True)


class TrackedProduct(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(200), nullable=False)
	product_id = db.Column(db.String(200), nullable=False)
	seller = db.Column(db.String(200), nullable=False)
	url = db.Column(db.String(1200), nullable=False)
	shipping = db.Column(db.String(1200), nullable=False)
	price = db.Column(db.Numeric(10,2))
	search_id = db.Column(db.Integer, db.ForeignKey('search.id'), nullable=False)


@app.route('/')
@app.route('/new_product')
def index():
	return render_template('index.html')

@app.route('/view_tracked_products')
def view_tracked_products():
	trackedProducts = Search.query.all()
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
	query = request.form['product']
	price = request.form['price']
	search = save_related_products(query, price)
	return redirect('related_products?search_id=' + str(search.id))

@app.route('/related_products', methods=['GET'])
def search_products():
	sid = request.args.get('search_id')
	search = Search.query.filter_by(id=sid).first()
	return render_template('related_products.html', search=search)


def save_related_products(query, price):
	search_url = 'https://www.trademe.co.nz/Browse/SearchResults.aspx?buy=buynow&v=List&searchString=' + query.replace(' ', '+')
	page_soup = bs(urlopen(search_url).read(), 'html.parser')
	total_count = page_soup.find(id="totalCount").text
	result = queue.Queue()
	threads = [ getProcessProductItemThreads(item, result) for item in page_soup.find_all('div', attrs={'data-listingid' : True})]
	
	for t in threads:
		t.start()
	for t in threads:
		t.join()

	search = Search(search=query, price=price)
	search.tacked_products = list(result.queue)
	db.session.add(search)
	db.session.commit()

	return search

def get_product_data(url, product, result):
	page_content = bs(urlopen(url).read(), 'html.parser')
	seller = page_content.find('a', {'class': 'seller-name'}).text
	shippingUL = page_content.find('ul', {'id': 'ShippingDetails_CustomShippingOptionList'})
	shippingPrices = '/'.join([sp.text for sp in shippingUL.findAll('span', {'class': 'custom-shipping-price'})])
	product.seller =  seller
	product.shipping = shippingPrices
	result.put(product)

def getProcessProductItemThreads(item, result):
	id = item['data-listingid']
	name = item.find('div', {'class': 'title'}).text.strip()
	price = item.find('div', {'class': 'listingBuyNowPrice'}).text.strip()[1:]
	url = 'https://www.trademe.co.nz/' + item.parent['href'].split('?')[0]
	product = TrackedProduct(product_id=id, name=name, price=price, url=url)
	return Thread(target=get_product_data, args = (url, product, result))

if __name__ == '__main__':
	app.run(debug=True)
