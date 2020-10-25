# -*- coding: utf-8 -*-
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

# customer module
import crowler


app = Flask(__name__)

line_bot_api = LineBotApi('NC+N9SCHuxKdRYSSqNQ4BargO6N9siKlYuadJavs64TYXRN/dULKYj9/Ysx8qtXXVE98UVxvCzhvHIrPAwLBSChxQ2wfR/DauR4LsBncn3o5mDL9hQ+v7caE+WI32jKBkywrHMVOTTok3ylxpwIxdgdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('873eda116b01fb8f950dbad2d030de08')


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
    
    message = event.message.text
    
    if message == "匯率查詢":
        # 取得最新評價
        text = crowler.exchangeRate()
        # 包裝訊息
        remessage = TextSendMessage(text=text)
        # 回應使用者
        line_bot_api.reply_message(
                        event.reply_token,
                        remessage)
        return 0
    
    
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=event.message.text))
    

if __name__ == "__main__":
    app.run()