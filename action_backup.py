# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []
from rasa_sdk.events import SlotSet
from rasa_sdk import Action, Tracker
import requests
from typing import Any, Text, Dict, List
from rasa_sdk.events import UserUtteranceReverted
from typing import Any, Text, Dict, List, Union
from xmlrpc.client import ServerProxy
import xmlrpc.client
from rasa_sdk.executor import CollectingDispatcher
import datetime
import psycopg2
import calendar
from datetime import timedelta
from typing import Any, Dict, List, Text
from dateutil.relativedelta import relativedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from telegram import Bot


def jay(sender_id):

    # Set up the PostgreSQL connection
    # conn = psycopg2.connect(
    #     host="127.0.0.1", port="5432", user="postgres", password="Password123"
    # )
    # cur = conn.cursor()

    # # Get the sender_id from the tracker
    # sender_id = str(sender_id)

    # # Query the user table to find the company associated with the sender_id
    # cur.execute("SELECT c_id FROM usernew WHERE sender_id = %s", (sender_id,))
    # result = cur.fetchone()

    # # Close the database connection
    # cur.close()
    # conn.close()

    # # Set the url, db, username, and password variables based on the company associated with the sender_id
    # if result[0] == 1:
    #     url = 'http://192.168.0.145:3333/'
    #     db = 'mar6_rapid_bevtech'
    #     username = 'admin'
    #     password = 'admin'
    # elif result[0] == 2:
    #     url = 'http://localhost:8069'
    #     db = 'dd'
    #     username = 'admin'
    #     password = 'admin'
    # elif result[0] == 3:
    #     url = 'http://192.168.0.63:8080'
    #     db = 'db_drc_20_01'
    #     username = 'admin'
    #     password = 'admin'
    # else :
    #     url = 'http://localhost:8069'
    #     db = 'dd'
    #     username = 'admin'
    #     password = 'admin'
    # Return the url, db, username, and password variables as a tuple
    url = "http://192.168.0.145:3333/"
    db = "mar6_rapid_bevtech"
    username = "admin"
    password = "admin"

    return (url, db, username, password)


# =================================================CRM=====================================================
# from datetime import datetime

# Question 1
from reportlab.lib.pagesizes import letter
import xmlrpc.client
from typing import Any, Text, Dict, List
from typing import Any, Text, Dict, List
from rasa_sdk.events import SlotSet
import io
import os
import urllib.request
from typing import Any, Text, Dict, List, Union
from typing import Any, Text, Dict, List
from typing import Final


TOKEN: Final = "6067470352:AAGitaW0GZR4-pJAytTZrr48irNO71d72gM"
BOT_USERNAME: Final = "@jaykin_bot"

from deep_translator import GoogleTranslator
from langdetect import detect


# =========================================================================================================
# def detect_and_translate(message, target_language="ar"):
#     detected_language = detect(message)
#     if detected_language != target_language:
#         message = GoogleTranslator(source="auto", target="ar").translate(message)
#     return message


# def detect_translate(message, target_language="en"):
#     detected_language = detect(message)
#     if detected_language != target_language:
#         message = GoogleTranslator(source="auto", target="en").translate(message)
#     return message


# =========================================================================================================


# class ListLeadsAction(Action):
#     def name(self) -> Text:
#         return "action_crm_list_leadsj"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         telegram_id = tracker.sender_id
#         url, db, username, password = jay(telegram_id)

#         # Authenticate and create the XML-RPC client
#         common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
#         uid = common.authenticate(db, username, password, {})
#         models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

#         # Retrieve a list of all the leads
#         lead_ids = models.execute_kw(
#             db, uid, password, "crm.lead", "search", [[]], {"order": "create_date DESC"}
#         )

#         leads = []
#         for lead_id in lead_ids:
#             lead = models.execute_kw(
#                 db,
#                 uid,
#                 password,
#                 "crm.lead",
#                 "read",
#                 [lead_id],
#                 {"fields": ["name", "phone"]},
#             )
#             leads.append(lead)

#         # Send the list of leads to the user
#         if leads:
#             message = "Here's a list of all the leads we have:\n"
#             for lead in leads:
#                 message = f"- Name: {lead[0]['name']}, Phone: {lead[0]['phone']}\n"
#                 dispatcher.utter_message(text=message)
#         else:
#             message = "There are no leads in the CRM system."
#             dispatcher.utter_message(text=message)
#         dispatcher.utter_message(text=telegram_id)

#         return []


# class ActionStartCommand(Action):
#     def name(self) -> Text:
#         return "action_crm_list_leadss"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         from telegram import Bot

#         bot = Bot(token=TOKEN)
#         chat_idd = tracker.sender_id
#         await bot.send_photo(chat_id=chat_idd, photo="inventory_value.png")

#         dispatcher.utter_message(image="inventory_value.png")


# class ActionStartCommand(Action):
#     def name(self) -> Text:
#         return "action_crm_list_leads"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         bot = Bot(token=TOKEN)
#         chat_id = tracker.sender_id
#         print(chat_id)
#         pdf_file = open("leads.pdf", "rb")
#         await bot.send_document(chat_id=chat_id, document=pdf_file)
#         dispatcher.utter_message(text="Here's the PDF file.")
#         dispatcher.utter_message(text=chat_id)
#         return []


# from telegram import Bot
# import io
# import xmlrpc.client
# from reportlab.lib.pagesizes import letter, landscape
# from reportlab.pdfgen import canvas
# from typing import Dict, Text, Any, List
# from rasa_sdk import Action
# from rasa_sdk.events import SlotSet


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
            message = f"Here's a list of all the leads we have."
        # dispatcher.utter_message(attachment=file_name)
        dispatcher.utter_message(text=message)
        await bot.send_document(chat_id=chat_id, document=file_name)
        os.remove(file_name)
        return []


# Question 2


# class UnfollowedLeadsAction(Action):
#     def name(self) -> Text:
#         return "action_crm_unfollowed_leads"

#     def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:

#         telegram_id = tracker.sender_id
#         url, db, username, password = jay(telegram_id)

#         # Authenticate and create the XML-RPC client
#         common = xmlrpc.client.ServerProxy("{}/xmlrpc/2/common".format(url))
#         uid = common.authenticate(db, username, password, {})
#         models = xmlrpc.client.ServerProxy("{}/xmlrpc/2/object".format(url))

#         # Calculate the date one week ago
#         one_week_ago = datetime.datetime.now() - datetime.timedelta(days=7)
#         one_week_ago_str = one_week_ago.strftime("%Y-%m-%d %H:%M:%S")

#         # Retrieve a list of all the leads that have not been followed up with in the last week
#         lead_ids = models.execute_kw(
#             db,
#             uid,
#             password,
#             "crm.lead",
#             "search",
#             [[["activity_ids.date_deadline", "<", one_week_ago_str]]],
#         )

#         leads = []
#         for lead_id in lead_ids:
#             lead = models.execute_kw(
#                 db,
#                 uid,
#                 password,
#                 "crm.lead",
#                 "read",
#                 [lead_id],
#                 {"fields": ["name", "phone"]},
#             )
#             leads.append(lead)

#         # Send the list of unfollowed leads to the user
#         if leads:
#             message = "Here's a list of all the leads that have not been followed up with in the last week:\n"
#             for lead in leads:
#                 message += f"- Name: {lead['name']}, Phone: {lead['phone']}, \n"
#         else:
#             message = "There are no unfollowed leads in the CRM system."
#         dispatcher.utter_message(text=message)

#         return []

class LeadsNotFollowedUpAction(Action):
    def name(self) -> Text:
        return "action_crm_unfollowed_leads"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the timeframe entity from the user's message
        timeframe = tracker.get_slot("timeframe")

        # Calculate the date range based on the timeframe
        if timeframe == "week":
            start_date = datetime.date.today() - datetime.timedelta(days=7)
            end_date = datetime.date.today()
        elif timeframe == "month":
            start_date = datetime.date.today() - datetime.timedelta(days=30)
            end_date = datetime.date.today()
        elif timeframe == "year":
            start_date = datetime.date.today() - datetime.timedelta(days=365)
            end_date = datetime.date.today()
        elif timeframe == "5 years":
            start_date = datetime.date.today() - datetime.timedelta(days=5*365)
            end_date = datetime.date.today()
        else:
            dispatcher.utter_message("Sorry, I didn't understand the timeframe you specified.")
            return []

        # Use the XML-RPC client to query the leads module in Odoo
        # and retrieve the leads that haven't been followed up with
        # within the specified timeframe
        url, db, username, password = jay(tracker.sender_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        lead_ids = models.execute_kw(db, uid, password, 'crm.lead', 'search',
            [[['type', '=', 'lead'], ['date_deadline', '<', end_date.strftime('%Y-%m-%d')],
            ['date_deadline', '>=', start_date.strftime('%Y-%m-%d')]]])
        leads = models.execute_kw(db, uid, password, 'crm.lead', 'read',
            [lead_ids], {'fields': ['name', 'email', 'phone']})

        # Send the list of leads to the user
        message = "Here are the leads that haven't been followed up with in the last {}: ".format(timeframe)
        for lead in leads:
            message += "\nName: {}, Email: {}, Phone: {}".format(lead['name'], lead['email'], lead['phone'])
        dispatcher.utter_message(message)

        return []


# Question for chart
# class ActionStartCommand(Action):
#     def name(self) -> Text:
#         return "action_crm_list_leadss"

#     async def run(
#         self,
#         dispatcher: CollectingDispatcher,
#         tracker: Tracker,
#         domain: Dict[Text, Any],
#     ) -> List[Dict[Text, Any]]:
#         from telegram import Bot

#         bot = Bot(token=TOKEN)
#         chat_idd = tracker.sender_id
#         await bot.send_photo(chat_id=chat_idd, photo="inventory_value.png")

#         dispatcher.utter_message(image="inventory_value.png")


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
            await bot.send_document(chat_id=chat_id, document=file_name)
            os.remove(file_name)
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



# =================================================//CRM//==================================================

# =================================================sales==================================================

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

import calendar
import datetime
import json
import random
import urllib.request

import requests

class SearchSaleOrders(Action):
    def name(self) -> Text:
        return "action_sale_number_orders_month"

    def run(
        self,
        dispatcher: CollectingDispatcher,
        tracker: Tracker,
        domain: Dict[Text, Any],
    ) -> List[Dict[Text, Any]]:
        # Add the code you want to execute in this function
        HOST = '192.168.0.145'
        PORT = 3333
        DB = 'mar6_rapid_bevtech'
        USER = 'admin'
        PASS = 'admin'

        def json_rpc(url, method, params):
            data = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": random.randint(0, 1000000000)
            }

            req = urllib.request.Request(url=url, data=json.dumps(data).encode(), headers={
                "Content-Type": "application/json",
            })
            reply = json.loads(urllib.request.urlopen(req).read().decode('UTF-8'))
            if reply.get("error"):
                raise Exception(reply["error"])
            return reply["result"]


        def call(url, service, method, *args):
            return json_rpc(url, "call", {"service": service, "method": method, "args": args})


        url = f"http://{HOST}:{PORT}/jsonrpc"
        uid = call(url, "common", "login", DB, USER, PASS)

        today = datetime.datetime.now()
        month_start = datetime.datetime(today.year, today.month, 1)
        month_end = datetime.datetime(today.year, today.month, calendar.monthrange(today.year, today.month)[1])

        args = [('state', '=', 'sale'),
                ('date_order', '>=', month_start.strftime('%Y-%m-%d')),
                ('date_order', '<=', month_end.strftime('%Y-%m-%d'))]

        note_id = call(url, "object", "execute", DB, uid, PASS, 'sale.order', 'search_count', args)
        # total_revenue = sum([order['amount_total'] for order in note_id])
        response = f"Searching records{note_id}"
            # response = f"Total revenue for the current month is {total_revenue}."
        dispatcher.utter_message(response)

        return []


class TotalOrdersThisMonthAction(Action):
    def name(self) -> Text:
        return "action_sale_number_orders_monthhh"

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
from typing import Any, Dict, List, Text
from datetime import date
from dateutil import relativedelta
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

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
        start_date = date.today().replace(day=1)
        end_date = start_date + relativedelta.relativedelta(months=3) - relativedelta.relativedelta(days=1)
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
# import xmlrpc.client
# from typing import Text, List, Dict, Any
# from rasa_sdk import Action, Tracker
# import datetime

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

# =================================================Purchase======================================================

#Question 1
from dateutil import relativedelta
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
        quarter_start = (today - relativedelta.relativedelta(months=3)).replace(day=1)
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

from collections import defaultdict

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

#Question 7
class HighestReturnRateAction(Action):
    def name(self) -> Text:
        return "action_inventory_product_highest_return_rate_this_year"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Search for all return orders this year
        year_start = datetime.date(datetime.datetime.now().year, 1, 1).strftime('%Y-%m-%d %H:%M:%S')
        domain = [('state', '=', 'done'), ('return_order', '=', True), ('date_done', '>=', year_start)]
        return_orders = models.execute_kw(db, uid, password, 'stock.picking', 'search_read', [domain], {'fields': ['move_lines']})

        # Count the return quantity for each product
        return_quantities = {}
        for order in return_orders:
            for move in order['move_lines']:
                product_id = move['product_id'][0]
                if product_id not in return_quantities:
                    return_quantities[product_id] = move['quantity_done']
                else:
                    return_quantities[product_id] += move['quantity_done']

        # Find the product with the highest return rate
        highest_product_id = max(return_quantities, key=return_quantities.get)
        highest_product = models.execute_kw(db, uid, password, 'product.product', 'read', [[highest_product_id]], {'fields': ['name']})[0]['name']

        # Calculate the return rate of the highest product
        total_purchased_quantity = models.execute_kw(db, uid, password, 'stock.move.line', 'search_count', [[('product_id', '=', highest_product_id), ('picking_id.picking_type_code', '=', 'outgoing'), ('state', '=', 'done')]])
        return_rate = return_quantities[highest_product_id] / total_purchased_quantity

        # Respond with the product with the highest return rate
        response = f"The product with the highest return rate this year is {highest_product} with a return rate of {return_rate:.2%}."
        dispatcher.utter_message(text=response)

        return []

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

        import datetime

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

# =================================================Account + invoice ==================================================

#Question 1

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


#Question 2

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
    
#Question 3

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
    
#Question 4

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
    
#Question 5

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
    
#Question 7

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

# class TopSellingInventoryAction(Action):
#     def name(self) -> Text:
#         return "action_ai_most_common_payment_method_used_by_customers_this_year"

#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
      
#         telegram_id = tracker.sender_id
#         url, db, username, password = jay(telegram_id)

#         # Authenticate and create the XML-RPC client
#         common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
#         uid = common.authenticate(db, username, password, {})
#         models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
#         current_year =str(datetime.datetime.now().year)
#         domain = [('journal_id', '!=', False),('date', '>=',current_year+'-01-01'), ('date', '<=',current_year+'-12-31')]
#         fields = ['journal_id']
#         payments = models.execute_kw(db, uid, password, 'account.payment', 'search_read', [domain], {'fields': fields})

#         payment_counts = {}
#         for payment in payments:
#             journal_id = payment['journal_id'][1]
#             if journal_id in payment_counts:
#                 payment_counts[journal_id] += 1
#             else:
#                 payment_counts[journal_id] = 1

#         most_common_payment = max(payment_counts, key=payment_counts.get)
#         response = 'The payment method that is most commonly used by customers is: {}'.format(most_common_payment)
#         dispatcher.utter_message(response)

#         return []
import datetime

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
        # Define the current year, month, and quarter
        current_year = str(datetime.datetime.now().year)
        current_month = str(datetime.datetime.now().month)
        current_quarter = str((datetime.datetime.now().month - 1) // 3 + 1)

        # Get the time period from the user input
        time_period = tracker.get_slot("time_period")
        print(time_period)


        if time_period == "year":
            domain = [('journal_id', '!=', False),('date', '>=',current_year+'-01-01'), ('date', '<=',current_year+'-12-31')]
        elif time_period == "month":
            domain = [('journal_id', '!=', False),('date', '>=',current_year+'-'+current_month+'-01'), ('date', '<=',current_year+'-'+current_month+'-31')]
        elif time_period == "quarter":
            domain = [('journal_id', '!=', False),('date', '>=',current_year+'-'+current_quarter+'-01'), ('date', '<=',current_year+'-'+current_quarter+'-31')]
        elif time_period == "week":
            current_week = str(datetime.datetime.now().isocalendar()[1])
            domain = [('journal_id', '!=', False),('date', '>=',current_year+'-W'+current_week+'-1'), ('date', '<=',current_year+'-W'+current_week+'-7')]
        else:
            # Default time period is this year
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
        response = 'The payment method that is most commonly used by customers {} is: {}'.format(time_period, most_common_payment)
        dispatcher.utter_message(response)

        return []


# =================================================//Account + invoice //==================================================

# Ouestion 1 | done
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "act_quatation_num"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # url = 'http://192.168.0.145:3333/'
        # db = 'mar6_rapid_bevtech'
        # username = 'admin'
        # password = 'admin'
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)

        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        table_name = 'crm.lead'
        # Select data from the table 'sale.order'
        record_count = models.execute_kw(db, uid, password, table_name, 'search_count', [[]])

        # Logout of the XMLRPC session
        # server.common.logout(session_id)

        # Print the record count
        message = (f"There are {record_count} Open Quotations.")
        
        dispatcher.utter_message(text=message)

        return []

# Ouestion 2 | done
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_value_quotation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # Set the necessary variables
        model_name = 'crm.lead'
        field_name = 'expected_revenue'
        domain = []
        
        # Execute the search_read method with the search_count parameter to get the total count
        record_count = models.execute_kw(
            db, 
            uid, 
            password, 
            model_name, 
            'search_count', 
            [domain]
        )
        
        # Execute the search_read method with the fields parameter to get the field values
        records = models.execute_kw(
            db, 
            uid, 
            password, 
            model_name, 
            'search_read', 
            [domain], 
            {'fields': [field_name]}
        )
        
        # Calculate the total of the expected_revenue field
        total_expected_revenue = sum(record[field_name] for record in records)
        
        message = f"There are {record_count} Quotations with a total value : {total_expected_revenue}."
        dispatcher.utter_message(text=message)

        return []


# Ouestion 3 | Done
class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "action_last_quotation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # Set the model name and field names
        model_name = 'crm.lead'
        field_names = ['quotation_no', 'partner_id', 'street', 'date_open','expected_revenue']
        
        # Define the search criteria
        domain = [('quotation_no', '!=', False)]
        
        # Sort by date_open field in descending order to get the latest quotation
        order = 'date_open desc'
        
        # Limit to one record to get the latest quotation
        limit = 1

        # Execute the search_read method
        sale_orders = models.execute_kw(
            db, 
            uid, 
            password, 
            model_name, 
            'search_read',
            [domain],
            {'fields': field_names, 'order': order, 'limit': limit}
        )
        
        if sale_orders:
            order = sale_orders[0]
            customer_name = order['partner_id'][1]
            expected_revenue = order['expected_revenue']
            quotation_no = order['quotation_no']
            message = f"The latest quotation : {quotation_no} \n customer : {customer_name} \n with value : {expected_revenue}."
        else:
            message = "No quotation found."
        
        dispatcher.utter_message(text=message)
        return []



# Question 4 | done
class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "action_quotation_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("quotation_number").upper()
        import xmlrpc.client
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # order_id = 'Q00004'

        # Select data from the table 'sale.order'
        sale_orders = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
                                        [],
                                        {'fields': ["quotation_no","stage_id",'partner_id','expected_revenue']})

        j = ''
        name = ''
        value = ''

        for sale_order in sale_orders:
            if sale_order["quotation_no"] == order_id:
                j = sale_order["stage_id"]
                name = sale_order["partner_id"]
                value = sale_order["expected_revenue"]
            # print("Sale order status: ", sale_order['status'])

        if j:
            message = (f"The status of Quotation : {order_id} is {j[1]} \n name : {name[1]} \n value : {value} ")
        else:
            message = f"The quotation number {order_id} is not found in the system."

        dispatcher.utter_message(text=message)
        # print(j[1])
        return []


# Question 5 | Done
class ActionPurchaseStatus(Action):
    def name(self) -> Text:
        return "action_purchase_status"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        purchase_id = tracker.get_slot("purchase_id").upper()
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Search for the purchase order by name
        sale_orders = models.execute_kw(db, uid, password, 'purchase.order', 'search_read',
                                        [],
                                        {'fields': ["name",'partner_id','amount_total','state']})
        order_found = False
        for sale_order in sale_orders:
            if sale_order["name"] == purchase_id:
                order_found = True
                j = sale_order["name"]
                name = sale_order["partner_id"]
                value = sale_order["amount_total"]
                state = sale_order["state"]
                message = (f"The Purchase Order : {purchase_id} \n name : {name[1]} \n value: {value} \n status: {state}")
                dispatcher.utter_message(text=message)
                break
        
        if not order_found:
            message = (f"The Purchase Order : {purchase_id} was not found.")
            dispatcher.utter_message(text=message)
        
        return []


# Question 6 |
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_value_sale"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Set the necessary variables
        model_name = 'sale.order'
        field_name = 'amount_total'
        domain = []
        
        # Execute the search_read method with the search_count parameter to get the total count
        record_count = models.execute_kw(
            db, 
            uid, 
            password, 
            model_name, 
            'search_count', 
            [domain]
        )
        
        # Execute the search_read method with the fields parameter to get the field values
        records = models.execute_kw(
            db, 
            uid, 
            password, 
            model_name, 
            'search_read', 
            [domain], 
            {'fields': [field_name]}
        )
        
        # Calculate the total of the amount_total field
        total_amount_total = sum(record[field_name] for record in records)
        
        message = f"There are {record_count} sale orders with a total amount of {total_amount_total}."
        dispatcher.utter_message(text=message)

        return []


# Question 7 |

class ListQuotationsAction(Action):
    def name(self) -> Text:
        return "action_list_quatation"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Connect to the XML-RPC API
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))

        # Set the model name and field names
        model_name = 'crm.lead'
        field_names = ['quotation_no', 'partner_id', 'street', 'date_open', 'expected_revenue']

        # Define the search criteria
        domain = [('quotation_no', '!=', False)]

        # Sort by date_open field in descending order to get the latest quotation
        order = 'date_open desc'

        # Execute the search method to get all quotations
        quotation_ids = models.execute_kw(
            db,
            uid,
            password,
            model_name,
            'search',
            [domain],
            {'order': order}
        )

        # Initialize variables to keep track of the start and end indices of the records to display
        start_index = 0
        end_index = min(len(quotation_ids), start_index + 4)

        # Loop through the records in batches of 4 and display them using buttons
        while start_index < len(quotation_ids):
            # Get the record data for the current batch
            record_ids = quotation_ids[start_index:end_index]
            records = models.execute_kw(
                db,
                uid,
                password,
                model_name,
                'read',
                [record_ids],
                {'fields': field_names}
            )

            # Generate a message with the data for the current batch
            message = ''
            for record in records:
                customer_name = "aj"
                expected_revenue = record['expected_revenue']
                quotation_no = record['quotation_no']
                message += f"{quotation_no}: Customer: {customer_name}, Value: {expected_revenue}\n"

            # Add buttons for navigating to the previous and next batches
            buttons = []
            if start_index > 0:
                buttons.append({
                    'title': 'Previous',
                    'payload': '/previous_quotations'
                })
            if end_index < len(quotation_ids):
                buttons.append({
                    'title': 'Next',
                    'payload': '/next_quotations'
                })

            # Send the message and buttons to the user
            dispatcher.utter_message(text=message, buttons=buttons)

            # Increment the indices for the next batch
            start_index = end_index
            end_index = min(len(quotation_ids), start_index + 4)

        return []

# Question 8 |

class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_inventry_product"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        # Get the value of the product keyword slot
        product_keyword = tracker.get_slot("pname")

        # Set the model name and field names
        model_name = 'product.template'
        field_names = ['name', 'qty_available', 'item_type']
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        # Search for products that match the product keyword
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        domain = [[('name', 'ilike', product_keyword)]]
        product_ids = models.execute_kw(db, uid, password, model_name, 'search', domain, {'limit': 10})
        
        # If no products match the keyword, inform the user and return an empty list
        if not product_ids:
            dispatcher.utter_message(text=f"No products found that match '{product_keyword}'")
            return []

        # Otherwise, display the list of matching products
        products = models.execute_kw(db, uid, password, model_name, 'read', [product_ids], {'fields': field_names})
        message = f"Found {len(products)} products that match '{product_keyword}':\n"
        dispatcher.utter_message(text=message)
        
        for product in products:
            message = f"name : {product['name'] }\n ON Hand : {product['qty_available'] } \n"
            dispatcher.utter_message(text=message)

        # Set the product selection slot to None
        # dispatcher.utter_slot("pname", None)

        return []
    
# Question 9 |

class CountEntriesAction(Action):
      def name(self) -> Text:
        return "action_sjo_list"

      def run(self, dispatcher: CollectingDispatcher,
              tracker: Tracker,
              domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
            telegram_id = tracker.sender_id
            url, db, username, password = jay(telegram_id)
            common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
            uid = common.authenticate(db, username, password, {})
            models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
            # Set the model name and field names
            model_name = 'sale.job.order'
            field_names = ['customer_id', 'status', 'name']  # update field_names here

            # Get the ids of all Sale Job Orders with state=in-progress
            sjo_ids = models.execute_kw(
                db, uid, password,
                model_name, 'search',
                [[('status', '=', 'progress')]],
                {'limit': 10}
            )

            # Get the details of each Sale Job Order and format the response
            message = 'Here are the Sale Job Orders with a status of "in-progress":\n\n'
            dispatcher.utter_message(text=message)
            
            for sjo_id in sjo_ids:
                sjo_data = models.execute_kw(
                    db, uid, password,
                    model_name, 'read',
                    [sjo_id],
                    {'fields': field_names}
                )[0]
                message = f"Number: {sjo_data['name']} \nCustomer Name: {sjo_data['customer_id'][1]} \n"
                dispatcher.utter_message(text=message)

            return []
        
        
class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "test"

    def run(self, dispatcher: CollectingDispatcher, tracker: Tracker, domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        telegram_id = tracker.sender_id # extract the chat_id from the sender_id
        dispatcher.utter_message(text=telegram_id)
        # use the telegram_id for any further processing

class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "action_quotation_name_address"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        order_id = tracker.get_slot("quotation_number")
        order_id = order_id.upper()
        import xmlrpc.client
        url = 'http://192.168.0.145:3333/'
        db = 'mar6_rapid_bevtech'
        username = 'admin'
        password = 'admin'
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        # order_id = 'Q00004'
        domain = []
        if order_id:
            domain = [[['quotation_no','=',order_id]]]
        # Select data from the table 'sale.order'
        sale_orders = models.execute_kw(db, uid, password, 'crm.lead', 'search_read',
                                    [[]],
                                    {'fields': ["quotation_no","partner_id","street"]})
        for sale_order in sale_orders:
            if sale_order["quotation_no"] == order_id:
                j = sale_order["partner_id"]
                k = sale_order["street"]
            # print("Sale order status: ", sale_order['status'])
        message = (f"The Quotation {order_id} Customer name is {j[1]} and address is {k} ")
        dispatcher.utter_message(text=message)
        # print(j[1])
        return []

class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "action_latest_quotation_revision"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the quotation number and convert it to uppercase
        search_quotation = tracker.get_slot("quotation_number").upper()
        
        import xmlrpc.client
        # url = 'http://192.168.0.145:3333/'
        # db = 'mar6_rapid_bevtech'
        # username = 'admin'
        # password = 'admin'
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Search for the latest revision of the given quotation number
        quotation_ids = models.execute_kw(db, uid, password, 'crm.lead', 'search',
                                          [[('quotation_no', 'ilike', search_quotation)]])
        latest_revision = None
        
        for quotation_id in quotation_ids:
            quotation = models.execute_kw(db, uid, password, 'crm.lead', 'read',
                                           [quotation_id],
                                           {'fields': ['quotation_no']})[0]['quotation_no']
            parts = quotation.split(" - ")
            # print(parts)
            if len(parts) == 2:
                quotation_num, revision_num = parts
                if latest_revision is None or revision_num > latest_revision:
                    latest_revision = revision_num
                    # print("hey i am ",latest_revision)
                    break
            else:
                latest_revision = None
        # print("hey ",latest_revision)
        
        # Construct the message to be sent back to the user
        if latest_revision is not None:
            latest_quotation = f"{search_quotation} - {latest_revision}"
            message = f"The latest quotation for {search_quotation} is: {latest_quotation}"
        else:
            message = f"No quotation found for {search_quotation}"
        
        dispatcher.utter_message(text=message)

        return []

class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "action_no_quotation_today"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the quotation number and convert it to uppercase
        
        url = 'http://192.168.0.145:3333/'
        db = 'mar6_rapid_bevtech'
        username = 'admin'
        password = 'admin'
        
        # Authenticate and create the XML-RPC client
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Get the count of quotations created today
        today_str = str(datetime.date.today())
        data_ids = models.execute_kw(db, uid, password, 'crm.lead', 'search',
                                          [[('create_date', '>=', f"{today_str} 00:00:00")]])
        count = len(data_ids)

        message = f"{count} quotations were created today."
        
        dispatcher.utter_message(text=message)

        return []

class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "action_no_quotation_month"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the quotation number and convert it to uppercase
        
        # url = 'http://192.168.0.145:3333/'
        # db = 'mar6_rapid_bevtech'
        # username = 'admin'
        # password = 'admin'
        
        # Authenticate and create the XML-RPC client
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
       
        # Get the count of quotations created this month
        today = datetime.date.today()
        start_of_month = today.replace(day=1)
        end_of_month = start_of_month.replace(day=28)
        record_count = models.execute_kw(
            db, uid, password, 'crm.lead', 'search_count',
            [[('create_date', '>=', start_of_month.strftime('%Y-%m-%d %H:%M:%S')),
              ('create_date', '<=', end_of_month.strftime('%Y-%m-%d %H:%M:%S'))]]
        )
        
        message = f"{record_count} quotations were created this month."
        dispatcher.utter_message(text=message)

        return []

class ActionQuotationStatus(Action):
    def name(self) -> Text:
        return "action_no_quotation_quarter"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
        
        # Get the quotation number and convert it to uppercase
        
        # url = 'http://192.168.0.145:3333/'
        # db = 'mar6_rapid_bevtech'
        # username = 'admin'
        # password = 'admin'
        
        # Authenticate and create the XML-RPC client
        telegram_id = tracker.sender_id
        url, db, username, password = jay(telegram_id)
        common = xmlrpc.client.ServerProxy('{}/xmlrpc/2/common'.format(url))
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy('{}/xmlrpc/2/object'.format(url))
        
        # Get the count of quotations created this quarter
        today = datetime.date.today()
        quarter_start_month = (today.month - 1) // 3 * 3 + 1
        start_of_quarter = datetime.date(today.year, quarter_start_month, 1)

        # format the datetime object as a string
        start_of_quarter_str = start_of_quarter.strftime('%Y-%m-%d %H:%M:%S')
        end_of_quarter = start_of_quarter.replace(month=start_of_quarter.month+2, day=28).strftime('%Y-%m-%d %H:%M:%S')

        # Search for records created within the current quarter
        record_count = models.execute_kw(db, uid, password, 'crm.lead', 'search_count',
                                        [[('create_date', '>=', start_of_quarter_str), ('create_date', '<=', end_of_quarter)]])

        message = f"{record_count} quotations were created this quarter."
        
        dispatcher.utter_message(text=message)

        return []
# =====================================================fall========================
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
        dispatcher.utter_message(template="my_custom_fallback_template")

        # Revert user message which led to fallback.
        return [UserUtteranceReverted()]
    
    
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
class CountEntriesAction(Action):
    def name(self) -> Text:
        return "action_crm_uncontacted_customers_last_month"

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

        # Send the list of customers to the user
        if len(customers) > 0:
            for customer in customers:
                message = f"Name: {customer['name']}, Phone: {customer['phone']}"
                dispatcher.utter_message(text=message)
        else:
            message = (
                "There are no customers that have not been contacted in the last month."
            )
            dispatcher.utter_message(text=message)

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

from json import dumps, loads
import random
import urllib.request
import requests
import datetime
import matplotlib.pyplot as plt


def json_rpc(url, method, params):
            data = {
                "jsonrpc": "2.0",
                "method": method,
                "params": params,
                "id": random.randint(0, 1000000000)
            }

            req = urllib.request.Request(url=url, data=dumps(data).encode(), headers={
                "Content-Type": "application/json",
            })
            reply = loads(urllib.request.urlopen(req).read().decode('UTF-8'))
            if reply.get("error"):
                raise Exception(reply["error"])
            return reply["result"]

def call(url, service, method, *args):
    return json_rpc(url, "call", {"service": service, "method": method, "args": args})

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
        await bot.send_photo(chat_id=telegram_id, photo="sales_chart.png")
        os.remove("sales_chart.png")

        # dispatcher.utter_message(text=message)

        return []
