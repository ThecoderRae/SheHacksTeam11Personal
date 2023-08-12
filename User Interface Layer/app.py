from flask import Flask, render_template, request, redirect, url_for, jsonify
import hashlib
import requests

app = Flask(__name__)
app.secret_key = '1234abcd'


# Login route
# @app.route('/')
@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        

        if email == 'tatendakbeni@gmail.com' and password == 'password123': 
            # return render_template('remittance_calculator.html')
             return redirect(url_for('remittance_calculator'))
    return render_template('login.html')


# Dashboard route
@app.route('/remittance_calculator')
def remittance_calculator():
     if request.method == 'GET':
        all_countries = get_all_countries()
        product_types = get_products_types()
        currencies = get_pay_in_currencies()
        
        return render_template('remittance_calculator.html',countries=all_countries['items'],product_types =product_types['items'],currencies=currencies['items'])


def get_all_countries():
    api_url = "https://api-uct.mukuru.com/taurus/v1/resources/countries?order_by=-displayOrder,name&page_size=241"
    response = requests.get(api_url)
    countries_data = response.json()
    
    return countries_data

def get_products_types():
    api_url = "https://api-uct.mukuru.com/taurus/v1/resources/product-types"

    response = requests.get(api_url)
    product_types_data = response.json()

    return product_types_data

def get_all_countries():
    api_url = "https://api-uct.mukuru.com/taurus/v1/resources/countries?order_by=-displayOrder,name&page_size=241"
    response = requests.get(api_url)
    countries_data = response.json()
    return countries_data

def get_pay_in_currencies():
    api_url = "https://api-uct.mukuru.com/taurus/v1/resources/currencies?order_by=-displayOrder,name&page_size=178"
    response = requests.get(api_url)
    pay_in_currencies = response.json()
    return pay_in_currencies

def get_pay_out_currencies():
    api_url = "https://api-uct.mukuru.com/taurus/v1/resources/currencies?order_by=-displayOrder,name&page_size=178"
    response = requests.get(api_url)
    pay_out_currencies = response.json()
    return pay_out_currencies

@app.route('/calculate', methods=['GET'])
def calculate_remit_cost():

    # working with javascript and AJAX
  
    pay_in_country = request.args.get('pay_in_country')
    pay_out_country = request.args.get('pay_out_country')
    product_type = request.args.get('product_type').lower().replace(' ', '-')
    
    pay_in_currency = request.args.get('pay_in_currency') # New field
    pay_out_currency = request.args.get('pay_out_currency')  # New field
    pay_in_amount = request.args.get('pay_in_amount')
    pay_out_amount = ""  # New field
  
    # api_url = f"https://api-uct.mukuru.com/taurus/v1/products/price-check?pay_in_country={pay_in_country}&pay_out_country={pay_out_country}&pay_in_currency={pay_in_currency}&pay_out_currency={pay_out_currency}&pay_in_amount={pay_in_amount}&pay_out_amount={pay_out_amount}&type={product_type}"
    api_url = "https://api-uct.mukuru.com/taurus/v1/products/price-check" \
          "?pay_in_country=" + pay_in_country + \
          "&pay_out_country=" + pay_out_country + \
          "&pay_in_currency=" + pay_in_currency + \
          "&pay_out_currency=" + pay_out_currency + \
          "&pay_in_amount=" + pay_in_amount + \
          "&pay_out_amount=" + pay_out_amount + \
          "&type=" + product_type 

    response = requests.get(api_url)
    result = response.json()
    remittance_costs = []
    print(result)
    for item in result['items']:
        description = item['description']
        pay_out_amount = item['payOutAmount']
        currency_code = item['payInCurrencyCode']
        fee_amount = item['fee']['amount']
        
        remittance_cost = pay_out_amount + fee_amount
       
        remittance_costs.append({'description': description, 'cost': remittance_cost, 'currency_code': currency_code})
    # calculated_cost = result.get('calculated_cost', 'N/A')
    # print(result)
    return jsonify({'remittance_costs': remittance_costs})

# @app.route('/get_price', methods=['GET'])
# def get_price():
#     # Get the pay_in_country parameter from the query string
#     # pay_in_country = request.args.get('pay_in_country')
#     print("Inside getprice")
#     pay_in_country = "Angola"
   
#     if pay_in_country:
#         # Define the URL with the base endpoint and query parameters
#         url = f"https://api-uct.mukuru.com/taurus/v1/products/price-check?pay_in_country"
       
#         # Make a GET request to the API
#         response = requests.get(url)
       
#         if response.status_code == 200:
#             data = response.json()
#             print(data)
#             return jsonify(data)
#         else:
#             return f"Error: {response.status_code}", response.status_code
#     else:
#         return "Missing pay_in_country parameter", 400



if __name__ == '__main__':
     app.run(debug=True)
     
