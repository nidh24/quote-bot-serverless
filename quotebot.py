import telebot
# import pandas as pd 
import os,time,sys,random
from datetime import datetime
import csv
import json
from datetime import datetime, timedelta
from config import Config
from s3handler import s3Access
from dynamodbhandler import dynamoDBAccess
import traceback


TOKEN = os.environ["TOKEN"]
bot = telebot.TeleBot(token=TOKEN)

def convertToIst(cronDateTime):
    return (cronDateTime + timedelta(hours=5, minutes=30)).time()


def sendDailyQuote():
	try:
		obbj = dynamoDBAccess(Config.table_name)
		response = obbj.scan_table()
		quote,author = quote_generator()
		for user in response:
			chat_id = int(user["chat_id"])
			first_name = user["first_name"]
			try:
				print("sending quote to "+first_name) 
				# if first_name == "Nidhish" or first_name == "QASSECRET":
				bot.send_message(chat_id,"Hi, "+first_name+"\nHere's your daily quote\n"+str(quote)+"\n"+"\t"+" - "+str(author))
			except telebot.apihelper.ApiTelegramException:
				print(first_name," blocked the bot")
	except Exception as e:
		print("Exception: ",str(e))
		traceback.print_exc()
		
		

def daily_quote(event):
	cronDateTime = event["time"]
	crontime_ist = convertToIst(datetime.strptime(cronDateTime, "%Y-%m-%dT%H:%M:%SZ"))
	if crontime_ist == Config.morningQuoteTime:
		sendDailyQuote()


def message_check_in(event):
	message = json.loads(event['body'])['message']
	chat_id = message['chat']['id']
	sender = message['from']['first_name']
	text = message['text']
	date = message['date']
	username = message['chat']["username"]
	return chat_id, sender, text, username, date


def start_msg(chat_id, sender, username, date):
	obj = dynamoDBAccess(Config.table_name)
	obj.putRow(chat_id,date,sender,username)

	if obj.filter_table(chat_id):
		msg_to_be_sent = Config.commands["welcome"].format(sender)
	else:
		msg_to_be_sent = Config.commands["welcome_back"].format(sender)
	bot.send_message(chat_id, msg_to_be_sent)


def quote_generator():
	try:
		s3Obj = s3Access()
		csv_number = random.randint(0,48)
		file_location = Config.quotesLocation + str(csv_number) + Config.CSV_EXT 
		quotes = s3Obj.readCsvFile(file_location)
		quotes = quotes.dropna(axis = 'index')
		index = random.randint(1,10001)
		print(csv_number, index)
		send_this_quote = quotes.loc[index]
		quote = send_this_quote['quote']
		author = send_this_quote['author']
		print(quote, author)
		return quote,author
	except Exception as e:
		traceback.print_exc()
		return str(e),"error"


def send_msg(chat_id):
	quote,author = quote_generator()
	bot.send_message(chat_id,str(quote)+"\n"+"\t"+" - "+str(author))


def handle_msg(event):
	chat_id, sender, text, username, date = message_check_in(event)
	try:
		msg = text.lower().strip()
		print(msg)
		if msg == "/help" or msg == "/hello":
			bot.send_message(chat_id, Config.commands[msg])
		elif msg == "/start":
			start_msg(chat_id, sender, username, date)
		elif msg == "/send":
			send_msg(chat_id)
		else:
			bot.send_message(chat_id, Config.commands["default"])
	except Exception as e:
		traceback.print_exc()
		print("Exception: ",str(e))
		bot.send_message(chat_id, Config.commands["Exception"])
