import os

from flask import Flask

app = Flask(__name__)

app.config["channel_secret"] = os.environ['ChannelSecret']
app.config["channel_access_token"] = os.environ["ChannelAccessToken"]

@app.errorhandler(404)
def not_found(error):
  return "NOT FOUND", 404

from app.lineWebhookModule import lineBlueprint

app.register_blueprint(lineBlueprint)