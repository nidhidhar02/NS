from django.db import models
from datetime import datetime

# Create your models here.

DEFAULT_ORDER_ID = 1
class Customer(models.Model):

	user_id = models.AutoField(primary_key=True)
	password = models.CharField(max_length=20)
	email = models.EmailField(max_length=80, unique=True)
	fname = models.CharField(max_length=20)
	lname = models.CharField(max_length=20)
	age= models.IntegerField()
	address = models.CharField(max_length=240)
	city = models.CharField(max_length=30)
	state = models.CharField(max_length=30)
	pincode = models.IntegerField()
	phone = models.IntegerField()
	gender = models.CharField(max_length=30)


	def __str__(self):
		return str(self.user_id)



class PinCode(models.Model):

	pincode = models.IntegerField(primary_key=True)
	pincode_class = models.IntegerField()


	def __str__(self):
		return str(self.pincode)



class CustomerCredit(models.Model):

	user_id = models.ForeignKey(Customer, to_field='user_id', on_delete=models.CASCADE)
	initial_credit_limit = models.IntegerField()
	current_credit_limit = models.IntegerField()
	credit_score = models.IntegerField()
	credit_utilization = models.IntegerField()


	def __str__(self):
		return str(self.user_id)




class Product(models.Model):

	product_id = models.AutoField(primary_key=True)
	product_name = models.CharField(max_length=30)
	product_category = models.CharField(max_length=30)
	price = models.IntegerField()


	def __str__(self):
		return str(self.product_id)




class Order(models.Model):

	order_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(Customer, to_field='user_id', on_delete=models.CASCADE)
	bill_amount = models.IntegerField()
	timestamp= models.DateTimeField(auto_now=True)


	def __str__(self):
		return str(self.order_id)




class OrderDetails(models.Model):


	user_id = models.ForeignKey(Customer, to_field='user_id', on_delete=models.CASCADE)
	order_id = models.ForeignKey(Order, to_field='order_id', on_delete=models.CASCADE, default = DEFAULT_ORDER_ID)
	product_id = models.ForeignKey(Product, to_field='product_id', on_delete=models.CASCADE)
	order_status = models.CharField(max_length=30, default="Nothing")
	quantity = models.IntegerField()
	total_price = models.IntegerField()


	def __str__(self):
		return str(self.order_id)




class Payment(models.Model):

	user_id = models.ForeignKey(Customer, to_field='user_id', on_delete=models.CASCADE)
	order_id = models.ForeignKey(Order, to_field='order_id', on_delete=models.CASCADE, default = DEFAULT_ORDER_ID)
	payment_type = models.CharField(max_length=30)
	mobile_wallet_used = models.CharField(max_length=30)


	def __str__(self):
		return str(self.order_id)




class EmiDetails(models.Model):

	user_id = models.ForeignKey(Customer, to_field='user_id', on_delete=models.CASCADE)
	order_id = models.ForeignKey(Order, to_field='order_id', on_delete=models.CASCADE, default = DEFAULT_ORDER_ID)
	emi_value = models.IntegerField()
	installment_number = models.IntegerField()
	expected_date = models.DateTimeField()
	actual_date = models.DateTimeField()
	number_of_installments = models.IntegerField(default = 1)


	def __str__(self):
		return str(self.user_id)



class Cart(models.Model):

	user_id = models.ForeignKey(Customer, to_field='user_id', on_delete=models.CASCADE)
	order_id = models.AutoField(primary_key=True)
	bill_amount = models.IntegerField()

	def __str__(self):
		return str(self.user_id)
    


#adding data from csv to model:

# In [1]: from allapps.models import PinCode

# In [2]: import csv

# In [3]: with open('/home/nidhi/Documents/vedangsample/location_db.csv') as csvfile:
#    ...:     reader = csv.DictReader(csvfile)
#    ...:     for row in reader:
#    ...:         p = PinCode(pincode=int(row['Pincode']), pincode_class=int(row['Class']))
#    ...:         p.save()




#find difference in months between 2 dates:

# start=EmiDetails.objects.values('actual_date').filter(user_id=1).first()
# print(start)
# start=start['actual_date']
# end=EmiDetails.objects.values('actual_date').filter(user_id=1).last()
# end=end['actual_date']
# start=str(start).split(".")[0]
# end=str(end).split(".")[0]


# from datetime import datetime
# from dateutil import relativedelta
# date1 = datetime.strptime(str(start), '%Y-%m-%d %H:%M:%S')
# date2 = datetime.strptime(str(end),'%Y-%m-%d %H:%M:%S')
# r = relativedelta.relativedelta(date2, date1)
# r= r.months + 1

