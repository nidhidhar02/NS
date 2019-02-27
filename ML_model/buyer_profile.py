from sklearn.svm import SVR
import pandas as pd
import numpy as np
import pickle
from datetime import datetime
from dateutil import relativedelta
from sklearn.preprocessing import StandardScaler

########################################################################################################################################################################################################

def load_model(csv_filepath='min_max_values.csv', model_filepath='model.sav'):
    val = np.array(pd.read_csv(csv_filepath))
    model = pickle.load(open(model_filepath, 'rb'))
    min_val = val[0]
    max_val = val[1]
    return model, min_val, max_val

########################################################################################################################################################################################################
    
def predict_function(df, model, min_val, max_val):
    
    buyer_profile_db = []

    '''
    cust_age = df[cust == df['customer_id']]['customer_age'].values[0]
    cust_gender = df[cust == df['customer_id']]['customer_gender'].values[0]
    loc_class = df[cust == df['customer_id']]['loc_class'].values[0]

    temp = df[cust == df['customer_id']].sort_values(by='timestamp')

    #no. of orders placed by one customer
    total_orders = temp['order_id'].nunique()

    #no. of products bought by one customer
    total_products_bought = temp['product_id'].count()

    #total amount spent by one customer
    total_amount_spent = temp['price'].sum()

    #no. of times EMI was applied for
    emi_applications = temp[temp['installment_count'] > 1]['installment_count'].count()

    #no of emi months a customer has to pay
    if(temp[temp['installment_count'] > 1]['installment_count'].sum() > 0):
        emi_months = temp[temp['installment_count'] > 1]['installment_count'].sum()
    else:
        emi_months = 0

    #average price per order
    avg_price_order = total_amount_spent/total_orders

    #average price pr product
    avg_price_product = total_amount_spent/total_products_bought

    #average emi/order/month
    if(emi_months != 0):
        total_amount_spent_emi = temp[temp['installment_count'] > 1]['price'].sum()
        avg_emi_per_month = total_amount_spent_emi/emi_months
    else:
        total_amount_spent_emi = np.nan
        avg_emi_per_month = np.nan

    date1 = datetime.strptime(temp['timestamp'].iloc[0], '%Y-%m-%d %H:%M:%S')    
    date2 = datetime.strptime(temp['timestamp'].iloc[-1],'%Y-%m-%d %H:%M:%S')

    if(temp['timestamp'].nunique() > 1):
        month_int = float((date2 - date1).days)/30
    else:
        month_int = 1

    orders_per_month = temp['order_id'].nunique()/month_int
    products_per_month = temp['product_id'].count()/month_int

    #payment type used
    credit_card = temp[temp['payment_type'] == "credit card"]['payment_type'].count()
    debit_card = temp[temp['payment_type'] == "debit card"]['payment_type'].count()
    net_banking = temp[temp['payment_type'] == "net banking"]['payment_type'].count()
    mobile_wallet = temp[temp['payment_type'] == "mobile wallet"]['payment_type'].count()
    cod = temp[temp['payment_type'] == "cash on delivery"]['payment_type'].count()

    #order status
    delivered = temp[temp['order_status'] == "delivered"]['order_status'].count()
    returned = temp[temp['order_status'] == "returned"]['order_status'].count()
    cancelled = temp[temp['order_status'] == "cancelled"]['order_status'].count()

    #no. of times wallet used
    wallet_used = temp[temp['mobile_wallet_used'] == "yes"]['mobile_wallet_used'].count()
    

    buyer_profile = [cust_age, loc_class, total_orders, total_products_bought,
                     total_amount_spent, credit_card, debit_card, net_banking, mobile_wallet, cod,
                     delivered, returned, cancelled, wallet_used, emi_months, avg_price_order,
                     avg_price_product, avg_emi_per_month, orders_per_month, products_per_month]
    '''

    buyer_profile_db.append(df)
    db = pd.DataFrame(buyer_profile_db)
    print("DB: ",db)
    scaler = StandardScaler()
    db = scaler.fit_transform(db)
    y = model.predict(db)
    
    normalized_val = 100*(y - min_val)/(max_val - min_val)
    
    return normalized_val
    
########################################################################################################################################################################################################

# model, min_val, max_val = load_model()
# score = predict_function(df, model, min_val, max_val)
