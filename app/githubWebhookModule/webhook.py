# app/githubWebhookModule
import requests

from app import app, line_bot_api
from flask import Blueprint, request
from linebot.models import TextSendMessage

githubBlueprint = Blueprint('githubWebhook', __name__)

@githubBlueprint.route('/github/webhook', methods=["POST"])
def callback():
  data = request.json

  eventType = request.headers.get('X-Github-Event')
  if eventType == 'create':

    # seseorang sedang membuat branch baru di remote repo
    if data['ref_type'] == 'branch':
      refMaster = data['master_branch']
      refName = data['ref']
      actor = data['sender']['login']
      refLink = data['repository']['html_url']

      message = actor + " telah membuat branch baru namanya " + refName + " dari branch " + refMaster + " : " + refLink+"/tree/"+refName
      line_bot_api.push_message(app.config["roomId"], TextSendMessage(text=message))
  elif eventType == 'pull_request':

    # seseorang sedang melakukan pull request
    if data['action'] == 'opened':
      link = data['pull_request']['html_url']
      headRepo = data['pull_request']['head']['ref']
      baseRepo = data['pull_request']['base']['ref']
      actor = data['sender']['login']

      message = "si " + actor + " udah bikin pull request dari " + headRepo + " ke " + baseRepo + ", tolong di review ya, ini link nya " + link
      line_bot_api.push_message(app.config["roomId"], TextSendMessage(text=message))
  elif eventType == 'repository':

    if data['action'] == 'unarchived':
      repoName = data['repository']['name']
      repoLink = data['repository']['html_url']

      message = "Alhamdulillah ya repository " + repoName + " udah aktif lagi, yuk kita berkontribusi lagi. cek linknya di + " + repoLink
      line_bot_api.push_message(app.config["roomId"], TextSendMessage(text=message))
    elif data['action'] == 'archived':
      repoName = data['repository']['name']
      repoLink = data['repository']['html_url']

      message = "ALERT\nRepository " + repoName + " telah diarchive, tapi masih bisa diakses kok.\n makasih ya udah bersama-sama berkontribusi di repo tersebut. cek linknya di " + repoLink
      line_bot_api.push_message(app.config["roomId"], TextSendMessage(text=message))

  elif eventType == 'pull_request_review':

    if data['action'] == 'submitted':
      repoName = data['repository']['name']
      prName = data['pull_request']['title']
      prReviewLink = data['review']['html_url']

      message = "Ada review tuh buat Pull Request + " + prName + " di Repository " + repoName + ", yang bersangkutan jangan lupa cek ya di " + prReviewLink
      line_bot_api.push_message(app.config["roomId"], TextSendMessage(text=message))
  else:
    print(eventType+ " belum ada handlernya ih")

  return "OK", 200