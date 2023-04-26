from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk import Action, Tracker
import requests
from typing import Any, Text, Dict, List, Union
from xmlrpc.client import ServerProxy
import xmlrpc.client    
from rasa_sdk.executor import CollectingDispatcher
import datetime
import psycopg2
import calendar
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from telegram import Bot
from typing import Final
from deep_translator import GoogleTranslator
from langdetect import detect
import io
import os
import urllib.request
from json import dumps, loads
import random
import requests
import matplotlib.pyplot as plt
from collections import defaultdict
from plotly import io
import pandas as pd
import plotly.express as px
import plotly.io as pio   
from rasa_sdk.events import SlotSet, UserUtteranceReverted
from rasa_sdk import Action, Tracker
from typing import Any, Text, Dict, List, Union
from xmlrpc.client import ServerProxy
import xmlrpc.client
from rasa_sdk.executor import CollectingDispatcher
import datetime
import psycopg2
import calendar
from datetime import timedelta
from dateutil.relativedelta import relativedelta
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, landscape
from telegram import Bot
from typing import Final
from deep_translator import GoogleTranslator
from langdetect import detect
import io
import os
import urllib.request
from json import dumps, loads
import random
import requests
import matplotlib.pyplot as plt
import matplotlib.pyplot as plt
import plotly.io as pio
import pandas as pd
import plotly.express as px
import datetime
from telegram import Bot
import telegram
import requests
import json

TOKEN = '6042767853:AAERCZHMBwaSiSY8Moamt6CHIwhMppjKFWU'
BOT_USERNAME = '@YORO_TECBLIC_BOT'
HOST = '192.168.0.145'
PORT = 3333
DB = 'mar6_rapid_bevtech'
USER = 'admin'
PASS = 'admin'
bot = Bot(token='6042767853:AAERCZHMBwaSiSY8Moamt6CHIwhMppjKFWU')


# ====================================================Needfull==================================================

def jay(sender_id):
    url = "http://192.168.0.145:3333/"
    db = "mar6_rapid_bevtech"
    username = "admin"
    password = "admin"
    return (url, db, username, password)

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

# =================================================//Needfull//=====================================================

