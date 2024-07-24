from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, ReplyMessageRequest, TextMessage
from linebot.v3.webhooks import MessageEvent, TextMessageContent
from linebot.models import MessageEvent, TextMessage, TextSendMessage, QuickReply, QuickReplyButton, MessageAction

app = Flask(__name__)

configuration = Configuration(access_token='SVStz7rysHeyn016ATPULogdP+1Hv35X4WxsZpISb2gxthTRpgtCw6IGQftmURa+R+wwTGi/EW/tWOujmqLe7XkwGEW7h/nAJGhlglP9ldUc1lOVPukZBgboMNbAd5dFIllzpaneLZql9KmID4pOpAdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('edd73f046ddd46fde4d3d9c8c495d7db')


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
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    msg = event.message.text

    if msg == '開始猜拳':
        reply_message = TextSendMessage(
            text='選擇一個動作',
            quick_reply=QuickReply(
                items=[
                    QuickReplyButton(action=MessageAction(label='剪刀', text='剪刀')),
                    QuickReplyButton(action=MessageAction(label='石頭', text='石頭')),
                    QuickReplyButton(action=MessageAction(label='布', text='布'))
                ]
            )
        )
    else:
        reply_message = TextSendMessage(text=msg)
        
    line_bot_api.reply_message(event.reply_token, reply_message)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.reply_message_with_http_info(
            ReplyMessageRequest(reply_token=event.reply_token, messages=[reply_message])
        )
        
if __name__ == "__main__":
    app.run()