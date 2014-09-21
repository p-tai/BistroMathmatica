import urllib
import json

"""
getVenmoPostURL - 
Returns the POST request URL to charge another user
token: access token for the user
email: email of the user being charged
items: list of tuples containing the ("item name", cost)
total: total cost of the order BEFORE tax/tip/delivery
surcharge: tax/tip/delivery fees (summed)
"""
def getVenmoPostURL(token, email, items, total, surcharge):
	"""
	Make a Payment/Charge
	POST /payments
	Pay or a charge an email, phone number or user.
	Permissions: make_payments, access_balance (optional)
	Parameters
	access_token required 	An authorized user's access token.
	phone, email or user_id required 	Provide a valid US phone, email or Venmo User ID.
	note required 	A message to accompany the payment.
	amount required 	The amount you want to pay. To create a charge, use a negative amount.
	audience 	The sharing setting for this payment. Possible values are 'public', 'friends' or 'private'.
	"""
	#baseURL = "https://api.venmo.com/v1/payments?"
	baseURL = "https://sandbox-api.venmo.com/v1/payments?"
	params = {}
	#needs an access token of the user
	params["access_token"] = token
	params["email"] = email
	note = ""
	subtotal = 0.0;
	
	#Add up the cost of each item and append it to the note
	for item in items:
		note += item[0]
		note += " "
		note += "{:.2f}".format(item[1])
		note += " + "
		subtotal += item[1]
	
	#Calcuate a pro-rated cost of other fees (delivery,tax,tip)
	note += "tax, tip, delivery "
	proRatedSurcharge = subtotal/total *  surcharge
	note += "{:.2f}".format(proRatedSurcharge)
	note += " = "
	subtotal+=proRatedSurcharge
	note += "{:.2f}".format(subtotal)
	params["note"] = note
	#print note
	
	#Set the amount negative to charge
	params["amount"] = "-" + "{:.2f}".format(subtotal)
	
	params["audience"] = "friends"
	postURL = baseURL + urllib.urlencode(params)
	
	#print postURL
	return postURL

"""
getVenmoAccessTokenURL - 
Forms the URL for the Venmo API that will automatically redirect you to a venmo login page.
After logging in, it will redirect to http://ordrwith.me/split and 
a client side token good for 30 minutes.
Returns the URL, (DOES NOT submit a post request to Venmo's API)
"""
def getVenmoAccessTokenURL():
	"""
	Redirect your user to the URL
	https://api.venmo.com/v1/oauth/authorize?client_id=<client_id>&scope=<scopes>

	The following parameters can be set in the URL:
    client_id (required) - You can find your client ID in the developer tab.
    scope (required) - Scopes should be space delimited. You can find a list of the available scopes here.
	"""
	baseURL = "https://api.venmo.com/v1/oauth/authorize?"
	params = {}
	
	#client id is assigned by Venmo
	params["client_id"] = "1990"
	
	params["scope"] = "make_payments"
	
	accessURL = baseURL + urllib.urlencode(params)
	
	#print accessURL
	return accessURL

"""
test functions, can be deleted once merged
"""
def main():
	print getVenmoAccessTokenURL()
	#after POSTing to Venmo to get the Access token
	#@get /split/oauth you can get the access_token field from the URL and use the token to post payments
	print getVenmoPostURL( "tempToken", "venmo@venmo.com",[("buffadilla",5.95), ("super-thick milk shake", 6.95)], 49.95, 10.00 )
	
if __name__ == "__main__": 
	main()
