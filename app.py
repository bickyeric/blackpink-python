import logging
import requests
import os

from flask import Flask, request, abort
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError, LineBotApiError
)
from linebot.models import *

app = Flask(__name__)

# botPush
channel_secret = os.environ['ChannelSecret']
channel_access_token = os.environ['ChannelAccessToken']

line_bot_api = LineBotApi(channel_access_token)
handler = WebhookHandler(channel_secret)

def unhandledMessage(event):
	line_bot_api.reply_message(
		event.reply_token,
		TextSendMessage(
			text="ini ma contoh aja ih!!!!"
		)
	)
@app.route("/callback", methods=['POST'])
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

	return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def message_text(event):
	try:
		unhandledMessage(event)
	except Exception as e:
		app.logger.warning("error detected")

if __name__ == "__main__":
	app.run(debug=True)
