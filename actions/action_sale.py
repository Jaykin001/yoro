
from comman import *

# =================================================sales==================================================

# Question 1
class TotalRevenueAction(Action):
    def name(self) -> Text:
        return "action_sale_total_revenue_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
       
        # Get the current quarter start and end dates
        today = datetime.datetime.now().date()
        quarter_start = datetime.date(today.year, (today.month - 1) // 3 * 3 + 1, 1)
        quarter_end = datetime.date(today.year, (today.month - 1) // 3 * 3 + 4, 1) - datetime.timedelta(days=1)

        # Retrieve the total revenue for the current quarter
        orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read', 
                                   [[('date_order', '>=', quarter_start.strftime('%Y-%m-%d')),
                                     ('date_order', '<=', quarter_end.strftime('%Y-%m-%d'))]], 
                                   {'fields': ['amount_total']})
        total_revenue = sum([order['amount_total'] for order in orders])
        message = f"The total revenue generated this quarter is {total_revenue:.2f}"
        # Send the response to the user
        dispatcher.utter_message(text=message)

        return [] 
    
# Question 2
class TopProductAction(Action):
    def name(self) -> Text:
        return "action_sale_highest_sales_volume_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the start and end dates of the current year
        today = datetime.datetime.now().date()
        year_start = datetime.date(today.year, 1, 1)
        year_end = datetime.date(today.year, 12, 31)

        # Retrieve the sales volume for each product sold this year
        lines = models.execute_kw(db, uid, password, 'sale.order.line', 'search_read',
                                  [[('order_id.date_order', '>=', year_start.strftime('%Y-%m-%d')),
                                    ('order_id.date_order', '<=', year_end.strftime('%Y-%m-%d'))]],
                                  {'fields': ['product_id', 'product_uom_qty']})

        # Calculate the total sales volume for each product
        # Calculate the total sales volume for each product
        product_volumes = {}
        for line in lines:
            if line['product_id']:
                product_id = line['product_id'][0]
                product_volume = line['product_uom_qty']
                if product_id in product_volumes:
                    product_volumes[product_id] += product_volume
                else:
                    product_volumes[product_id] = product_volume


        # Find the product with the highest sales volume
        top_product_id = max(product_volumes, key=product_volumes.get)
        top_product = models.execute_kw(db, uid, password, 'product.product', 'read', [top_product_id], {'fields': ['name']})

        # Send the response to the user
        dispatcher.utter_message(text=f"The product with the highest sales volume this year is {top_product[0]['name']}.")

        return []
   
# Question 3 | not-done

class AverageDeliveryTimeAction(Action):
    def name(self) -> Text:
        return "action_sale_average_delivery_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the start and end dates of the current year
        today = datetime.datetime.now().date()
        year_start = datetime.date(today.year, 1, 1)
        year_end = datetime.date(today.year, 12, 31)

        # Retrieve the delivery time for each order fulfilled this year
        orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
                                    [[('state', '=', 'done'),
                                      ('date_order', '>=', year_start.strftime('%Y-%m-%d')),
                                      ('date_order', '<=', year_end.strftime('%Y-%m-%d')),
                                      ('date_delivery', '!=', False)]],
                                    {'fields': ['date_order', 'date_delivery']})

        # Calculate the total delivery time for all orders
        total_delivery_time = datetime.timedelta(0)
        for order in orders:
            date_order = datetime.datetime.strptime(order['date_order'], '%Y-%m-%d %H:%M:%S').date()
            date_delivery = datetime.datetime.strptime(order['date_delivery'], '%Y-%m-%d %H:%M:%S').date()
            delivery_time = date_delivery - date_order
            total_delivery_time += delivery_time

        # Calculate the average delivery time for orders fulfilled this year
        if len(orders) > 0:
            average_delivery_time = total_delivery_time / len(orders)
            average_delivery_days = average_delivery_time.days
            dispatcher.utter_message(text=f"The average delivery time for orders fulfilled this year is {average_delivery_days} days.")
        else:
            dispatcher.utter_message(text="There were no orders fulfilled this year.")

        return []

#Question 4

# class SearchSaleOrders(Action):
#     def name(self) -> Text:
#         return "action_sale_number_orders_month"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         # Add the code you want to execute in this function
#         HOST = '192.168.0.145'
#         PORT = 3333
#         DB = 'mar6_rapid_bevtech'
#         USER = 'admin'
#         PASS = 'admin'

#         def json_rpc(url, method, params):
#             data = {
#                 "jsonrpc": "2.0",
#                 "method": method,
#                 "params": params,
#                 "id": random.randint(0, 1000000000)
#             }

#             req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
#                 "Content-Type": "application/json",
#             })
#             reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
#             if reply.get("error"):
#                 raise Exception(reply["error"])
#             return reply["result"]


#         def call(url, service, method, *args):
#             return json_rpc(url, "call", {"service": service, "method": method, "args": args})


#         url = f"http://{HOST}:{PORT}/jsonrpc"
#         uid = call(url, "common", "login", DB, USER, PASS)

#         today = datetime.datetime.now()
#         month_start = datetime.datetime(today.year, today.month, 1)
#         month_end = datetime.datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

#         args = [('state', '=', 'sale'),
#                 ('date_order', '>=', month_start.strftime('%Y-%m-%d')),
#                 ('date_order', '<=', month_end.strftime('%Y-%m-%d'))]

#         note_id = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'search_count', args)
#         # total_revenue = sum([order['amount_total'] for order in note_id])
#         response = f"Searching records{note_id}"
#             # response = f"Total revenue for the current month is {total_revenue}."
#         dispatcher.utter_message(response)

#         return []

class TotalOrdersThisMonthAction(Action):
    def name(self) -> Text:
        return "action_sale_number_orders_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the start and end dates of the current month
        today = datetime.datetime.now().date()
        month_start = datetime.date(today.year, today.month, 1)
        month_end = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        # Retrieve the orders received this month
        orders = models.execute_kw(db, uid, password, 'sale.order', 'search_count',
                                    [[('state', '=', 'sale'),
                                      ('date_order', '>=', month_start.strftime('%Y-%m-%d')),
                                      ('date_order', '<=', month_end.strftime('%Y-%m-%d'))]])

        # Send a message to the user with the total number of orders received this month
        dispatcher.utter_message(text=f"{orders} orders have been received this month.")

        return []

#Question 5 

class TotalSalesRevenueBySalesperson(Action):
    def name(self) -> Text:
        return "action_sale_revenue_by_salesperson"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Define search criteria for sales orders
        search_domain = [
            ('date_order', '>=', '2023-01-01'),
            ('date_order', '<=', '2023-03-31'),
            ('state', 'in', ['sale', 'done'])
        ]

        # Search for sales orders with the specified criteria
        sales_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
                                         [search_domain],
                                         {'fields': ['user_id', 'amount_total']})

        # Aggregate sales revenue by salesperson
        sales_by_salesperson = {}
        for order in sales_orders:
            salesperson_id = order['user_id'][0]
            revenue = order['amount_total']
            if salesperson_id not in sales_by_salesperson:
                sales_by_salesperson[salesperson_id] = revenue
            else:
                sales_by_salesperson[salesperson_id] += revenue

        # Format the results for display
        message = "Sales revenue by salesperson this quarter:\n"
        for salesperson_id, revenue in sales_by_salesperson.items():
            salesperson_name = models.execute_kw(db, uid, password, 'res.users', 'read',
                                                  [salesperson_id],
                                                  {'fields': ['name']})[0]['name']
            message += f"- {salesperson_name}: ${revenue:.2f}\n"

        # Send the message to the user
        dispatcher.utter_message(text=message)

        return []

#Question 6 

class CountCreditSalesAction(Action):
    def name(self) -> Text:
        return "action_sale_count_credit_sales"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the date range for this month
        today = datetime.datetime.today()
        first_day_of_month = datetime.datetime(today.year, today.month, 1)
        last_day_of_month = first_day_of_month + datetime.timedelta(days=31)

        # Search for all sale orders created this month
        sale_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
            [[['date_order', '>=', first_day_of_month.strftime('%Y-%m-%d')],
            ['date_order', '<', last_day_of_month.strftime('%Y-%m-%d')]]],
            {'fields': ['invoice_status']})

        # Count the number of sale orders made on credit
        credit_sales_count = 0
        for sale_order in sale_orders:
            if sale_order['invoice_status'] == 'to invoice':
                credit_sales_count += 1
                
        # Calculate the percentage of sales made on credit
        total_sales_count = len(sale_orders)
        if total_sales_count != 0:
            credit_sales_percentage = credit_sales_count / total_sales_count * 100
        else:
            credit_sales_percentage = 0

        # Send the response to the user
        message = "This month, {:.2f}% of sales were made on credit.".format(credit_sales_percentage)
        dispatcher.utter_message(message)

        return []

#Question 7

class TopCustomerAction(Action):
    def name(self) -> Text:
        return "action_sale_top_customer"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the date range for this year
        today = datetime.datetime.today()
        first_day_of_year = datetime.datetime(today.year, 1, 1)
        last_day_of_year = datetime.datetime(today.year, 12, 31)

        # Search for all sale orders created this year
        sale_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
            [[['date_order', '>=', first_day_of_year.strftime('%Y-%m-%d')],
            ['date_order', '<=', last_day_of_year.strftime('%Y-%m-%d')]]],
            {'fields': ['partner_id', 'amount_total']})

        # Calculate the total sales volume for each customer
        customer_sales = {}
        for sale_order in sale_orders:
            customer_id = sale_order['partner_id'][0]
            sales_amount = sale_order['amount_total']
            if customer_id in customer_sales:
                customer_sales[customer_id] += sales_amount
            else:
                customer_sales[customer_id] = sales_amount

        # Get the customer with the highest sales volume
        top_customer_id = max(customer_sales, key=customer_sales.get)
        top_customer = models.execute_kw(db, uid, password, 'res.partner', 'read', [top_customer_id], {'fields': ['name']})


        # Send the response to the user
        message = "The customer with the highest sales volume this year is {}.".format(top_customer[0]['name'])
        dispatcher.utter_message(message)

        return []

#Question 8

class AvgDiscountRateAction(Action):
    def name(self) -> Text:
        return "action_sale_average_discount_rate_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the date range for this year
        today = datetime.datetime.today()
        first_day_of_year = datetime.datetime(today.year, 1, 1)

        # Search for all sale order lines with a discount this year
        sale_order_lines = models.execute_kw(db, uid, password, 'sale.order.line', 'search_read',
            [[['create_date', '>=', first_day_of_year.strftime('%Y-%m-%d')],
            ['discount', '>', 0]]],
            {'fields': ['discount', 'product_uom_qty']})

        # Calculate the total discount and total quantity of sale order lines
        total_discount = 0
        total_quantity = 0
        for sale_order_line in sale_order_lines:
            total_discount += sale_order_line['discount'] * sale_order_line['product_uom_qty']
            total_quantity += sale_order_line['product_uom_qty']

        # Calculate the average discount rate offered to customers this year
        if total_quantity > 0:
            avg_discount_rate = total_discount / total_quantity
        else:
            avg_discount_rate = 0

        # Send the response to the user
        message = "This year, the average discount rate offered to customers is {:.2f}%.".format(avg_discount_rate)
        dispatcher.utter_message(message)

        return []

#Question 9

class AverageGrossMarginAction(Action):
    def name(self) -> Text:
        return "action_sale_avg_gross_margin_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Retrieve the average gross margin for sales this quarter
        start_date = datetime.date.today().replace(day=1)
        end_date = start_date + relativedelta(months=3) - relativedelta(days=1)
        domain = [
            ('date', '>=', start_date.strftime('%Y-%m-%d')),
            ('date', '<=', end_date.strftime('%Y-%m-%d')),
            ('state', 'not in', ['draft', 'cancel']),
        ]
        fields = ['margin']
        result = models.execute_kw(db, uid, password, 'account.move', 'search_read', [domain], {'fields': fields})
        total_margin = sum([r['margin'] for r in result])
        count = len(result)
        if count == 0:
            average_margin = 0
        else:
            average_margin = round(total_margin / count, 2)

        # Send the response back to the user
        message = f"The average gross margin for sales this quarter is {average_margin}."
        dispatcher.utter_message(text=message)
       
        return []

#Question 10

class RevenueByCategoryAction(Action):
    def name(self) -> Text:
        return "action_sale_revenue_by_category_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the date range for this year
        today = datetime.datetime.today()
        first_day_of_year = datetime.datetime(today.year, 1, 1)

        # Search for all product templates with a category this year
        product_templates = models.execute_kw(db, uid, password, 'product.template', 'search_read',
            [[['categ_id', '!=', False],
            ['create_date', '>=', first_day_of_year.strftime('%Y-%m-%d')]]],
            {'fields': ['categ_id', 'list_price', 'default_code', 'name']})

        # Calculate the total revenue by category
        revenue_by_category = {}
        for product_template in product_templates:
            category_id = product_template['categ_id'][0]
            list_price = product_template['list_price']
            revenue = models.execute_kw(db, uid, password, 'sale.order.line', 'search_count',
                [[['product_id.product_tmpl_id', '=', product_template['id']],
                ['order_id.invoice_status', '=', 'invoiced'],
                ['create_date', '>=', first_day_of_year.strftime('%Y-%m-%d')]]]) * list_price
            if category_id in revenue_by_category:
                revenue_by_category[category_id] += revenue
            else:
                revenue_by_category[category_id] = revenue

        # Send the response to the user
        if not revenue_by_category:
            message = "There were no sales made in any product category this year."
        else:
            message = "The total revenue generated by product category this year is:\n\n"
            for category_id, revenue in revenue_by_category.items():
                category = models.execute_kw(db, uid, password, 'product.category', 'read', [[category_id]], {'fields': ['name']})[0]
                message += "{}: ${:.2f}\n".format(category['name'], revenue)
        dispatcher.utter_message(message)

        return []

#Question 11

class CanceledSalesOrderAction(Action):
    def name(self) -> Text:
        return "action_sale_canceled_sales_order_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the date range for this month
        today = datetime.datetime.today()
        first_day_of_month = datetime.datetime(today.year, today.month, 1)

        # Search for all canceled sales orders this month
        canceled_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read',
            [[['state', '=', 'cancel'],
            ['date_order', '>=', first_day_of_month.strftime('%Y-%m-%d')]]],
            {'fields': ['name', 'date_order', 'partner_id', 'user_id', 'amount_total']})

        # Send the response to the user
        if not canceled_orders:
            message = "There are no canceled sales orders for this month."
            dispatcher.utter_message(message)
        else:
            message = "Here are the details of canceled sales orders for this month:\n\n"
            for order in canceled_orders:
                message += "Order Name: {}\n".format(order['name'])
                message += "Order Date: {}\n".format(order['date_order'])
                partner = models.execute_kw(db, uid, password, 'res.partner', 'read', [[order['partner_id'][0]]], {'fields': ['name']})[0]
                message += "Customer: {}\n".format(partner['name'])
                user = models.execute_kw(db, uid, password, 'res.users', 'read', [[order['user_id'][0]]], {'fields': ['name']})[0]
                message += "Salesperson: {}\n".format(user['name'])
                message += "Total Amount: ${:.2f}\n\n".format(order['amount_total'])
            dispatcher.utter_message(message)

        return []

# =================================================//End-sales//==================================================


