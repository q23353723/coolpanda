from flask import Flask, request, abort

from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    SourceUser, SourceGroup, SourceRoom,
    TemplateSendMessage, ConfirmTemplate, MessageAction,
    ButtonsTemplate, ImageCarouselTemplate, ImageCarouselColumn, URIAction,
    PostbackAction, DatetimePickerAction,
    CameraAction, CameraRollAction, LocationAction,
    CarouselTemplate, CarouselColumn, PostbackEvent,
    StickerMessage, StickerSendMessage, LocationMessage, LocationSendMessage,
    ImageMessage, VideoMessage, AudioMessage, FileMessage,
    UnfollowEvent, FollowEvent, JoinEvent, LeaveEvent, BeaconEvent,
    FlexSendMessage, BubbleContainer, ImageComponent, BoxComponent,
    TextComponent, SpacerComponent, IconComponent, ButtonComponent,
    SeparatorComponent, QuickReply, QuickReplyButton
)
import os
import psycopg2
import random
from chatbot import LineChatBOT

app = Flask(__name__)

line_bot_api = LineBotApi('HRWbC4w2S3J3JvFAQQkQnp4gxXVWtCwLWgrdanU72Y26+hwAoZvdiwhjyLPuIPdYLaqqy4ZDIC48EDGEo9FDp0VhS453OJfXEfFCwoFhZxhIFy6ESVLFr7fPuythQb4WA4gvEHkCjJ+yuMJDgzeR8gdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('4abb8726ea0ae9dc4a91154ce6fecb60')


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

@handler.add(FollowEvent)
def handle_follow(event):
    #profile = line_bot_api.get_profile(event.source.user_id)
    bubble = BubbleContainer(
        {
            "type": "bubble",
            "hero": {
                "type": "image",
                "url": "https://scdn.line-apps.com/n/channel_devcenter/img/fx/01_1_cafe.png",
                "size": "full",
                "aspectRatio": "20:13",
                "aspectMode": "cover",
                "action": {
                "type": "uri",
                "uri": "http://linecorp.com/"
                }
            },
            "body": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                {
                    "type": "text",
                    "text": "本大貓主選單",
                    "weight": "bold",
                    "size": "xl"
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "margin": "lg",
                    "spacing": "sm",
                    "contents": [
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "功能",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": "簡易聊天機器人、抽籤",
                            "wrap": true,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 4
                        }
                        ]
                    },
                    {
                        "type": "box",
                        "layout": "baseline",
                        "spacing": "sm",
                        "contents": [
                        {
                            "type": "text",
                            "text": "維護時間",
                            "color": "#aaaaaa",
                            "size": "sm",
                            "flex": 2
                        },
                        {
                            "type": "text",
                            "text": "不定期，我爽就維護(◕ܫ◕)",
                            "wrap": true,
                            "color": "#666666",
                            "size": "sm",
                            "flex": 4
                        }
                        ]
                    }
                    ]
                }
                ]
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {  
                    "type":"message",
                    "label":"所有籤桶",
                    "text":"所有籤桶"
                    }
                },
                {
                    "type": "button",
                    "style": "link",
                    "height": "sm",
                    "action": {  
                    "type":"message",
                    "label":"查看抽籤教學",
                    "text":"查看抽籤教學"
                    }
                },
                {
                    "type": "spacer",
                    "size": "sm"
                }
                ],
                "flex": 0
            }
        }
    )
    message = FlexSendMessage(alt_text="hello", contents=bubble)
    line_bot_api.reply_message(
        event.reply_token,
        message
    )
    return 0

def excludeWord(msg, event):
    exList = ['目錄', '所有籤桶', '所有籤筒', '籤桶', '籤筒', '刪除', '刪除籤桶', '刪除籤筒']
    if msg in exList:
        content = "這句話不能說，很可怕！"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    return 1

bot = LineChatBOT()

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global bot
    conn = psycopg2.connect(database="d6tkud0mtknjov", user="ifvbkjtshpsxqj", password="4972b22ed367ed7346b0107d3c3e97db14fac1dde628cd6d7f08cf502c927ee1", host="ec2-50-16-197-244.compute-1.amazonaws.com", port="5432")
    lineMessage = event.message.text
    if lineMessage[0:4] == "所有籤桶" or lineMessage[0:4] == "所有籤筒":
        sql = "SELECT KeyWord from userdata;"
        cur = conn.cursor()
        cur.execute(sql)
        keyList = list(dict.fromkeys([record[0] for record in cur.fetchall()]))
        conn.close()
        content = ""
        for row in keyList:
            content = content + row + "\n"
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    elif lineMessage[0:2] == "籤桶" or lineMessage[0:2] == "籤筒":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            for message in lineMes[2:]:
                cur = conn.cursor()
                sql = "INSERT INTO userdata (KeyWord, Description) VALUES(%s, %s);"
                cur.execute(sql, (keymessage, message))
                conn.commit()
            conn.close()
            content = "我拿到了新的籤"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    elif lineMessage[0:4] == "刪除籤桶" or lineMessage[0:4] == "刪除籤筒":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            cur = conn.cursor()
            sql = "DELETE FROM userdata WHERE KeyWord=%s;"
            cur.execute(sql, (keymessage,))
            conn.commit()
            conn.close()
            content = "我把這桶籤給全吃了"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    elif lineMessage[0:2] == "刪除":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        if excludeWord(keymessage, event) == 1:
            for message in lineMes[2:]:
                cur = conn.cursor()
                sql = "DELETE FROM userdata WHERE KeyWord=%s AND Description=%s;"
                cur.execute(sql, (keymessage, message))
                conn.commit()
            conn.close()
            content = "我把籤給仍了"
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text=content))
            return 0
    elif lineMessage[0:2] == "抽籤":
        lineMes = lineMessage.split(';')
        keymessage = lineMes[1]
        cur = conn.cursor()
        sql = "SELECT Description from userdata where KeyWord=%s;"
        cur.execute(sql, (keymessage,))
        DescList = [record[0] for record in cur.fetchall()]
        conn.close() 
        content = random.choice(DescList)
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))
        return 0
    else:
        content = str(bot.getResponse(lineMessage))
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=content))  
        return 0

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)