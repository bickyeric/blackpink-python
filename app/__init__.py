import os

from flask import Flask
from linebot import LineBotApi

app = Flask(__name__)

app.config["channel_secret"] = os.environ['ChannelSecret']
app.config["channel_access_token"] = os.environ["ChannelAccessToken"]
app.config["roomId"] = "Re7addd65b0dfd625d1208224865f66b5"
line_bot_api = LineBotApi(app.config["channel_access_token"])

@app.errorhandler(404)
def not_found(error):
  return "NOT FOUND", 404

from app.lineWebhookModule import lineBlueprint
from app.githubWebhookModule import githubBlueprint

app.register_blueprint(lineBlueprint)
app.register_blueprint(githubBlueprint)