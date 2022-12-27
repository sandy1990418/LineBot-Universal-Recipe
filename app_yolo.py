## https://ithelp.ithome.com.tw/articles/10279933

from flask import Flask, request, abort

#https://pypi.org/project/line-bot-sdk/
from linebot import (
    LineBotApi, WebhookHandler
)
from linebot.exceptions import (
    InvalidSignatureError
)
from linebot.models import *
import re
from dataframe import *
import pandas as pd
import urllib.request
import json
from kitchen_story import *
from googletrans import Translator
import cv2 as cv
import torch 
torch.hub.set_dir('D:/課程學習/政大課程/研究所課程/統計諮詢/linebot/food-recognition/yolov5')
#from linebot.models.send_messages import ImageSendMessage

#from moon import *

app = Flask(__name__)



# 必須放上自己的Channel Access Token(在line那邊按下issue)
line_bot_api = LineBotApi('CH3wOyE/D+WDGV9W7RWE/BsjOnBaM+ek4dm6GFO5THJjkxO7mcqBUNviesI7fJMdKM7fRxKgIZnbY11TU9SU2wWYuW8EI06LFl8iRIKtNdwgAv53ZKFyCtTQNR67hLoRn1q7wHupV/QIeLfU4SDnzAdB04t89/1O/w1cDnyilFU=')
# 必須放上自己的Channel Secret
handler = WebhookHandler('8123ee61268493ff2d037552df0089b5')



# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    
    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'



keyword = []
@handler.add(MessageEvent) #, message=TextMessage
def handle_message(event):
    global keyword, keyword_copy
    if (event.message.type == "image"):
        
        #event.contentProvider.originalContentUrl
        model = torch.hub.load('ultralytics/yolov5', 'yolov5l')  # yolov5n - yolov5x6 or custom
        image_content  = line_bot_api.get_message_content(event.message.id)
 
        
        path='./img/test.jpg'
        with open(path, 'wb') as fd:
            for chunk in image_content.iter_content():
                fd.write(chunk)
                
        results = model(cv.imread('./img/test.jpg',1)) 
        img_corp = results.crop()
        keywordtmep = list(set([img_corp[i]['label'].split(" ")[0] for i in range(len(img_corp)) if img_corp[i]['label'].split(" ")[0] not in (['bowl','cup','dining','spoon','sandwich'])]))
        
        translator = Translator() 
        keywordtmep = [translator.translate(i, dest='zh-TW').text for i in keywordtmep]
        #print(keywordtmep)
        
        keyword.extend(keywordtmep)
        print(keyword)
    else : 
        # keywordtmep=[event.message.text]
        # keyword.extend(keywordtmep)
        
        while "開始搜尋" not in keyword:        
            temp = [event.message.text]
            print(temp)
            keyword.extend(temp)
            print(keyword)
            
            if "開始搜尋" in keyword:
                
                keyword_copy = keyword[:-1].copy()
                keyword = []
                break
            return keyword_copy
    # keyword=event.message.text

    #line_bot_api.reply_message(
     #   event.reply_token,
      #  TextSendMessage(text="等我一下 我找一下"+event.message.text+"食譜"))
    
    print(keyword_copy)
    condition = [['<15', '<30', '>=30'], ['有教學影片', '無教學影片'],['<=3', '<=5'], ['<=3', '<=5', '<=7'], ['按讚數最高', '點擊數最高']]
    condition_ingrediant = [j for i in condition for j in i]
    condition_filter = []
    for i in condition:
        x = []
        for j in keyword_copy:
            if j in i:
                x.append([j])
        if x != []:
            condition_filter += x[-1]
        else:
            condition_filter += ['']
    print(condition_filter) 
    data = generate_data([i for i in keyword_copy if i not in condition_ingrediant] ,5)
    #keyword = ['牛奶', '時間管理大師', '30分鐘內完成', '開始搜尋']
    #import pandas as pd
    #data = pd.read_csv('D:/recipe/results/data_牛奶.csv')
    #時間管理大師
    if condition_filter[0]=="<15":
        data = data[data.烹飪時間<15]
    elif condition_filter[0]=="<30":
        data = data[data.烹飪時間<30]
    elif condition_filter[0]==">=30":
        data = data[data.烹飪時間>=30]
    #手把手教學
    elif condition_filter[1]=="有教學影片":
        if "有無影片" in data.columns :
            data = data[data['有無影片'] == '有影片']
        else:
            line_bot_api.reply_message(
                event.reply_token,
                TextSendMessage(text="請搜尋其他食材"))
    elif condition_filter[1]=="無教學影片":
        if "有無影片" in data.columns :
            data = data[data['有無影片'] != '有影片']
        else:
            data = data
    #熱門食譜
    elif condition_filter[4]=="按讚數最多":
        data = data.sort_values(["按讚數"],ascending=False)
    elif condition_filter[4]=="點擊數最多":
        data = data.sort_values(["點擊次數"],ascending=False)
    #步驟少一點
    elif condition_filter[2]=="三步內":
        data = data[data.烹飪步驟<=3]
    elif condition_filter[2]=="五步內":
        data = data[data.烹飪步驟<=5]
    #食材不太夠
    elif condition_filter[3]=="<=3":
        data = data[data.食材種類 <= 3]
    elif condition_filter[3]=="<=5":
        data = data[data.食材種類 <= 5]
    elif condition_filter[3]=="<=7":
        data = data[data.食材種類 <= 7]
    
    #判斷是否有值
    if data.empty:
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="請搜尋其他條件"))
    else:
        data = data.iloc[:,2:12]
        data = data.reset_index(drop = True)
        food_name = data.loc[0,'食譜名稱']
        food_image = data.loc[0,'圖片連結']
        food_url = data.loc[0,'url']
        print(food_name)
        carousel_template_message = TemplateSendMessage(
            alt_text='Carousel template',
            template=CarouselTemplate(
                columns=[
                    CarouselColumn(
                        thumbnail_image_url=food_image,
                        title=str(food_name),
                        text='準備材料與做法:...',
                        actions=[
                            URIAction(
                                label='點我看更多',
                                uri=food_url
                            )
                        ]
                    ),
                ]
            )
        )
        # print(carousel_template_message)
        # line_bot_api.reply_message(
        # event.reply_token,
        # TextSendMessage(text=food_url))
        #line_bot_api.reply_message(event.reply_token, carousel_template_message)
        try:
            line_bot_api.reply_message(event.reply_token, carousel_template_message)

        except:
            line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=food_url))

if __name__ == "__main__":
    app.debug=False
    app.run()
    

    
## https://ithelp.ithome.com.tw/articles/10279953?sc=iThomeR