from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from .serializers import  CustomerSerializer
from .models import Customer, CustomerCredit, Order, OrderDetails, Product, Payment, EmiDetails, PinCode
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponse
import json
from datetime import datetime
from dateutil.relativedelta import relativedelta
from django.db.models import Sum
from django.db.models import F
from django.conf import settings
#from dateutil import relativedelta



# Import M L model
from ML_model.buyer_profile import load_model, predict_function





#curl -X POST http://127.0.0.1:8000/signup/ -d '{"password":"tikks1", "email":"tikks1@gmail.com", "fname":"tikks1", "lname":"arora1","age":"20","address":"sky","city":"pune","state":"maharashtra","pincode":"411006","phone":"1234","gender":"female"}' -H "Content-Type:application/json"
@csrf_exempt 
def SignUpView(request):

#go to /signup url
#input = 11 fields
#output user_id

	if request.method == 'POST':
		
		print (request.body)
		body_unicode = request.body.decode('utf-8')
		print(body_unicode)
		body = json.loads(body_unicode)


		password = body['password']
		email = body['email']
		fname = body['fname']
		lname = body['lname']
		age= body['age']
		address = body['address']
		city = body['city']
		state = body['state']
		pincode = body['pincode']
		phone = body['phone']
		gender = body['gender']

		customer_obj=Customer.objects.create(password=password, email=email, fname=fname, lname=lname, age=age, address= address, city = city, state=state, pincode = pincode, phone=phone, gender=gender)
		customer_obj.save()

		#call AI Model here to calculate initial credit score

		#populate CustomerCredit on the basis of credit score

		#code to be executed in case AI model cannot be made
		temp_customer = Customer.objects.filter(email= email).first()
		customer_credit_obj = CustomerCredit.objects.create(user_id= temp_customer, initial_credit_limit=5000, credit_score=500, credit_utilization=0, current_credit_limit=5000)
		customer_credit_obj.save()


		if customer_obj is not None:
			return JsonResponse({'user_id' : customer_obj.user_id})
		else:
			return JsonResponse({'user_id' : -1})

	else:
		return JsonResponse({'user_id' : -1})


 

#curl -X POST http://127.0.0.1:8000/login/ -d '{"email": "nidhi@gmail.com", "password":"nidhi"}' -H "Content-Type:application/json"
@csrf_exempt
def LoginView(request):

# go to /login url
#input = email ,password
#output = user_id/None

	if request.method == 'POST':

		# request_uname = request.POST.get("username")
		# request_pwd = request.POST.get("password")
		print (request.body)

		body_unicode = request.body.decode('utf-8')
		print(body_unicode)
		body = json.loads(body_unicode)

		email = body['email']
		password = body['password']

		print (email)

		temp_customer = Customer.objects.filter(email= email).first()
		print (temp_customer)

		if temp_customer is not None:
			print("HELLO",temp_customer.email)
			if temp_customer.password == password:
				return JsonResponse({'user_id' : temp_customer.user_id})
			else:
				return JsonResponse({'user_id' : -1})
		else:
			return JsonResponse({'user_id' : -1})
	else:
		return JsonResponse({'user_id' : -1})




#curl -X POST http://127.0.0.1:8000/catalogue/ -d '{"user_id":"2", "product_list":[{"product_id":"1","quantity":"2", "price":"100"},{"product_id":"2","quantity":"3","price":"200"}]}' -H "Content-Type:application/json"
@csrf_exempt
def CatalogueView(request):

#go to /catalogue
#input = user_id and product list
#output = user_id, product_list, bill_amount

	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		user_id = body['user_id']
		product_list = body['product_list']

		
		temp_customer = Customer.objects.filter(user_id= user_id).first()
		if temp_customer is None:
			return JsonResponse({'message' : 'CustomerRetrievalError'})


		bill_amount=0
		quantity=0
		price=0
		product_id=1
		
		for dic in product_list:
			product_id=dic["product_id"]
			quantity=dic["quantity"]
			price=dic["price"]
			bill_amount = bill_amount + (int(quantity)*int(price))


		order_obj = Order.objects.create(user_id=temp_customer, bill_amount=bill_amount)
		order_obj.save()


       	#uptil now only Order table has been filled

		temp_order = Order.objects.filter(user_id=temp_customer).last()
		order_id = temp_order.order_id
		if temp_order is None:
			return JsonResponse({'message' : 'OrderRetrievalError'})

		#working code including quantity field:
		# for dic in product_list:
		# 	total_price_per_product=0
		# 	product_id=dic["product_id"]
		# 	quantity=dic["quantity"]
		# 	price=dic["price"]
		# 	total_price_per_product = total_price_per_product + (int(quantity)*int(price))

		# 	temp_product = Product.objects.filter(product_id=product_id).first()

		# 	if temp_product is None:
		# 		return JsonResponse({'message' : 'ProductRetrievalError'})

		# 	order_details_obj =OrderDetails.objects.create(user_id=temp_customer, order_id=temp_order, product_id=temp_product, quantity=quantity, total_price=total_price_per_product)
		# 	order_details_obj.save()



		for dic in product_list:
			total_price_per_product=0
			product_id=dic["product_id"]
			quantity=dic["quantity"]
			price=dic["price"]
			#total_price_per_product = total_price_per_product + (int(quantity)*int(price))

			temp_product = Product.objects.filter(product_id=product_id).first()
			print("PRODUCT ID: ",temp_product.product_id)

			if temp_product is None:
				return JsonResponse({'message' : 'ProductRetrievalError'})

			count=0
			for count in range(int(quantity)):
				order_details_obj =OrderDetails.objects.create(user_id=temp_customer, order_id=temp_order, product_id=temp_product, quantity=1, total_price=price)
				order_details_obj.save()


		return JsonResponse({'user_id' : user_id, 'product_list':product_list, 'bill_amount':bill_amount})


	else:
		return JsonResponse({'user_id' : 'None'})





@csrf_exempt
def CartView(request):

#go to /cart
#input = user_id
#output= credit score, quantity, buyers profile score, transaction number

	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		user_id = body['user_id']

		temp_customer = Customer.objects.filter(user_id= user_id).first()
		if temp_customer is None:
			return JsonResponse({'message' : 'CustomerRetrievalError'})


		temp_order = Order.objects.filter(user_id=temp_customer).last()
		if temp_order is None:
			return JsonResponse({'message' : 'OrderRetrievalError'})


		x=Customer.objects.values('age','pincode').filter(user_id=user_id)
		for temp in x:
			age=temp['age']
			pincode=temp['pincode']

		print("age: ",age)
		print("pincode: ",pincode)


		pincode_obj= PinCode.objects.filter(pincode=pincode).first()
		#pincode_class = pincode_obj.pincode_class
		pincode_class=2
		if pincode_class is None:
			pincode_class=1
		print("pincode_class: ",pincode_class)

		total_orders=Order.objects.filter(user_id=temp_customer).exclude(order_id=temp_order.order_id).count()
		if total_orders is None:
			total_orders=0;
		print("total_orders: ",total_orders)


		total_products_bought=OrderDetails.objects.filter(user_id=temp_customer).exclude(order_id=temp_order.order_id).count()
		if total_products_bought is None:
			total_products_bought=0;
		print("total_products_bought: ",total_products_bought)


		total_amount_spent = Order.objects.filter(user_id=temp_customer).exclude(order_id=temp_order.order_id).aggregate(Sum('bill_amount'))['bill_amount__sum']
		if total_amount_spent is None:
			total_amount_spent=0;
		print("total_amount_spent: ",total_amount_spent)


		credit_card = Payment.objects.filter(user_id=temp_customer, payment_type="credit card").exclude(order_id=temp_order.order_id).count()
		if credit_card is None:
			credit_card=0;
		print("credit_card: ",credit_card)


		debit_card = Payment.objects.filter(user_id=user_id, payment_type="debit card").exclude(order_id=temp_order.order_id).count()
		if debit_card is None:
			debit_card=0;
		print("debit_card: ",debit_card)


		net_banking = Payment.objects.filter(user_id=user_id, payment_type="net banking").exclude(order_id=temp_order.order_id).count()
		if net_banking is None:
			net_banking=0;
		print("net_banking: ",net_banking)


		mobile_wallet = Payment.objects.filter(user_id=user_id, payment_type="mobile wallet").exclude(order_id=temp_order.order_id).count()
		if mobile_wallet is None:
			mobile_wallet=0;
		print("mobile_wallet: ",mobile_wallet)


		cod = Payment.objects.filter(user_id=user_id, payment_type="cash on delivery").exclude(order_id=temp_order.order_id).count()
		if cod is None:
			cod=0;
		print("cod: ",cod)


		emi_applications = Payment.objects.filter(user_id=user_id, payment_type="EMI").exclude(order_id=temp_order.order_id).count()
		if emi_applications is None:
			emi_applications=0;
		print("emi_applications: ",emi_applications)


		mobile_wallet_used = Payment.objects.filter(user_id=user_id, mobile_wallet_used="yes").exclude(order_id=temp_order.order_id).count()
		if mobile_wallet_used is None:
			mobile_wallet_used=0;
		print("mobile_wallet_used: ",mobile_wallet_used)


		delivered = OrderDetails.objects.filter(user_id=user_id, order_status="delivered").exclude(order_id=temp_order.order_id).count()
		if delivered is None:
			delivered=0;
		print("delivered: ",delivered)


		returned = OrderDetails.objects.filter(user_id=user_id, order_status="returned").exclude(order_id=temp_order.order_id).count()
		if returned is None:			returned=0;
		print("returned: ",returned)


		cancelled = OrderDetails.objects.filter(user_id=user_id, order_status="cancelled").exclude(order_id=temp_order.order_id).count()
		if cancelled is None:
			cancelled=0;
		print("cancelled: ",cancelled)


		if total_orders==0:
			avg_price_order=0
		else:
			avg_price_order = total_amount_spent/total_orders
		if avg_price_order is None:
			avg_price_order=0;
		print("avg_price_orders: ",avg_price_order)


		if total_products_bought==0:
			avg_price_product=0
		else:
			avg_price_product = total_amount_spent/total_products_bought
		if avg_price_product is None:
			avg_price_product=0;
		print("avg_price_products: ",avg_price_product)


		emi_months = EmiDetails.objects.filter(user_id=user_id).exclude(order_id=temp_order.order_id).count()
		if emi_months is None:
			emi_months=0;
		print("emi_months: ",emi_months)


		total_amt_emi = EmiDetails.objects.filter(user_id=user_id).exclude(order_id=temp_order.order_id).aggregate(Sum('emi_value'))['emi_value__sum']
		if total_amt_emi is None:
			total_amt_emi=0;
		print("total_amt_emi: ",total_amt_emi)


		historic_emi_sum = EmiDetails.objects.filter(user_id=temp_customer).exclude(order_id=temp_order).aggregate(Sum('emi_value'))['emi_value__sum']
		historic_number_of_installments = EmiDetails.objects.filter(user_id=temp_customer).exclude(order_id=temp_order).count()

		if historic_number_of_installments==0:
			avg_emi_order_month=0
		else:
			avg_emi_order_month = (historic_emi_sum)/(historic_number_of_installments)
		if avg_emi_order_month is None:
			avg_emi_order_month=0;
		print("avg_emi_order_month: ",avg_emi_order_month)


		first_order = Order.objects.filter(user_id=temp_customer).exclude(order_id=temp_order.order_id).first()
		last_order = Order.objects.filter(user_id=temp_customer).exclude(order_id=temp_order.order_id).last()
		start= first_order.timestamp
		start=str(start).split(".")[0]
		last= last_order.timestamp
		last=str(last).split(".")[0]
		date1 = datetime.strptime(str(start), '%Y-%m-%d %H:%M:%S')
		date2 = datetime.strptime(str(last),'%Y-%m-%d %H:%M:%S')
		r = relativedelta(date2, date1)
		num_of_months= r.months


		if num_of_months==0:
			orders_per_month=0
			products_per_month=0
		else:
			orders_per_month= total_orders/num_of_months	
			products_per_month = total_products_bought/num_of_months

		print("orders_per_month: ",orders_per_month)
		print("products_per_month: ",products_per_month)


		if emi_applications==0:
			avg_amount_order_emi=0
		else:
			avg_amount_order_emi = total_amt_emi/ emi_applications
		print("avg_amount_order_emi: ",avg_amount_order_emi)


		prepayment=Payment.objects.filter(user_id=temp_customer).exclude(payment_type="cash on delivery", order_id=temp_order).count()
		print("prepayment: ",prepayment)


		x=Payment.objects.filter(user_id=temp_customer).exclude(payment_type="cash on delivery")
		count=0

		for temp in x:
			order_id1 = temp.order_id
			c = OrderDetails.objects.filter(order_id=order_id1).exclude(order_status="delivered").count()
			print("c: ",c)
			count = count+c
			print("count: ",count)
			c=0

		if prepayment==0:
			prepayment_rc=0
		else:
			prepayment_rc = count/prepayment

		print("prepayment_rc: ",prepayment_rc)


		x1=Payment.objects.filter(user_id=temp_customer).exclude(payment_type="credit card")
		count1=0;

		for temp in x1:
			order_id1 = temp.order_id
			c = OrderDetails.objects.filter(order_id=order_id1, order_status="delivered").count()
			print("c: ",c)
			count1 = count1+c
			print("count: ",count1)
			c=0

		if prepayment==0:
			prepayment_d=0
		else:
			prepayment_d = count1/prepayment

		print("prepayment_d: ",prepayment_d)














		#customer_credit table to be filled as well

############################################################################################


		x=CustomerCredit.objects.filter(user_id=user_id).first()
		max_credit = x.current_credit_limit
		if max_credit is None:
			max_credit=0;
		print("max_credit: ",max_credit)


		emi_on_time_count = EmiDetails.objects.filter(user_id=user_id, actual_date__in=F('expected_date')).exclude(order_id=temp_order.order_id).count()
		
		if emi_applications==0:
			avg_emi_on_time=0
		else:
			avg_emi_on_time = emi_on_time_count/emi_applications
		if avg_emi_on_time is None:
			avg_emi_on_time=0;
		print("avg_emi_on_time: ",avg_emi_on_time)


		if total_orders==0:
			debit_percent=0
		else:
			debit_percent = debit_card/total_orders
		if debit_percent is None:
			debit_percent=0;
		print("debit_percent: ",debit_percent)


		if total_orders==0:
			cod_percent=0
		else:
			cod_percent = cod/total_orders
		if cod_percent is None:
			cod_percent=0;
		print("cod_percent: ",cod_percent)


		if total_orders==0:
			credit_percent=0
		else:
			credit_percent = credit_card/total_orders
		if credit_percent is None:
			credit_percent=0;
		print("credit_percent: ",credit_percent)


		if total_orders==0:
			mobile_wallet_percent=0
		else:
			mobile_wallet_percent = mobile_wallet/total_orders
		if mobile_wallet_percent is None:
			mobile_wallet_percent=0;
		print("mobile_wallet_percent: ",mobile_wallet_percent)


		if total_orders==0:
			net_banking_percent=0
		else:
			net_banking_percent = net_banking/total_orders
		if net_banking_percent is None:
			net_banking_percent=0;
		print("net_banking_percent: ",net_banking_percent)


#########################################################################


		
		order_quantity = OrderDetails.objects.filter(order_id=temp_order).count()
		if order_quantity is None:
			order_quantity=0
		print("order_quantity: ",order_quantity)


		number_of_transactions = Order.objects.filter(user_id= temp_customer).count()
		if number_of_transactions is None:
			number_of_transactions=0
		print("number_of_transactions: ",number_of_transactions)



		buyers_profile_list=[age, pincode_class, total_orders, total_products_bought, total_amount_spent, credit_card, debit_card, net_banking, mobile_wallet, cod, delivered, returned, cancelled, mobile_wallet_used, emi_months, avg_price_order, avg_price_product, avg_emi_order_month, orders_per_month, products_per_month]

		model, min_val, max_val = load_model(settings.MODEL_URL + '/min_max_values.csv', settings.MODEL_URL + '/model.sav')
		score = predict_function(buyers_profile_list, model, min_val, max_val)

		print("score is: ",score[0])

		return JsonResponse({'credit_score' : 500, 'quantity': order_quantity, 'buyers_profile_score': score[0], 'number_of_transactions':number_of_transactions})

	else:
		return JsonResponse({'credit_score' : 0, 'quantity': 0, 'buyers_profile_score': 0, 'number_of_transactions':0})




#curl -X POST http://127.0.0.1:8000/pay/ -d '{"user_id":"2", "payment_option_id":"3"}' -H "Content-Type:application/json"
@csrf_exempt
def PayView(request):

#go to /pay
#input= user_id and payment_option_id
#1. CC   2. DC   3. COD   4. EMI   5. Netbanking(cancelled)   6. Mobile Wallets   7. MW + CC    8. MW + DC   9. MW + COD   10. MW + EMI  11. MW+Netbanking(cancelled) 12. Postpaid wallets
#output = user_id and number of emi installments



	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)

		user_id = body['user_id']
		payment_option_id = body['payment_option_id']


		temp_customer = Customer.objects.filter(user_id= user_id).first()
		if temp_customer is None:
			return JsonResponse({'message' : 'CustomerRetrievalError'})


		temp_order = Order.objects.filter(user_id=temp_customer).last()
		if temp_order is None:
			return JsonResponse({'message' : 'OrderRetrievalError'})

		payment_type="None"
		mobile_wallet_used="None"

		if payment_option_id=="1":
			payment_type="credit card"
			mobile_wallet_used= "no"
		elif payment_option_id=="2":
			payment_type="debit card"
			mobile_wallet_used= "no"
		elif payment_option_id=="3":
			payment_type="cash on delivery"
			mobile_wallet_used= "no"
		elif payment_option_id=="4":
			payment_type="EMI"
			mobile_wallet_used= "no"
		elif payment_option_id=="5":
			payment_type="net banking"
			mobile_wallet_used= "no"
		elif payment_option_id=="6":
			payment_type="mobile wallet"
			mobile_wallet_used= "yes"
		elif payment_option_id=="7":
			payment_type="credit card"
			mobile_wallet_used= "yes"
		elif payment_option_id=="8":
			payment_type="debit card"
			mobile_wallet_used= "yes"
		elif payment_option_id=="9":
			payment_type="cash on delivery"
			mobile_wallet_used= "yes"
		elif payment_option_id=="10":
			payment_type="EMI"
			mobile_wallet_used= "yes"
		elif payment_option_id=="11":
			payment_type="net banking"
			mobile_wallet_used= "yes"



		payment_obj =Payment.objects.create(user_id=temp_customer, order_id=temp_order, payment_type=payment_type, mobile_wallet_used=mobile_wallet_used)
		payment_obj.save()


		#calculating the number of installments which can be given to the user for emi
		if payment_option_id=="4" or payment_option_id=="10":

			number_of_products= OrderDetails.objects.filter(order_id=temp_order).count()

			if(number_of_products==1):
				product_price = OrderDetails.objects.filter(order_id=temp_order).values('total_price')
				for x in product_price:
					price=(x['total_price'])
				print(price)

				emi_3_value = price/3
				emi_6_value = price/6
				emi_12_value =price/12


				historic_emi_sum = EmiDetails.objects.filter(user_id=temp_customer).aggregate(Sum('emi_value'))['emi_value__sum']
				historic_number_of_installments = EmiDetails.objects.filter(user_id=temp_customer).count()
				avg_emi = (historic_emi_sum)/(historic_number_of_installments)


				value_3_diff = abs(avg_emi - emi_3_value) 
				value_6_diff = abs(avg_emi - emi_6_value) 
				value_12_diff = abs(avg_emi - emi_12_value) 

				vals=[value_3_diff, value_6_diff, value_12_diff]

				twoLargest = sorted(vals)[-2:]

				if value_3_diff in twoLargest:
					month_3=1
				else:
					month_3=0

				if value_6_diff in twoLargest:
					month_6=1
				else:
					month_6=0

				if value_12_diff in twoLargest:
					month_12=1
				else:
					month_12=0


				return JsonResponse({'user_id' : user_id, '3_months':month_3, '6_months':month_6, '12_months':month_12})



			else:
				return JsonResponse({'user_id' : user_id, '3_months':0, '6_months':0, '12_months':0})
		else:
				return JsonResponse({'user_id' : user_id, '3_months':0, '6_months':0, '12_months':0})

	else: 
		return JsonResponse({'user_id' : user_id, '3_months':0, '6_months':0, '12_months':0})



#curl -X POST http://127.0.0.1:8000/emi/ -d '{"user_id":"3", "number_of_installments":"3"}' -H "Content-Type:application/json"
@csrf_exempt
def EmiView(request):

#go to /emi
#takes user_id, number_of_installmets as input from client
#returns user_id to client


	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)


		user_id = body['user_id']
		number_of_installments = body['number_of_installments']


		temp_customer = Customer.objects.filter(user_id= user_id).first()
		if temp_customer is None:
			return JsonResponse({'message' : 'CustomerRetrievalError'})


		temp_order = Order.objects.filter(user_id=temp_customer).last()
		if temp_order is None:
			return JsonResponse({'message' : 'OrderRetrievalError'})


		temp_order_detail = OrderDetails.objects.filter(order_id=temp_order).first()
		if temp_order_detail is None:
			return JsonResponse({'message' : 'OrderDetailsRetrievalError'})

		product_id = temp_order_detail.product_id
		print("product id is: ",product_id)

		temp_product = Product.objects.filter(product_id=str(product_id)).first()
		print("HELLO")
		if temp_product is None:
			return JsonResponse({'message' : 'ProductRetrievalError'})


		product_price = temp_product.price
		print("product price is: ",product_price)


		emi_value = int(product_price) / int(number_of_installments)


		current_datetime = datetime.now()


		for i in range(int(number_of_installments)):
			current_datetime = current_datetime+relativedelta(months=+1)
			emi_obj =EmiDetails.objects.create(user_id=temp_customer, order_id=temp_order, emi_value=emi_value, installment_number=i+1, expected_date=current_datetime, actual_date=current_datetime, number_of_installments=number_of_installments)
			emi_obj.save()


		return JsonResponse({'user_id' : user_id})

	else:
		return JsonResponse({'user_id' : 'None'})



#curl -X POST http://127.0.0.1:8000/simulation/ -d '{"user_id":"2", "simulation_option":"1"}' -H "Content-Type:application/json"
@csrf_exempt
def SimulationView(request):

#go to /simulation
#client sends user_id and simulation option
# 1. buy  2. cancel  3. return  4. pay emi  5. miss emi


	if request.method == 'POST':
		body_unicode = request.body.decode('utf-8')
		body = json.loads(body_unicode)


		user_id = body['user_id']
		simulation_option = body['simulation_option']


		temp_customer = Customer.objects.filter(user_id= user_id).first()
		if temp_customer is None:
			return JsonResponse({'message' : 'CustomerRetrievalError'})


		temp_order = Order.objects.filter(user_id=temp_customer).last()
		if temp_order is None:
			return JsonResponse({'message' : 'OrderRetrievalError'})


		if simulation_option=="1":
			OrderDetails.objects.filter(order_id=temp_order).update(order_status="delivered")
		elif simulation_option=="2":
			OrderDetails.objects.filter(order_id=temp_order).update(order_status="cancelled")
		elif simulation_option=="3":
			OrderDetails.objects.filter(order_id=temp_order).update(order_status="returned")


		return JsonResponse({'user_id' : user_id})

	else:
		return JsonResponse({'user_id' : 'None'})



#curl -X POST http://127.0.0.1:8000/logout/ -d '{"user_id":"1"}' -H "Content-Type:application/json"
@csrf_exempt
def LogoutView(request):

	if request.method == 'POST':

		return JsonResponse({'user_id' : 'None'})

	else:
		return JsonResponse({'user_id' : 'None'})

