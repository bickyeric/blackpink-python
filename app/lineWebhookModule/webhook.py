# app/lineWebhookModule
import requests

from app import app
from flask import Blueprint, request
from linebot import WebhookHandler, LineBotApi
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)

from linebot.models import *

lineBlueprint = Blueprint('lineWebhook', __name__)

line_bot_api = LineBotApi(app.config["channel_access_token"])
handler = WebhookHandler(app.config["channel_secret"])

def unhandledMessage(event):
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(
			text="ini ma contoh aja ih!!!!"
		)
	)

def shareProfileMessage(event):
	username = event.message.text.split(" ")[2]
	response = requests.get("https://api.github.com/users/{}".format(username))
	data = response.json()
	app.logger.info(data)
	if response.status_code == 200:
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(
				text = "fullName = {}\ncompany = {}\nlocation = {}\nfollowers = {}\nfollowing = {}\npublic repo = {}\npublic gist = {}\n".format(data['name'], data['company'], data['location'], data['followers'], data['following'], data['public_repos'], data['public_gists'])
			)
		)
	else:
		line_bot_api.reply_message(
			event.reply_token,
			TextSendMessage(
				text = "Tidak ditemukan"
			)
		)

@lineBlueprint.route('/callback', methods=["POST"])
def callback():
  signature = request.headers['X-Line-Signature']

  data = request.get_data(as_text=True)

	# handle webhook body
  try:
    handler.handle(data, signature)
  except InvalidSignatureError as e:
    app.logger.error("Error Occurred : {}".format(e))
  except LineBotApiError as l:
    app.logger.error("Error Occurred : {}".format(l))
  finally:
    app.logger.info("Finished!!!")

  return "OK", 200

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
	app.logger.info(event)
	try:
		# if "Cari profil" in event.message.text:
		# 	shareProfileMessage(event)
		# #else:
		unhandledMessage(event)
	except Exception as e:
		app.logger.warning("error detected " + e.message)

	return 'OK'