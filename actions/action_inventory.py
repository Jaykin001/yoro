from comman import *

# =================================================Inventory==================================================
#Question 1

class InventoryValueAction(Action):
    def name(self) -> Text:
        return "action_inventory_current_inventory_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Search for all products in the system
        products = models.execute_kw(db, uid, password, 'stock.valuation.layer', 'search_read',
                                    [[('product_id.type', '=', 'product')]],
                                    {'fields': ['quantity','unit_cost','value']})

        # Calculate the total inventory value of all products
        total_inventory_value = 0
        for product in products:
            total_inventory_value += product['value']

        # Respond with the total inventory value
        response = f"The current inventory value of our products is {total_inventory_value:,.2f} units"
        dispatcher.utter_message(text=response)

        return []

#Question 2

class HighestDemandAction(Action):
    def name(self) -> Text:
        return "action_inventory_highest_demand_product_this_month"

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
        first_day_of_month = datetime.date(today.year, today.month, 1)
        last_day_of_month = datetime.date(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        # Search for all sale orders in the date range
        domain = [('order_id.date_order', '>=', first_day_of_month.strftime('%Y-%m-%d 00:00:00')),
                ('order_id.date_order', '<=', last_day_of_month.strftime('%Y-%m-%d 23:59:59')),
                ('state', 'in', ['sale', 'done'])]
        sale_orders = models.execute_kw(db, uid, password, 'sale.order.line', 'search_read', [domain],
                                        {'fields': ['product_uom_qty']})

        print(sale_orders)
        # Sum up the quantities of each product in all sale orders
        product_quantities = {}
        for sale_order in sale_orders:
            product_id = sale_order['id']
            product_qty = sale_order['product_uom_qty']
            if product_id in product_quantities:
                product_quantities[product_id] += product_qty
            else:
                product_quantities[product_id] = product_qty

        # Get the product with the highest demand this month
        highest_demand_product_id = max(product_quantities, key=product_quantities.get)
        highest_demand_product = \
            models.execute_kw(db, uid, password, 'product.product', 'read', [highest_demand_product_id],
                            {'fields': ['name']})[0]['name']

        # Respond with the product with the highest demand
        response = f"The product with the highest demand this month is {highest_demand_product}."
        dispatcher.utter_message(text=response)
        return []

#Question 3
class AvgDeliveryTimeAction(Action):
    def name(self) -> Text:
        return "action_inventory_average_delivery_time_this_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Get the date range for this quarter
        today = datetime.date.today()
        quarter_start_month = ((today.month - 1) // 3) * 3 + 1
        first_day_of_quarter = datetime.date(today.year, quarter_start_month, 1)
        last_day_of_quarter = datetime.date(today.year, quarter_start_month + 2,
                                            calendar.monthrange(today.year, quarter_start_month + 2)[1])

        # Search for all sale orders in the date range
        domain = [('date_order', '>=', first_day_of_quarter.strftime('%Y-%m-%d 00:00:00')),
                ('date_order', '<=', last_day_of_quarter.strftime('%Y-%m-%d 23:59:59')), ('state', '=', 'done')]
        sale_orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read', [domain],
                                        {'fields': ['date_order', 'done_date']})

        # Calculate the total delivery time for all sale orders
        total_delivery_time = 0
        num_deliveries = 0
        for sale_order in sale_orders:
            date_order = datetime.datetime.strptime(sale_order['date_order'], '%Y-%m-%d %H:%M:%S')
            commitment_date = datetime.datetime.strptime(sale_order['done_date'], '%Y-%m-%d %H:%M:%S')
            delivery_time = commitment_date - date_order
            total_delivery_time += delivery_time.total_seconds() / 3600  # convert to hours
            num_deliveries += 1

        # Calculate the average delivery time
        if num_deliveries > 0:
            avg_delivery_time = total_delivery_time / num_deliveries
            response = f"The average time taken to deliver products to customers this quarter is {avg_delivery_time:.2f} hours."
        else:
            response = "No deliveries found in the specified quarter."
        # Respond with the average delivery time
        dispatcher.utter_message(text=response)

        return []

#Question 4
class InvvTurnoverRatioAction(Action):
    def name(self) -> Text:
        return "action_inventory_turnover_ratio"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        domain = [('sales_count', '>', 0)]
        # Sort the products by sales count (descending)
        fields = ['name', 'standard_price', 'qty_available', 'sales_count']
        limit = 1
        product_ids = models.execute_kw(db, uid, password, 'product.template', 'search', [domain],{'limit':limit})
        products = models.execute_kw(db, uid, password, 'product.template', 'read', [product_ids], {'fields': fields})

        for product in products:
            result = '{}'.format(product['name'])
            # cost = result['standard_price']
            cost = product['standard_price']

            sold = product['sales_count']

            tot_cost = ((cost*sold)*2)

            qty_aval = product['qty_available']

            highest_turnover = tot_cost / qty_aval
            # print("The inventory turnover ratio for our highest selling product this year is", highest_turnover)
        response = f"The inventory turnover ratio for our highest selling product this year is {highest_turnover:.2f}" 
        dispatcher.utter_message(response)

        return []

#Question 5
class AvgLeadTimeAction(Action):
    def name(self) -> Text:
        return "action_inventory_average_lead_time_for_receiving_goods_from_suppliers_this_quarter"

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
        quarter_start = datetime.date(today.year, (today.month - 1) // 3 * 3 + 1, 1)
        quarter_end = datetime.date(today.year, (today.month - 1) // 3 * 3 + 3, 1) + datetime.timedelta(days=30)

        # Search for all incoming shipment in the date range
        domain = [('picking_type_code', '=', 'incoming'), ('state', '=', 'done'), ('scheduled_date', '>=', quarter_start.strftime('%Y-%m-%d 00:00:00')), ('scheduled_date', '<=', quarter_end.strftime('%Y-%m-%d 23:59:59'))]
        incoming_shipments = models.execute_kw(db, uid, password, 'stock.picking', 'search_read', [domain], {'fields': ['create_date', 'date_done']})

        # Calculate the average lead time
        total_lead_time = 0
        num_shipments = 0
        for shipment in incoming_shipments:
            if shipment['create_date'] and shipment['date_done']:
                lead_time = (datetime.datetime.strptime(shipment['date_done'], '%Y-%m-%d %H:%M:%S') - datetime.datetime.strptime(shipment['create_date'], '%Y-%m-%d %H:%M:%S')).days
                total_lead_time += lead_time
                num_shipments += 1

        avg_lead_time = total_lead_time / num_shipments if num_shipments > 0 else 0

        # Respond with the average lead time
        response = f"The average lead time for receiving goods from suppliers this quarter is {avg_lead_time:.2f} days."
        # print(">>>>>>>>>>>responseQ5",response)
        dispatcher.utter_message(text=response)

        return []

#Question 6
class InTransitAction(Action):
    def name(self) -> Text:
        return "action_inventory_number_of_units_currently_in_transit"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Search for all outgoing shipments that are not done
        domain = [('state', '=', 'assigned')]

        # Retrieve Stock Pickings that meet the domain criteria
        pickings = models.execute_kw(db, uid, password, 'stock.move', 'search_read', [domain], {'fields': ['product_uom_qty']})

        # Sum the quantities of all pickings to get the total number of units in transit
        total_units_in_transit = sum(picking['product_uom_qty'] for picking in pickings)
        # Respond with the total quantity in transit
        response = f"There are currently {total_units_in_transit:.0f} units of products in transit."
        dispatcher.utter_message(text=response)

        return []

# #Question 7
# class HighestReturnRateAction(Action):
#     def name(self) -> Text:
#         return "action_inventory_product_highest_return_rate_this_year"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

#         telegram_id = tracker.sender_id
#         url, db, username, password = jay(telegram_id)

#         # Authenticate and create the XML-RPC client
#         common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
#         uid = common.authenticate(db, username, password, {})
#         models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

#         # Search for all return orders this year
#         year_start = datetime.date(datetime.datetime.now().year, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
#         domain = [('state', '=', 'done'), ('return_order', '=', True), ('date_done', '>=', year_start)]
#         return_orders = models.execute_kw(db, uid, password, 'stock.picking', 'search_read', [domain], {'fields': ['move_lines']})

#         # Count the return quantity for each product
#         return_quantities = {}
#         for order in return_orders:
#             for move in order['move_lines']:
#                 product_id = move['product_id'][0]
#                 if product_id not in return_quantities:
#                     return_quantities[product_id] = move['quantity_done']
#                 else:
#                     return_quantities[product_id] += move['quantity_done']

#         # Find the product with the highest return rate
#         highest_product_id = max(return_quantities, key=return_quantities.get)
#         highest_product = models.execute_kw(db, uid, password, 'product.product', 'read', [[highest_product_id]], {'fields': ['name']})[0]['name']

#         # Calculate the return rate of the highest product
#         total_purchased_quantity = models.execute_kw(db, uid, password, 'stock.move.line', 'search_count', [[('product_id', '=', highest_product_id), ('picking_id.picking_type_code', '=', 'outgoing'), ('state', '=', 'done')]])
#         return_rate = return_quantities[highest_product_id] / total_purchased_quantity

#         # Respond with the product with the highest return rate
#         response = f"The product with the highest return rate this year is {highest_product} with a return rate of {return_rate:.2%}."
#         dispatcher.utter_message(text=response)

#         return []

#Question 8

class AvgFulfillmentTimeAction(Action):
    def name(self) -> Text:
        return "action_inventory_average_time_to_fulfill_customer_orders_this_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Get orders for this month
        model_name = 'stock.picking'
        domain = [('state', '=', 'done'), ('inv_date', '!=', False)]

        order_ids = models.execute_kw(db, uid, password, model_name, 'search', [domain])
        print(order_ids)
        orders = models.execute_kw(db, uid, password, model_name, 'read', [order_ids], {'fields': ['inv_date']})
        print(orders)
        valid_orders = [order for order in orders if order['inv_date']]

        if valid_orders:
            ref_date = datetime.datetime(datetime.datetime.now().year, 1, 1)
            total_days = sum([(datetime.datetime.strptime(order['inv_date'], "%Y-%m-%d") - ref_date).days for order in valid_orders])
            avg_days = total_days / len(valid_orders)
            avg_date = ref_date + datetime.timedelta(days=avg_days)
            response = "Average invoice date for invoiced stock picking records: " + avg_date.strftime("%Y-%m-%d")
        else:
            response = "No invoiced stock picking records found."

        # Send response
        # response = "The average time taken to fulfill customer orders this month is {}.".format(avg_fulfillment_time)
        dispatcher.utter_message(response)

        return []

#Question 9
class HighestInventoryHoldingCostAction(Action):
    def name(self) -> Text:
        return "action_inventory_location_highest_inventory_holding_cost_this_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Get locations

        # Calculate inventory holding cost for each location this quarter
        today = datetime.datetime.today()
        start_of_quarter = datetime.datetime(today.year, (today.month - 1) // 3 * 3 + 1, 1)

        locations = models.execute_kw(db, uid, password, 'stock.location', 'search_read', [[['usage', '=', 'internal']]],
                                    {'fields': ['id', 'name'], 'offset': 0, 'limit': False})
        total_holding_cost = {}
        for location in locations:
            domain = [('location_dest_id', '=', location['id']),
                    ('create_date', '>=', start_of_quarter.strftime('%Y-%m-%d 00:00:00')),
                    ('create_date', '<=', today.strftime('%Y-%m-%d 23:59:59'))]
            moves = models.execute_kw(db, uid, password, 'stock.move', 'search_read',
                                    [domain])
            # print("************",moves)
            holding_cost = sum((move['product_uom_qty'] * move['price_unit']) for move in moves)
            total_holding_cost[location['name']] = holding_cost
            # print(holding_cost)

        # Get location with highest inventory holding cost
        highest_cost_location = max(total_holding_cost, key=total_holding_cost.get)
        # print(highest_cost_location)
        # highest_valuation_id = max(valuation_data, key=valuation_data.get)

        # Send response
        response = "The location with the highest inventory holding cost in this quarter is {}.".format(
            highest_cost_location)
        dispatcher.utter_message(response)

        return []

#Question 10
class TopSellingInventoryAction(Action):
    def name(self) -> Text:
        return "action_inventory_current_inventory_level_top_10_selling_products"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Get top 10 selling products
        domain = [('sales_count', '>', 0)]
        # Sort the products by sales count (descending)
        fields = ['name']
        limit = 10
        product_ids = models.execute_kw(db, uid, password, 'product.template', 'search', [domain],{'limit':limit})
        products = models.execute_kw(db, uid, password, 'product.template', 'read', [product_ids], {'fields': fields})
        response = "The current inventory level for our top 10 selling products are: \n"

        for product in products:
            # print(product)
            response += '{}\n'.format(product['name'])
        
        # Send response
  
        dispatcher.utter_message(response)

        return []

# =================================================//Inventory//==================================================




