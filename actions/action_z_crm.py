from comman import *

# Question 1

class ListLeadsAction(Action):
    def name(self) -> Text:
        return "action_crm_list_leads"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        print(telegram_id)
        url, db, username, password = jay(telegram_id)
        bot = Bot(token=TOKEN)
        chat_id = tracker.sender_id
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Retrieve a list of all the leads
        lead_ids = models.execute_kw(
            db, uid, password, "crm.lead", "search", [[]], {"order": "create_date DESC"}
        )

        leads = []
        for lead_id in lead_ids:
            lead = models.execute_kw(
                db,
                uid,
                password,
                "crm.lead",
                "read",
                [lead_id],
                {"fields": ["name", "phone"]},
            )
            leads.append(lead)

        # Generate a PDF file containing the list of leads
        if leads:
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=landscape(letter))
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(100, 550, f"Here's a list of all the leads we have.")
            pdf.setFont("Helvetica", 12)
            y = 500
            # pdf.drawString(100, 550, f"List of Leads")
            for lead in leads:
                name = lead[0]["name"]
                phone = lead[0]["phone"]
                pdf.drawString(100, y, f"Name: {name}, Phone: {phone}")
                y -= 20
            pdf.showPage()
            pdf.save()

            # Save the PDF file to disk
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            file_name = f"leads_{now}.pdf"
            with open(file_name, "wb") as f:
                f.write(buffer.getbuffer())

            # Send a message indicating that the file has been saved
            message = f"Sure! Here's a list of all the leads we have in our CRM system. Is there anything else I can help you with?"
        # dispatcher.utter_message(attachment=file_name)
        dispatcher.utter_message(text=message)
        # try:
        try:
            with open(file_name, "rb") as f:
                bot.send_document(chat_id=telegram_id, document=f, filename=file_name)
            os.remove(file_name)
        except Exception as e:
            dispatcher.utter_message(attachment=file_name)
        return []

# Question 2

class UnfollowedLeadsAction(Action):
    def name(self) -> Text:
        return "action_crm_unfollowed_leads"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Calculate the date one week ago
        one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
        one_week_ago_str = one_week_ago.strftime("%Y-%m-%d %H:%M:%S")

        # Retrieve a list of all the leads that have not been followed up with in the last week
        lead_ids = models.execute_kw(
            db,
            uid,
            password,
            "crm.lead",
            "search",
            [[["activity_ids.date_deadline", "<", one_week_ago_str]]],
        )

        leads = []
        for lead_id in lead_ids:
            lead = models.execute_kw(
                db,
                uid,
                password,
                "crm.lead",
                "read",
                [lead_id],
                {"fields": ["name", "phone"]},
            )
            leads.append(lead)

        # Send the list of unfollowed leads to the user
        if leads:
            message = "Here's a list of all the leads that have not been followed up with in the last week:\n"
            for lead in leads:
                message += f"- Name: {lead['name']}, Phone: {lead['phone']}, \n"
        else:
            message = "There are no unfollowed leads in the CRM system."
        dispatcher.utter_message(text=message)

        return []

# Question 3 | INC

class SalesOpportunitiesAction(Action):
    def name(self) -> Text:
        return "action_crm_sales_opportunities_summary"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        bot = Bot(token=TOKEN)
        chat_id = tracker.sender_id

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Retrieve sales opportunities from pipeline
        opportunities = models.execute_kw(
            db,
            uid,
            password,
            "crm.lead",
            "search_read",
            [[["type", "=", "opportunity"], ["stage_id", "!=", False]]],
            {"fields": ["name", "expected_revenue", "probability", "stage_id"]},
        )

        # Generate a PDF file containing the summary of sales opportunities
        if opportunities:
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=landscape(letter))
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(100, 550, "Summary of Sales Opportunities")
            pdf.setFont("Helvetica", 12)
            y = 500
            for opp in opportunities:
                name = opp["name"]
                stage = opp["stage_id"][1]
                prob = opp["probability"]
                revenue = opp["expected_revenue"]
                pdf.drawString(100, y, f"Name: {name}")
                pdf.drawString(400, y, f"Stage: {stage}")
                pdf.drawString(100, y - 20, f"Probability: {prob}%")
                pdf.drawString(400, y - 20, f"Expected Revenue: ${revenue}")
                y -= 40
            pdf.showPage()
            pdf.save()

            # Save the PDF file to disk
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            file_name = f"sales_opportunities_{now}.pdf"
            with open(file_name, "wb") as f:
                f.write(buffer.getbuffer())

            # Send a message indicating that the file has been saved
            message = "Here's a summary of the sales opportunities in the pipeline."
            dispatcher.utter_message(text=message)
            
            try:
                with open(file_name, "rb") as f:
                    bot.send_document(chat_id=telegram_id, document=f, filename=file_name)
                os.remove(file_name)
            except Exception as e:
                dispatcher.utter_message(attachment=file_name)
        else:
            dispatcher.utter_message(
                text="There are no sales opportunities in the pipeline at the moment."
            )

        return []

# Question 4
class OpportunityStatusAction(Action):
    def name(self) -> Text:
        return "action_crm_opportunity_status"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        customer_name = tracker.get_slot("cname")
        print(customer_name)
        if not customer_name:
            dispatcher.utter_message(
                text="I'm sorry, I didn't catch the customer name."
            )
            return []

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Search for the opportunity for the given customer
        opportunity_ids = models.execute_kw(
            db,
            uid,
            password,
            "crm.lead",
            "search",
            [[["type", "=", "opportunity"], ["partner_name", "=ilike", customer_name]]],
        )

        if not opportunity_ids:
            message = (
                f"I'm sorry, I couldn't find any opportunities for {customer_name}."
            )
        elif len(opportunity_ids) > 1:
            message = f"I found {len(opportunity_ids)} opportunities for {customer_name}. Please be more specific."
        else:
            opportunity = models.execute_kw(
                db,
                uid,
                password,
                "crm.lead",
                "read",
                [opportunity_ids[0]],
                {"fields": ["name", "stage_id"]},
            )

            stage = models.execute_kw(
                db,
                uid,
                password,
                "crm.stage",
                "read",
                [opportunity["stage_id"][0]],
                {"fields": ["name"]},
            )["name"]

            message = f"The status of the opportunity '{opportunity['name']}' for {customer_name} is '{stage}'."

        dispatcher.utter_message(text=message)

        return []

# Question 5

class DealsReportAction(Action):
    def name(self) -> Text:
        return "action_crm_deals_report"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Get the current date and the date from one month ago
        today = datetime.datetime.today()
        one_month_ago = today - timedelta(days=30)

        # Search for deals won or lost in the last month
        domain = [
            ("create_date", ">", one_month_ago.strftime("%Y-%m-%d")),
            ("type", "=", "opportunity"),
        ]
        fields = ["name", "partner_id", "stage_id", "probability"]
        deals = models.execute_kw(
            db, uid, password, "crm.lead", "search_read", [domain], {"fields": fields}
        )
        print(deals)
        # Filter the deals to only those that were won or lost
        won_or_lost_deals = [
            deal for deal in deals if deal["stage_id"][1] in ("Won", "Lost")
        ]
        print(won_or_lost_deals)
        # Send a message with the list of deals
        if won_or_lost_deals:
            message = "Here are the deals that were won or lost in the last month:\n"

            for deal in won_or_lost_deals:
                message += (
                    f"{deal['name']} ({deal['stage_id'][1]},  {deal['probability']})\n"
                )
        else:
            message = "There were no deals won or lost in the last month."
        dispatcher.utter_message(text=message)

        return []

# Question 6

class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_count_entries_action"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Get the sales orders waiting to be invoiced and sum their amounts
        domain = [("state", "=", "sale"), ("invoice_status", "=", "to invoice")]
        fields = ["amount_total"]
        orders = models.execute_kw(
            db, uid, password, "sale.order", "search_read", [domain], {"fields": fields}
        )
        total_amount = sum([order["amount_total"] for order in orders])

        # Send the value to the user
        message = f"The current value of sales orders waiting to be invoiced is {total_amount}"
        dispatcher.utter_message(text=message)

        return []

# Question 7

class UncontactedCustomersLastMonthAction(Action):
    def name(self) -> Text:
        return "action_crm_uncontacted_customers_last_month"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        bot = Bot(token=TOKEN)
        chat_id = tracker.sender_id

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Calculate the date one month ago from today
        one_month_ago = (
            datetime.datetime.now() - datetime.timedelta(days=30)
        ).strftime("%Y-%m-%d %H:%M:%S")

        # Search for customers that have not been contacted in the last month
        domain = [("write_date", "<", one_month_ago)]
        fields = ["name", "phone"]
        customers = models.execute_kw(
            db,
            uid,
            password,
            "res.partner",
            "search_read",
            [domain],
            {"fields": fields},
        )

        # Generate a PDF file containing the list of uncontacted customers
        if customers:
            buffer = io.BytesIO()
            pdf = canvas.Canvas(buffer, pagesize=landscape(letter))
            pdf.setFont("Helvetica-Bold", 14)
            pdf.drawString(100, 550, "Uncontacted Customers Last Month")
            pdf.setFont("Helvetica", 12)
            y = 500
            for customer in customers:
                name = customer["name"]
                phone = customer["phone"]
                pdf.drawString(100, y, f"Name: {name}")
                pdf.drawString(400, y, f"Phone: {phone}")
                y -= 40
            pdf.showPage()
            pdf.save()

            # Save the PDF file to disk
            now = datetime.datetime.now().strftime("%Y-%m-%d_%H:%M:%S")
            file_name = f"uncontacted_customers_{now}.pdf"
            with open(file_name, "wb") as f:
                f.write(buffer.getbuffer())

            # Send a message indicating that the file has been saved
            message = "Here is the list of uncontacted customers last month."
            dispatcher.utter_message(text=message)
            # await bot.send_document(chat_id=chat_id, document=file_name)
            try:
                with open(file_name, "rb") as f:
                    bot.send_document(chat_id=telegram_id, document=f, filename=file_name)
                os.remove(file_name)
            except Exception as e:
                dispatcher.utter_message(attachment=file_name)
            # os.remove(file_name)
        else:
            dispatcher.utter_message(
                text="There are no customers that have not been contacted in the last month."
            )

        return []

# Question 8
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_top_customers_by_revenue_current_year"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Get the top 10 customers by revenue for the current year
        current_year = datetime.datetime.now().year
        domain = [
            ("move_type", "=", "out_invoice"),
            ("state", "in", ["posted"]),
            ("invoice_date", ">=", f"{current_year}-01-01"),
        ]
        fields = ["partner_id", "amount_total"]
        invoices = models.execute_kw(
            db,
            uid,
            password,
            "account.move",
            "search_read",
            [domain],
            {"fields": fields},
        )
        print("invoices", invoices)
        # Aggregate the revenue by customer and sort by descending revenue
        revenue_by_customer = {}
        for invoice in invoices:
            partner_id = invoice["partner_id"][0]
            amount_total = invoice["amount_total"]
            if partner_id not in revenue_by_customer:
                revenue_by_customer[partner_id] = 0
            revenue_by_customer[partner_id] += amount_total
        sorted_revenue = sorted(
            revenue_by_customer.items(), key=lambda x: x[1], reverse=True
        )[:10]

        # Get the names of the top 10 customers and add them to a message
        message = "The top 10 customers by revenue for the current year are:\n"
        for customer_id, revenue in sorted_revenue:
            customer = models.execute_kw(
                db,
                uid,
                password,
                "res.partner",
                "read",
                [customer_id],
                {"fields": ["name"]},
            )
            customer_name = customer[0]["name"]
            message += f"{customer_name}: {revenue}\n"

        dispatcher.utter_message(text=message)

        return []

# Question 9
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_average_time_salesteam"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Get the opportunities that have been won
        domain = [("type", "=", "opportunity"), ("stage_id", "=", 4)]
        fields = ["user_id", "create_date", "date_closed"]
        opportunities = models.execute_kw(
            db, uid, password, "crm.lead", "search_read", [domain], {"fields": fields}
        )

        # Calculate the average time it takes for the sales team to close a deal
        total_time = 0
        num_opportunities = 0
        for opportunity in opportunities:
            create_date = datetime.datetime.strptime(
                opportunity["create_date"], "%Y-%m-%d %H:%M:%S"
            )
            date_closed = datetime.datetime.strptime(
                opportunity["date_closed"], "%Y-%m-%d %H:%M:%S"
            )
            time_to_close = date_closed - create_date
            total_time += time_to_close.days
            num_opportunities += 1

        if num_opportunities == 0:
            average_time_to_close = 0
        else:
            average_time_to_close = total_time / num_opportunities

        message = "The average time it takes for our sales team to close a deal is {:.2f} days.".format(
            average_time_to_close
        )

        dispatcher.utter_message(text=message)

        return []

# Question 10
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_salesperson_highest_win_rate"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

        # Get the salesperson with the highest win rate
        domain = [
            ("type", "=", "opportunity"),
            ("probability", ">", 0),
            ("user_id", "!=", False),
        ]
        fields = ["user_id", "stage_id"]
        opportunities = models.execute_kw(
            db, uid, password, "crm.lead", "search_read", [domain], {"fields": fields}
        )

        # Aggregate the number of opportunities and wins by salesperson
        num_opportunities_by_salesperson = {}
        num_wins_by_salesperson = {}
        for opportunity in opportunities:
            user_id = opportunity["user_id"][0]
            stage_id = opportunity["stage_id"][0]
            if user_id not in num_opportunities_by_salesperson:
                num_opportunities_by_salesperson[user_id] = 0
            num_opportunities_by_salesperson[user_id] += 1
            if stage_id == 4:  # 4 is the ID of the 'Won' stage
                if user_id not in num_wins_by_salesperson:
                    num_wins_by_salesperson[user_id] = 0
                num_wins_by_salesperson[user_id] += 1

        # Calculate the win rate for each salesperson
        win_rates = {}
        for salesperson_id in num_opportunities_by_salesperson.keys():
            if salesperson_id not in num_wins_by_salesperson:
                win_rate = 0
            else:
                win_rate = (
                    num_wins_by_salesperson[salesperson_id]
                    / num_opportunities_by_salesperson[salesperson_id]
                )
            win_rates[salesperson_id] = win_rate

        # Find the salesperson with the highest win rate
        highest_win_rate_salesperson_id = max(win_rates, key=win_rates.get)
        highest_win_rate_salesperson = models.execute_kw(
            db,
            uid,
            password,
            "res.users",
            "read",
            [highest_win_rate_salesperson_id],
            {"fields": ["name"]},
        )[0]["name"]

        message = f"The salesperson with the highest win rate is {highest_win_rate_salesperson}."

        dispatcher.utter_message(text=message)

        return []

# Question 11 Sales person wise number of sales done

class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_salesperson_number_sales_done"

    async def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        # HOST, DB, USER, PASS = jay(telegram_id)
        HOST = '192.168.0.145'
        PORT = 3333
        DB = 'mar6_rapid_bevtech'
        USER = 'admin'
        PASS = 'admin'
        
        url = "http://%s:%s/jsonrpc" % (HOST, PORT)
        uid = call(url, "common", "login", DB, USER, PASS)

        args = [('type', '=', 'opportunity'), ('stage_id', '=', 4)]
        fields = ['user_id']
        opportunities = call(url, "object", "execute", DB, uid, PASS, 'crm.lead', 'search_read', args, fields)
        sales_counts = {}
        for opportunity in opportunities:
            salesperson_id = opportunity['user_id'][0]
            if salesperson_id in sales_counts:
                sales_counts[salesperson_id] += 1
            else:
                sales_counts[salesperson_id] = 1
    
        # Create a bar chart
        salespeople = []
        counts = []
        for salesperson_id, count in sales_counts.items():
            fields_two = ['name']
            salesperson = call(url, "object", "execute", DB, uid, PASS, 'res.users', 'read', salesperson_id, fields_two)
            salespeople.append(salesperson[0]['name'])
            counts.append(count)

        fig = plt.figure(figsize=(10, 5))
        plt.bar(salespeople, counts)
        plt.xlabel("Salesperson")
        plt.ylabel("Number of Sales")
        plt.title("Sales by Salesperson")
        plt.savefig("sales_chart.png")  # Save the chart as an image
        bot = Bot(token=TOKEN)
        file_name = "sales_chart.png"
        # await bot.send_photo(chat_id=telegram_id, photo="sales_chart.png")
        # os.remove("sales_chart.png")
        # message="hey i am from the odoo"
        plt.clf()
        try:
            with open(file_name, "rb") as f:
                bot.send_photo(chat_id=telegram_id, photo=f, filename=file_name)
            os.remove(file_name)
        except Exception as e:
            dispatcher.utter_message(attachment=file_name)
        return []
    
# Question 12 Which products are selling the most done
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_products_selling_most"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        products = models.execute_kw(db, uid, password,
                             'product.product', 'search_read',
                             [[['type', '=', 'product']]], {'fields': ['name', 'qty_available']})

        # Calculate the total sales quantity across all products
        total_sales = sum([p['qty_available'] for p in products])

        # Calculate the percentage of sales for each product
        product_sales = [{'name': p['name'], 'sales_percentage': (p['qty_available'] / total_sales) * 100} for p in products]

        # Sort the products by their sales percentage in descending order
        product_sales = sorted(product_sales, key=lambda p: p['sales_percentage'], reverse=True)

        # Display the top 10 products by sales percen   tage as a pie chart
        top_products = product_sales[:5]
        print(top_products)
        data = [{'x': p['name'], 'y': p['sales_percentage']} for p in top_products]
        labels = [p['name'] for p in top_products]
        chart_title = "Top 5 products by sales percentage"
        plt.pie([p['sales_percentage'] for p in top_products], labels=labels)
        plt.title(chart_title)

        # Display the chart on the screen

        # Save the chart to disk
        file_name = 'top_products_pie_chart.png'
        plt.savefig(file_name)
        bot = Bot(token=TOKEN)
        # await bot.send_photo(chat_id=telegram_id, photo="sales_chart.png")
        # os.remove("sales_chart.png")
        plt.clf()
        try:
            with open(file_name, "rb") as f:
                bot.send_photo(chat_id=telegram_id, photo=f, filename=file_name)
            os.remove(file_name)
        except Exception as e:
            dispatcher.utter_message(attachment=file_name)
        return []
    
# Question 13 Can you provide the total revenue generated for each quarter of this year ? 
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_revenue_quarter_this_year"

    async def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        # Authenticate and create the XML-RPC client
                                                                                                            
        # Authenticate and create the XML-RPC client                                                            
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))                                    
        uid = common.authenticate(db, username, password, {})                                                   
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))                                    
                                                                                                                
        # Define the start and end dates for each quarter                                                       
        now = datetime.datetime.now()                                                                           
        today = datetime.date.today()                                                                           
        quarters = [(datetime.date(now.year, (i - 1) // 3 * 3 + 1, 1),                                          
                    datetime.date(now.year, (i - 1) // 3 * 3 + 4, 1) - pd.offsets.Day(1))                      
                    for i in range(1, 5)]                                                                       
                                                                                                                
        # Retrieve the total revenue for each quarter                                                           
        quarters_revenue = []                                                                                   
        for start_date, end_date in quarters:                                                                   
            orders = models.execute_kw(db, uid, password, 'sale.order', 'search_read',                          
                                    [[('date_order', '>=', start_date.strftime('%Y-%m-%d')),                 
                                        ('date_order', '<=', end_date.strftime('%Y-%m-%d'))]],                 
                                    {'fields': ['amount_total']})                                            
            total_revenue = sum([order['amount_total'] for order in orders])                                    
            quarters_revenue.append(total_revenue)                                                              
                                                                                                                
        # Create a dataframe with the revenue data for each quarter                                             
        df = pd.DataFrame({'Quarter': ['Q1', 'Q2', 'Q3', 'Q4'], 'Revenue': quarters_revenue})                   
                                                                                                                
        # Create a line chart of the revenue data                                                               
        fig = px.line(df, x='Quarter', y='Revenue')                                                             
        fig.update_layout(title='Total Revenue by Quarter', xaxis_title='Quarter', yaxis_title='Revenue')       
        pio.write_image(fig, 'revenue_chart.png')                                                               
                                                                                                                                                                             
        file_name = 'revenue_chart.png'
        bot = Bot(token=TOKEN)
        # print("jayin",telegram_id)
        # await bot.send_photo(chat_id=telegram_id, photo=file_name)
        # os.remove("sales_chart.png")
        try:
            with open(file_name, "rb") as f:
                bot.send_photo(chat_id=telegram_id, photo=f, filename=file_name)
            os.remove(file_name)
        except Exception as e:
            dispatcher.utter_message(attachment=file_name)
        return []
    
# =================================================//CRM//==================================================









