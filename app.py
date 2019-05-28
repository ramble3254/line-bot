from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
)

app = Flask(__name__)

line_bot_api = LineBotApi('5nsqTbXHZVVERwNqu53plQtRLj1NLDjMdne2OCC11pBQcydRX6czEkbCZ5zmf7oQsonglyweUwwJzHc/QnxrU3xFL1F0th4mXjVG/Xu9d1GVM1oW14cz9qC6Tlu0lkzJP2Q9hTSbxv2edt1MievpGAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('7aa2a4d19cc7a8df46b0dd1659435f67')


@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        print("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))


if __name__ == "__main__":
    app.run()