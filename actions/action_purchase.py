from comman import *

# =================================================Purchase======================================================

#Question 1
class PurchaseAmountAction(Action):
    def name(self) -> Text:
        return "action_purchase_purchase_amount_quater"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Calculate the date range for the current quarter
        today = datetime.datetime.today()
        quarter_start = (today - relativedelta(months=3)).replace(day=1)
        quarter_end = today.replace(day=1) - datetime.timedelta(days=1)

        # Search for all sale orders and their corresponding lines for this quarter
        po_orders = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
            [[['create_date', '>=', quarter_start.strftime('%Y-%m-%d')],
                ['create_date', '<=', quarter_end.strftime('%Y-%m-%d')]]],
            {'fields': ['amount_total']})
        # print(">>>>>>>>>purchase",po_orders)
        total_purchase_amount = sum(order['amount_total'] for order in po_orders)
        # print(">>>>>>>>>total_purchase_amount",total_purchase_amount)
        # Send the response to the user
        message = "The total amount spent on purchases this quarter is ${:.2f}".format(total_purchase_amount)
        dispatcher.utter_message(message)

        return []

#Question 2
class HighestQuantitySupplierAction(Action):
    def name(self) -> Text:
        return "action_purchase_highest_quantity_supplier_this_year"

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
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # Get the top 10 customers by revenue for the current year

        # Search for all purchase orders received this year
        purchase_orders = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
                                            [[['state', 'in', ['purchase', 'done']],
                                            ['date_order', '>=', first_day_of_year.strftime('%Y-%m-%d')]]],
                                            {'fields': ['partner_id', 'order_line']})
        # Calculate the quantity of goods provided by each supplier
        quantity_by_supplier = {}
        for order in purchase_orders:
            supplier_id = order['partner_id'][0]
            lines = order['order_line']
            purchase_orders_line = models.execute_kw(db, uid, password, 'purchase.order.line', 'search_read',
                                                    [[['order_id', '=', lines]]],
                                                    {'fields': ['partner_id', 'order_id', 'product_uom_qty']})
            quantity = sum(line['product_uom_qty'] for line in purchase_orders_line)
            if supplier_id in quantity_by_supplier:
                quantity_by_supplier[supplier_id] += quantity
            else:
                quantity_by_supplier[supplier_id] = quantity

        # Find the supplier with the highest quantity of goods
        highest_quantity = 0
        highest_quantity_supplier_id = None
        for supplier_id, quantity in quantity_by_supplier.items():
            if quantity > highest_quantity:
                highest_quantity = quantity
                highest_quantity_supplier_id = supplier_id

        # Get the name of the supplier with the highest quantity of goods
        highest_quantity_supplier = \
        models.execute_kw(db, uid, password, 'res.partner', 'read', [[highest_quantity_supplier_id]], {'fields': ['name']})[0]

        # Send the response to the user
        message = "The supplier who provided the highest quantity of goods this year is: {}".format(
            highest_quantity_supplier['name'])
        dispatcher.utter_message(message)

        return []

#Question 3
class AverageLeadTimeAction(Action):
    def name(self) -> Text:
        return "action_purchase_average_lead_time_action"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Retrieve average lead time for goods after placing an order
        orders = models.execute_kw(db, uid, password,
            'sale.order', 'search_read',
            [[['state', '=', 'sale'], ['picking_ids', '!=', False]]],
            {'fields': ['picking_ids']})
        
        # Calculate the average lead time
        lead_times = []
        for order in orders:
            picking_ids = order['picking_ids']
            pickings = models.execute_kw(db, uid, password,
                'stock.picking', 'search_read',
                [[['id', 'in', picking_ids], ['state', '=', 'done']]],
                {'fields': ['date_done', 'scheduled_date']})
            for picking in pickings:
                lead_time = (datetime.datetime.strptime(picking['date_done'], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(picking['scheduled_date'], "%Y-%m-%d %H:%M:%S")).days
                lead_times.append(lead_time)
        
        if lead_times:
            average_lead_time = sum(lead_times) / len(lead_times)
            message = f"The average lead time for receiving goods after placing an order is {average_lead_time} days."
            dispatcher.utter_message(text=message)
        else:
            dispatcher.utter_message(text="There are no orders in the system that have been delivered.")
       
        return []

#Question 4
class TopProductAction(Action):
    def name(self) -> Text:
        return "action_highest_purchase_volume_product_this_year"

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

        # Find the product with the highest purchase volume this year
        # Get the fields of the order_line model
        order_line_fields = models.execute_kw(db, uid, password, 'purchase.order.line', 'fields_get', [],
                                            {'attributes': ['string']})
        order_line_qty_field = next(
            field for field in order_line_fields if order_line_fields[field]['string'] == 'Quantity')
        order_line_product_field = next(
            field for field in order_line_fields if order_line_fields[field]['string'] == 'Product')
        order_line_name_field = next(
            field for field in order_line_fields if order_line_fields[field]['string'] == 'Description')

        orders = models.execute_kw(db, uid, password, 'purchase.order.line', 'search_read',
                                [[['state', 'in', ['purchase', 'done']],
                                    ['create_date', '>=', first_day_of_year.strftime('%Y-%m-%d')]]],
                                {'fields': [order_line_qty_field, order_line_product_field, order_line_name_field, 'order_id']
                                    })
        product_list = []
        for order in orders:
            top_product = order['product_id'][0]
            top_product_name = \
            models.execute_kw(db, uid, password, 'product.product', 'read', [[top_product]], {'fields': ['name']})[0][
                'name']
            product_list.append(top_product_name)
        message = f"The product with the highest purchase volume this year is {max(product_list, key=product_list.count)}."
        dispatcher.utter_message(text=message)
        return []

#Question 5

class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_credit_purchases_percentage_this_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Retrieve data on purchases made this month
        today = datetime.date.today()
        first_day_of_month = datetime.date(today.year, today.month, 1)
        last_day_of_month = datetime.date(today.year, today.month+1, 1) - datetime.timedelta(days=1)

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Search for purchases made between the first and last day of the month
        domain = [('date_order', '>=', str(first_day_of_month)), ('date_order', '<=', str(last_day_of_month))]
        purchase_ids = models.execute_kw(db, uid, password, 'purchase.order', 'search', [domain])

        # Retrieve payment method for each purchase
        payment_methods = []
        for purchase_id in purchase_ids:
            purchase = models.execute_kw(db, uid, password, 'purchase.order', 'read', [purchase_id])
            payment_methods.append(purchase['payment_term_id'][1])

        # Calculate percentage of purchases made on credit
        num_credit_purchases = payment_methods.count('Credit')
        total_purchases = len(payment_methods)
        if total_purchases == 0:
            percentage = 0
        else:
            percentage = num_credit_purchases / total_purchases * 100

        # Send response to user
        message = "This month, {}% of purchases were made on credit.".format(percentage)
        dispatcher.utter_message(text=message)

        return []

#Question 6

class CountCanceledPurchaseOrdersAction(Action):
    def name(self) -> Text:
        return "action_canceled_purchase_orders_this_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Define the start and end dates of the current quarter
        now = datetime.datetime.now()
        current_month = now.month
        current_quarter_start_month = ((current_month - 1) // 3) * 3 + 1
        current_quarter_end_month = current_quarter_start_month + 2
        current_quarter_start_date = datetime.date(now.year, current_quarter_start_month, 1)
        current_quarter_end_date = datetime.date(now.year, current_quarter_end_month, 1) + datetime.timedelta(days=32)
        current_quarter_end_date = current_quarter_end_date.replace(day=1) - datetime.timedelta(days=1)

        # Search for canceled purchase orders in the current quarter
        domain = [
            ('date_order', '>=', str(current_quarter_start_date)),
            ('date_order', '<=', str(current_quarter_end_date)),
            ('state', '=', 'cancel'),
        ]
        purchase_orders = models.execute_kw(db, uid, password, 'purchase.order', 'search_count', [domain])

        # Respond with the number of canceled purchase orders
        response = f"{purchase_orders} purchase orders were canceled this quarter."
        dispatcher.utter_message(text=response)

        return []

#Question 7

class AverageDiscountRateAction(Action):
    def name(self) -> Text:
        return "action_average_discount_rate_suppliers_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

       # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

       
        # Get the current year
        now = datetime.datetime.now()
        year = now.year

        # Search for supplier discounts negotiated during the current year
        domain = [('date_start', '<=', f'{year}-12-31'), ('date_end', '>=', f'{year}-01-01')]
        supplier_discounts = models.execute_kw(db, uid, password, 'product.supplierinfo', 'search_read', [domain],
                                                {'fields': ['discount']})

        # Extract the discount rates from the supplier discounts
        discount_rates = [red['discount'] for red in supplier_discounts]
        print(discount_rates)
        # Calculate the average discount rate
        if discount_rates:
            average_discount_rate = sum(discount_rates) / len(discount_rates)
        else:
            average_discount_rate = 0.0

        # Respond with the average discount rate
        response = f"The average negotiated discount rate with suppliers for this year is {average_discount_rate}%"
        # dispatcher.utter_message(text=response)
        dispatcher.utter_message(text=response)
        return []

#Question 8

class HighestPurchaseVolumeAction(Action):
    def name(self) -> Text:
        return "action_highest_purchase_volume_department_this_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Define the start and end dates of the current quarter
        today = datetime.datetime.now().date()
        year_start = datetime.date(today.year, 1, 1)
        year_end = datetime.date(today.year, 12, 31)

        # Retrieve the sales volume for each product sold this year
        lines = models.execute_kw(db, uid, password, 'purchase.order.line', 'search_read',
                                    [[('order_id.date_order', '>=', year_start.strftime('%Y-%m-%d')),
                                    ('order_id.date_order', '<=', year_end.strftime('%Y-%m-%d'))]],
                                    {'fields': ['product_id', 'product_uom_qty']})

        # Calculate the total sales volume for each product
        product_volumes = {}
        for line in lines:
            product_id = line['product_id'][0]
            product_volume = line['product_uom_qty']
            if product_id in product_volumes:
                product_volumes[product_id] += product_volume
            else:
                product_volumes[product_id] = product_volume

        # Find the product with the highest sales volume
        top_product_id = max(product_volumes, key=product_volumes.get)
        top_product = models.execute_kw(db, uid, password, 'product.product', 'read', [top_product_id], {'fields': ['name']})
        response = f"The product with the highest sales volume this year is {top_product[0]['name']}"
        dispatcher.utter_message(text=response)

        return []

#Question 9

class LatePurchaseOrdersAction(Action):
    def name(self) -> Text:
        return "action_late_purchase_orders_received_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        
        # Get the current year
        now = datetime.datetime.now()
        # year = now.year


        today = datetime.date.today()

        year = today.strftime("%Y")

        print(year)

        # Search for purchase orders received after their scheduled delivery date this year
        domain = [('state', '=', 'purchase'), ('delivery_date', '>=', f'{year}-01-01'),
            ('delivery_date', '<=', f'{year}-12-31')
            ]
        late_purchase_orders = models.execute_kw(db, uid, password, 'purchase.order', 'search_count', [domain])

        # Print the number of late purchase orders
        response = f"{late_purchase_orders} purchase orders were received late this year."

        dispatcher.utter_message(text=response)

        return []

#Question 10

class HighestAvgDeliveryTimeAction(Action):
    def name(self) -> Text:
        return "action_highest_average_delivery_time_supplier_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Define the start and end dates of the current year
        now = datetime.datetime.now()
        current_year_start_date = datetime.date(now.year, 1, 1)
        current_year_end_date = datetime.date(now.year, 12, 31)

        # Search for purchase orders received this year
        domain = [
            ('date_order', '>=', str(current_year_start_date)),
            ('date_order', '<=', str(current_year_end_date)),
            ('state', '=', 'done'),
        ]
        purchase_orders = models.execute_kw(db, uid, password, 'purchase.order', 'search_read', [domain], {'fields': ['partner_id', 'date_order', 'date_planned', 'date_approve', 'effective_date', 'effective_date']})

        # Calculate the average delivery time for each supplier
        delivery_times = defaultdict(list)
        for po in purchase_orders:
            supplier = models.execute_kw(db, uid, password, 'res.partner', 'read', [po['partner_id'][0]], {'fields': ['name']})[0]['name']
            print(po['effective_date'])
            # delivery_time = (datetime.datetime.strptime(po['effective_date'], models.DEFAULT_SERVER_DATETIME_FORMAT).date() - datetime.datetime.strptime(po['date_planned'], models.DEFAULT_SERVER_DATETIME_FORMAT).date()).days
            delivery_time =(datetime.datetime.strptime(po['effective_date'], "%Y-%m-%d %H:%M:%S") - datetime.datetime.strptime(po['date_planned'], "%Y-%m-%d %H:%M:%S")).days

            
            delivery_times[supplier].append(delivery_time)

        # Find the supplier with the highest average delivery time
        highest_avg_delivery_time_supplier = max(delivery_times.items(), key=lambda x: sum(x[1])/len(x[1]))[0]

        # Respond with the supplier and their average delivery time
        response = f"The supplier with the highest average delivery time this year is {highest_avg_delivery_time_supplier} with an average delivery time of {sum(delivery_times[highest_avg_delivery_time_supplier])/len(delivery_times[highest_avg_delivery_time_supplier])} days."
        dispatcher.utter_message(text=response)

        return []

#Question 11

class MostPurchasedProductAction(Action):
    def name(self) -> Text:
        return "most_purchased_product"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Define the start and end dates of the current month
        now = datetime.datetime.now()
        current_month_start_date = datetime.date(now.year, now.month, 1)
        current_month_end_date = datetime.date(now.year, now.month, calendar.monthrange(now.year, now.month)[1])

        # Search for purchase orders received this month
        domain = [
            ('date_order', '>=', str(current_month_start_date)),
            ('date_order', '<=', str(current_month_end_date)),
            ('state', '=', 'done'),
        ]
        purchase_orders = models.execute_kw(db, uid, password, 'purchase.order', 'search_read', [domain], {'fields': ['order_line']})

        # Calculate the total quantity of each product purchased this month
        product_quantities = {}
        for po in purchase_orders:
            for line in po['order_line']:
                product_id = line[2]['product_id'][0]
                product_qty = line[2]['product_qty']
                if product_id not in product_quantities:
                    product_quantities[product_id] = 0
                product_quantities[product_id] += product_qty

        # Find the product with the highest total quantity purchased this month
        product_id, total_qty = max(product_quantities.items(), key=lambda x: x[1])

        # Get the name of the product
        product_name = models.execute_kw(db, uid, password, 'product.product', 'read', [product_id], {'fields': ['name']})[0]['name']

        # Respond with the product and its total quantity purchased
        response = f"The most purchased product this month is {product_name} with a total quantity of {total_qty}."
        dispatcher.utter_message(text=response)

        return []

# =================================================//Purchase//==================================================
