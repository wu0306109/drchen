import os

from flask import Blueprint, Response, abort, current_app, request
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage

from . import openai_client

CHANNEL_ACCESS_TOKEN = os.environ.get('CHANNEL_ACCESS_TOKEN')
CHANNEL_SECRET = os.environ.get('CHANNEL_SECRET')

line = Blueprint('line', __name__, url_prefix='/line')

line_bot_api = LineBotApi(CHANNEL_ACCESS_TOKEN)
handler = WebhookHandler(CHANNEL_SECRET)


@line.route('/', methods=['POST'])
def callback() -> Response:
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    current_app.logger.info('Request body: ' + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        current_app.logger.error(
            'Invalid signature. Please check your channel access token/channel secret.'
        )
        abort(400)

    return 'OK', 200


@handler.add(MessageEvent, message=TextMessage)
def handle_message(event) -> None:
    response = openai_client.request(event.message.text)
    line_bot_api.reply_message(
        event.reply_token,
        TextSendMessage(text=response),
    )
