from comman import *

# # =================================================Account + invoice ==================================================

# #Question 1

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_total_revenue_this_month"

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
        today = datetime.date.today()
        first_day_of_month = datetime.date(today.year, today.month, 1)
        last_day_of_month = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        # Search for all sale orders in the date range
        domain = [('date_order', '>=', first_day_of_month.strftime('%Y-%m-%d 00:00:00')), ('date_order', '<=', last_day_of_month.strftime('%Y-%m-%d 23:59:59')), ('state', 'in', ['sale', 'done'])]
        sale_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [domain], {'fields': ['amount_total']})

        # Calculate the total revenue of all sale orders
        total_revenue = sum(sale_order['amount_total'] for sale_order in sale_orders)

        # Respond with the total revenue for this month
        response = f"The total revenue for this month is {total_revenue:,.2f}."
        dispatcher.utter_message(text=response)

        return []

# Question 2

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_customer_highest_outstanding_balance_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        start_date = datetime.date.today().replace(month=1, day=1).strftime('%Y-%m-%d')
        end_date = datetime.date.today().strftime('%Y-%m-%d')

        invoices = models.execute_kw(db, uid, password, 'account.move', 'search_read', [[
            ['move_type', '=', 'out_invoice'],
            ['state', 'in', ['posted', 'draft']],
            ['invoice_date_due', '>=', start_date],
            ['invoice_date_due', '<=', end_date],
        ]], {'fields': ['partner_id', 'amount_residual']})

        customer_balances = {}
        for invoice in invoices:

            if invoice['partner_id'][0] in customer_balances:
                customer_balances[invoice['partner_id'][0]] += invoice['amount_residual']
            else:
                customer_balances[invoice['partner_id'][0]] = invoice['amount_residual']

        customer_id = max(customer_balances, key=customer_balances.get)

        customer = models.execute_kw(db, uid, password, 'res.partner', 'read', [customer_id], {'fields': ['name']})

        # print(customer)
        response = f"Customer with the highest outstanding balance this year is:{customer[0]['name']}"
        dispatcher.utter_message(response)

        return []   
    
# #Question 3

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_average_collection_time_invoices_this_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        
        today = datetime.date.today()
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        first_day_of_quarter = datetime.date(today.year, quarter_start_month, 1)
        last_day_of_quarter = datetime.date(today.year, quarter_start_month+2, calendar.monthrange(today.year, quarter_start_month+2)[1])

        # Search for all sale orders in the date range
        domain = [('date_order', '>=', first_day_of_quarter.strftime('%Y-%m-%d 00:00:00')), ('date_order', '<=', last_day_of_quarter.strftime('%Y-%m-%d 23:59:59')), ('state', 'in', ['sale', 'done'])]
        sale_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [domain], {'fields': ['date_order', 'commitment_date']})

        # Calculate the total delivery time for all sale orders
        total_delivery_time = 0
        num_deliveries = 0
        for sale_order in sale_orders:
            date_order = datetime.datetime.strptime(sale_order['date_order'], '%Y-%m-%d %H:%M:%S') if sale_order['date_order'] else False
            commitment_date = datetime.datetime.strptime(sale_order['commitment_date'], '%Y-%m-%d %H:%M:%S') if sale_order['commitment_date'] else False
            # print("<KKKKKKKKKKKKKKKKKdelivery_time",delivery_time)
            if date_order and commitment_date:
                delivery_time = commitment_date - date_order
                total_delivery_time += delivery_time.total_seconds() / 3600  # convert to hours
                num_deliveries += 1
            else:
                print("><<<<<<<<<<<<<<commitment_date",commitment_date) 
        # Calculate the average delivery time
        if num_deliveries > 0:
            avg_delivery_time = total_delivery_time / num_deliveries
            response = f"The average time taken to deliver products to customers this quarter is {avg_delivery_time:.2f} hours."
        else:
            response = "No deliveries found in the specified quarter."
        dispatcher.utter_message(text=response)
        return []
    
# #Question 4

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_product_category_highest_sales_volume_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # Retrieve the sales orders created this year
        year = '2023'
        order_ids = models.execute_kw(db, uid, password, 'sale.order', 'search', [[['date_order', '>=', year + '-01-01'], ['date_order', '<=', year + '-12-31']]])

        # Retrieve the line items for each sales order and calculate the total sales volume for each product category
        categories = {}
        for order_id in order_ids:
            lines = models.execute_kw(db, uid, password, 'sale.order.line', 'search_read', [[['order_id', '=', order_id]]], {'fields': ['product_id', 'product_uom_qty', 'price_unit']})
            for line in lines:
                if line['product_id']:
                    product = models.execute_kw(db, uid, password, 'product.product', 'read', [line['product_id'][0]], {'fields': ['name', 'categ_id']})

                    category = models.execute_kw(db, uid, password, 'product.category', 'search_read', [[]],{'fields': ['name']})
                    category_name = category[0]
                    quantity = line['product_uom_qty']

                    price = line['price_unit']
                    sales_volume = quantity * price

                    if category_name in [categories]:
                        # print('@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@2',category_name)
                        categories[category_name['name']] += sales_volume
                    else:
                        # print(categories[category_name] ,sales_volume)
                        categories[category_name['name']] = sales_volume

        # Sort the categories by sales volume in descending order and return the category with the highest sales volume
        sorted_categories = sorted(categories.items(), key=lambda x: x[1], reverse=True)
        highest_category = sorted_categories[0][0]

        response = f"The product category with the highest sales volume this year is {highest_category}."
        
        dispatcher.utter_message(response)

        return []
    
# #Question 5

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_number_of_invoices_issued_this_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        this_year = datetime.date.today().year
        start_date_q1 = datetime.date(this_year, 1, 1)
        end_date_q1 = datetime.date(this_year, 3, 31)

        start_date_q2 = datetime.date(this_year, 4, 1)
        end_date_q2 = datetime.date(this_year, 6, 30)

        start_date_q3 = datetime.date(this_year, 7, 1)
        end_date_q3 = datetime.date(this_year, 9, 30)

        start_date_q4 = datetime.date(this_year, 10, 1)
        end_date_q4 = datetime.date(this_year, 12, 31)

        domain_q1 = [('move_type', '=', 'out_invoice'),('invoice_date', '>=', start_date_q1.strftime('%Y-%m-%d')),
                ('invoice_date', '<=', end_date_q1.strftime('%Y-%m-%d'))]

        domain_q2 = [('move_type', '=', 'out_invoice'),('invoice_date', '>=', start_date_q2.strftime('%Y-%m-%d')),
                ('invoice_date', '<=', end_date_q2.strftime('%Y-%m-%d'))]

        domain_q3 = [('move_type', '=', 'out_invoice'),('invoice_date', '>=', start_date_q3.strftime('%Y-%m-%d')),
                ('invoice_date', '<=', end_date_q3.strftime('%Y-%m-%d'))]

        domain_q4 = [('move_type', '=', 'out_invoice'),('invoice_date', '>=', start_date_q4.strftime('%Y-%m-%d')),
                ('invoice_date', '<=', end_date_q4.strftime('%Y-%m-%d'))]

        invoices_q1 = models.execute_kw(db, uid, password, 'account.move', 'search_read', [domain_q1], {'fields': ['name', 'amount_residual', 'partner_id']})
        invoices_q2 = models.execute_kw(db, uid, password, 'account.move', 'search_read', [domain_q2], {'fields': ['name', 'amount_residual', 'partner_id']})
        invoices_q3 = models.execute_kw(db, uid, password, 'account.move', 'search_read', [domain_q3], {'fields': ['name', 'amount_residual', 'partner_id']})
        invoices_q4 = models.execute_kw(db, uid, password, 'account.move', 'search_read', [domain_q4], {'fields': ['name', 'amount_residual', 'partner_id']})

        invoice_sum_q1 = 0
        invoice_sum_q2 = 0
        invoice_sum_q3 = 0
        invoice_sum_q4 = 0

        for inv1 in invoices_q1:
            invoice_sum_q1+=1

        for inv2 in invoices_q2:
            invoice_sum_q2+=1

        for inv3 in invoices_q3:
            invoice_sum_q3+=1

        for inv4 in invoices_q4:
            invoice_sum_q4+=1

        response = f"Number of invoices Issued \n (Jan - Mar) are {invoice_sum_q1} \n (April - June) are {invoice_sum_q2} \n (July - Sep) are {invoice_sum_q3} \n (Oct - Dec) are {invoice_sum_q4}."

        dispatcher.utter_message(response)

        return []
    
#Question 6

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_average_invoice_amount_per_customer_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        this_year = datetime.date.today().year
        first_day_of_year = datetime.date(this_year, 1, 1)
        last_day_of_year = datetime.date(this_year, 12, 31)

        domain = [('invoice_date', '>=', first_day_of_year.strftime('%Y-%m-%d 00:00:00')), ('invoice_date', '<=', last_day_of_year.strftime('%Y-%m-%d 23:59:59'))]
        invoices = models.execute_kw(db, uid, password, 'account.move', 'search_read', [domain], {'fields': ['amount_total_signed']})
        total_invoice_amount = 0
        invoice_num = 0

        for inv in invoices:
            total_invoice_amount += inv['amount_total_signed']
            invoice_num += 1

        response = f"The average invoice amount per customer is  {total_invoice_amount/invoice_num:,.2f}"
        dispatcher.utter_message(response)

        return []
    
# #Question 7

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_number_of_overdue_invoices_currently"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        today_date = datetime.datetime.now().strftime('%Y-%m-%d')
        result = [('move_type','=','out_invoice'),('invoice_date_due', '<', today_date)]
        customer_name=models.execute_kw(db, uid, password, 'account.move', 'search_count',[result])
        response = f"The Number of overdue invoices are {customer_name}."
        dispatcher.utter_message(response)

        return []
    
#Question 8

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_salesperson_highest_revenue_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        invoices = models.execute_kw(db, uid, password,
                                      'account.move', 'search_read',
                                      [[('invoice_user_id.name', '=', 'Administrator')]], {'fields': ['id', 'name', 'invoice_user_id']})

        for i in invoices:
            response = f"Sales person which has generated the highest revenue is  {i['invoice_user_id'][1]}."
        dispatcher.utter_message(response)

        return []
    
#Question 9

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_average_discount_rate_offered_to_customers_this_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        model_name = 'sale.order.line'

        # Calculate the start date and end date for the current quarter
        today = datetime.datetime.today()
        quarter_start = datetime.datetime(today.year, (today.month - 1) // 3 * 3 + 1, 1)
        quarter_end = datetime.datetime(today.year, (today.month - 1) // 3 * 3 + 4, 1) - timedelta(days=1)

        # Define a domain to filter the sale orders for this quarter
        domain = [
            ('date_order', '>=', quarter_start),
            ('date_order', '<=', quarter_end),
        ]

        # Fetch the sale orders for this quarter
        fields = ['id']
        sale_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [domain], {'fields': fields})
        # Define a domain to filter the sale order lines for this quarter
        domain = [
            ('order_id', 'in', [sale_order['id'] for sale_order in sale_orders]),
            ('discount', '!=', 0.0),
        ]
        fields = ['discount']
        sale_order_lines = models.execute_kw(db, uid, password, model_name, 'search_read', [domain], {'fields': fields})
        print(sale_order_lines)
        if sale_order_lines:
            total_discount_rate = sum(sale_order_line['discount'] for sale_order_line in sale_order_lines)
            average_discount_rate = total_discount_rate / len(sale_order_lines)
            response = "The average discount rate offered to customers this quarter is: {:.2f}".format(average_discount_rate)
        else:
            response = "No discount rates found for this quarter."
        dispatcher.utter_message(response)

        return []
    
#Question 10

class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_ai_most_common_payment_method_used_by_customers_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        current_year =str(datetime.datetime.now().year)
        domain = [('journal_id', '!=', False),('date', '>=',current_year+'-01-01'), ('date', '<=',current_year+'-12-31')]
        fields = ['journal_id']
        payments = models.execute_kw(db, uid, password, 'account.payment', 'search_read', [domain], {'fields': fields})

        payment_counts = {}
        for payment in payments:
            journal_id = payment['journal_id'][1]
            if journal_id in payment_counts:
                payment_counts[journal_id] += 1
            else:
                payment_counts[journal_id] = 1

        most_common_payment = max(payment_counts, key=payment_counts.get)
        response = 'The payment method that is most commonly used by customers is: {}'.format(most_common_payment)
        dispatcher.utter_message(response)

        return []

# # =================================================//Account + invoice //==================================================

# # =============================================fall=========================================================

class ActionDefaultFallback(Action):
    """Executes the fallback action and goes back to the previous state
    of the dialogue"""

    def name(self) -> Text:
        return "action_fallback"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        fallback_message = tracker.latest_message.get('text')
        jay = tracker.sender_id
        # Open the file for appending and get the next sequence number
        with open('user_messages.txt', 'a') as f:
            f.write(f'=> {fallback_message} , {jay} \n')

        dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]

# # =============================================//fall//=========================================================
