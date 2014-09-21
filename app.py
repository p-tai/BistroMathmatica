from flask import Flask, render_template, request
import ordrin
from decimal import *

app = Flask(__name__)
api_key = '-HgyKdNLalGrm_T0x3ABYN2ABtCGOlqBzxK1xDy391s'
ordrin_api = ordrin.APIs(api_key, ordrin.TEST)

street_address = ''
city = ''
state = ''
zipcode = ''
choice_id = ''
total = ''

@app.route('/')
def home():
	#nothing here, just a continue button
	return render_template('index.html')

@app.route('/address')
def address():
	#Get STREET, CITY, STATE, ZIP, EMAIL, PHONE number, FIRSTNAME, LASTNAME; send onward
	return render_template('address.html')

@app.route('/restaurants', methods = ['POST'])
def list():
	#Use ADDRESS to send ordrin request to get list of all restaurants that deliver to that addr
	street_address = request.form['street']
	city = request.form['city']
	state = request.form['state']
	zipcode = request.form['zip']
	
	restaurants = ordrin_api.delivery_list('ASAP', street_address, city, zipcode)

	#find which restaurants deliver now
	we_deliver = []
	for r in restaurants:
		#comment out for demo:
		if r['is_delivering'] == 1:
			we_deliver.append(r)
	#Display list (disp options: name, cuisine type, address, min order cost, delivery time)
	#Get user choice back (Restaurant ID -> RID)
	return render_template('restaurants.html', restaurants=we_deliver)

#if menu is dumb, use eric song's text search, have user type in orders
#test everything else first, hardcode a tray in
@app.route('/menu')
def menu():
	rid = 'hardcode'
	tray = 'hardcode'
	subtotal = 'hardcode'
	tip = 'hardcode'
	#Use RID to get menu JSON
	#Display menu, with buttons; display current TRAY (Aedan)
	#TRAY string = [item id1]/[qty1],[option id11] + [item id2]/[qty2],[option id21],[option id22]
	#send TRAY string onward
	return

@app.route('/fees')
def fees():
	#display delivery fees and total
	choice_id = request.args['rid']
	subtotal = request.args['subtotal']
	tip = request.args['tip']
	
	fees = ordrin_api.fee('ASAP', choice_id, subtotal, tip, street_address, city, zipcode)
	fee = fees['fee']
	tax = fees['tax']
	minimum = fees['mino']
	time = fees['del']

	total = Decimal(subtotal) + Decimal(tip) + Decimal(fee) + Decimal(tax)

	#wait for user to accept
	return

@app.route('/payment')
def payment():
	#get CREDIT card info, BILLING address
	return render_template('billing.html')

@app.route('/confirmation')
def confirm():
	#send order via post request or API wrapper
	#RID, TRAY, TIP, ASAP, ASAP, FIRSTNAME, LASTNAME, ADDR, CITY, STATE, ZIP, PHONE, EMAIL, CARDNAME, CARDNUM, CARDCVC, CARDEXPR, CARDADDR, (CARDADDR2), CARDCITY, CARDSTATE, CARDZIP,CARDPHONE
	#confirmation (auto?) sent to user's email
	#Tell user order has been sent, move on to VENMO STUFF
	#email
	#items list of tuples ("item name", cost)
	#total BEFORE tax/tip/fees
	#surcharges = tax + tip + fees
	return

@app.route('/failure')
def fail():
	#Tell user they're a piece of shit
	return

if __name__ == '__main__':
	app.run('0.0.0.0', port=4000, debug=True)
