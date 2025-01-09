import requests
import tkinter as tk
from tkinter import *
from tkinter import ttk
import pykakasi

# 不快指数の計算式
def discomfort_index(te,hu):
    # floatに変換してから計算する
    temp = float(te)
    hum = float(hu)
    return 0.81 * temp + 0.01 * hum * (0.99 * temp - 14.3) + 46.3

def clothes_judge(unpl_goto,unpl_city,city_name,goto_city_name,description):
    if unpl_goto == unpl_city:
        label_5.config(text=f"{city_name}と{goto_city_name}で服装は変えずにOK")
    elif description == '雨' or description == '小雨' or description == '雪':
        label_7.config(text='傘を持っているとよし')
    elif unpl_goto <= 55:
        label_5.config(text='寒く感じるでしょう')
        label_6.config(text='長袖シャツやセーター、ジャケットやコートを羽織ると良いでしょう\n寒さを感じる時期なので、暖かい服装を選び、体温を保つことが重要です。')
    elif 55 < unpl_goto <= 60:
        label_5.config(text='肌寒く感じるでしょう')
        label_6.config(text='長袖シャツや薄手のセーター、軽いジャケットを羽織ると良いでしょう\n肌寒さを感じる範囲なので、重ね着をして温度調整をしやすくするのがポイントです。')
    elif 60 < unpl_goto <= 65:
        label_5.config(text='快適でしょう')
        label_6.config(text='半そでシャツに薄手のブラウスなど、軽めのカーディガンやジャケットを羽織ると良いでしょう\n快適に感じる気温帯なので、特に体感に問題はないですが、少し寒さを感じた時のために薄い羽織物を準備すると良いでしょう。')
    elif 65 < unpl_goto <= 70:
        label_5.config(text='快適でしょう')
        label_6.config(text='半そでシャツやポロシャツ、軽いカーディガンや薄手のジャケットを羽織ると良いでしょう\n快適に過ごせる範囲なので、リラックスできる服装で十分です。通気性の良い素材を選んで、快適さを維持しましょう。')
    elif 70 < unpl_goto <= 75:
        label_5.config(text='少し暑いでしょう')
        label_6.config(text='半そでシャツや軽いTシャツ、通気性の良い靴やサンダルが良いでしょう\n軽やかな服装を選んで、快適に過ごせる環境を整えましょう。')
    elif 75 < unpl_goto <= 80:
        label_5.config(text='やや暑いでしょう')
        label_6.config(text='薄手の半そでシャツやTシャツ、UV対策の帽子や日焼け止めを使用しましょう\n暑さを感じるので、軽装で風通しの良い素材を選びましょう。外に長時間いる場合は、日差しや紫外線対策を強化することが大切です。')
    elif 80 < unpl_goto <= 85:
        label_5.config(text='暑くて汗が出るでしょう')
        label_6.config(text='半そでシャツやタンクトップ、通気性の良いサンダルや軽いスニーカーが良いでしょう\n暑さが強く汗をかくため、通気性の良い服装が必要です。また、水分補給を忘れずに、涼しく過ごせるように配慮しましょう。')
    elif 85 < unpl_goto:
        label_5.config(text='暑くてたまらないでしょう')  
        label_6.config(text='薄手のタンクトップや半そでシャツ、帽子やサングラス、日焼け止めなどを使用しましょう\n非常に暑く、体力を消耗しやすいため、極力外に出ないことが理想ですが、出る場合は非常に軽装で涼しさを保つことが大切です。こまめに水分補給を行い、涼しい場所で休むことを心がけてください。')  
    return

def get_weather(city,go_to_city):

    # ここにAPIキーを入力してください
    api_key = 'ae45d60f6d28c509fccb84db10ae681d'

    kks = pykakasi.kakasi()
    city = kks.convert(city)
    go_to_city = kks.convert(go_to_city)

    # OpenWeatherMapのエンドポイント
    url_city = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={city[0]['passport']}&appid={api_key}&units=metric&lang=ja"
    url_goto = f"https://api.openweathermap.org/data/2.5/weather?units=metric&q={go_to_city[0]['passport']}&appid={api_key}&units=metric&lang=ja"

    # APIリクエストを送信
    response_city = requests.get(url_city)
    data_city = response_city.json()

    response_goto = requests.get(url_goto)
    data_goto = response_goto.json()
    
    if response_city.status_code == 200 and response_goto.status_code == 200:

        # 現在地の天気情報を抽出
        description_city = data_city['weather'][0]['description']
        tem_city = data_city['main']['temp']
        hum_city = data_city['main']['humidity']

        # 行先の天気情報を抽出
        description_goto = data_goto['weather'][0]['description']
        tem_goto = data_goto['main']['temp']
        hum_goto = data_city['main']['humidity']

        #都市名を取得
        city_name = data_city['name']
        goto_city_name = data_goto['name']
        label_3.config(text=f"{goto_city_name}の現在の天気は{description_goto}, 気温は{tem_goto} °C")

        #不快指数を計算
        discom_goto = int(discomfort_index(tem_goto,hum_goto))
        discom_city = int(discomfort_index(tem_city,hum_city))

        diff_tem = int(tem_goto - tem_city)

        #気温差を判定
        if diff_tem != 0:

            #気温が高い場合
            if tem_city < tem_goto:
                label_4.config(text=f"行先の{goto_city_name}は{city_name}より{diff_tem}°C高いです")
                clothes_judge(discom_goto,discom_city,goto_city_name,city_name,description_goto)

            #気温が低い場合
            elif tem_city > tem_goto:
                label_4.config(text=f"行先の{goto_city_name}は{city_name}より{-(diff_tem)}°C低いです")
                clothes_judge(discom_goto,discom_city,goto_city_name,city_name,description_goto)

        #気温差がない場合
        else:
            label_4.config(text="気温に差はあまりないです")
            clothes_judge(discom_goto,discom_city,goto_city_name,city_name,description_goto)

    else:
        print("天気データの取得に失敗しました。", response_city.status_code)
    return



def set_clear():
    text_1.set('')
    text_2.set('')

root = tk.Tk()
root.geometry("600x200")
root.title("天気予報＆服装判定")

#オブジェクトの定義
label_1 = ttk.Label(root,text='現在一番近い都市名')
text_1 = StringVar()
entry_1 = ttk.Entry(root,textvariable=text_1)

label_2 = ttk.Label(root,text='行先の都市名')
text_2 = StringVar()
entry_2 = ttk.Entry(root,textvariable=text_2)

label_3 = ttk.Label(root)
label_4 = ttk.Label(root)
label_5 = ttk.Label(root)
label_6 = ttk.Label(root)
label_7 = ttk.Label(root)

button_1 = ttk.Button(root,text = '予報',command=lambda:get_weather(city = text_1.get(),go_to_city = text_2.get()))
button_2 = ttk.Button(root,text = 'クリア',command=lambda:set_clear())
button_3 = ttk.Button(root,text = '終了',command=quit)


#レイアウト
label_1.grid(row=0,column=0)
entry_1.grid(row=0,column=1)
label_2.grid(row=1,column=0)
entry_2.grid(row=1,column=1)
button_1.grid(row=2,column=0)
button_2.grid(row=2,column=1)
button_3.grid(row=2,column=2)
label_3.grid(row=3,column=1)
label_4.grid(row=4,column=1)
label_5.grid(row=5,column=1)
label_6.grid(row=6,column=1)
label_7.grid(row=7,column=1)

root.mainloop()