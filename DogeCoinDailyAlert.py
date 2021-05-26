import requests
import json
import smtplib

URL = 'https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=INR'

def getDogePrice():
    response = requests.request('GET', URL)
    response = json.loads(response.text)
    msg = '\nDogeCoin price daily update!\nCurrent value : {}'.format(response['INR'])
    print(msg)
    sendEmail(float(response['INR']), msg)
    sendTelegramMessage(msg)
    
def sendEmail(current_value, msg):
    TO = ['vikhyath456@gmail.com']
    message = 'Subject: {}\n\n{}'.format('DogeCoin price update', msg)
    for addr in TO:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('vikhyath456@gmail.com', 'PASSWORD')
        s.sendmail(from_addr='vikhyath456@gmail.com', to_addrs=addr, msg=message)

def sendTelegramMessage(message):
    url = "https://api.telegram.org/" + 'botID' + "/sendMessage"
    data = {
        "chat_id": 'CHANNEL_ID',
        "text": message
    }
    try:
        response = requests.request("POST", url, params=data)
        print("Telegram URL :",url)
        print("Telegram response :", response.text)
        telegram_data = json.loads(response.text)
        return telegram_data["ok"]
    except Exception as e:
        print("An error occurred in sending the alert message via Telegram")
        print(e)
        return False

if __name__ == '__main__':
    getDogePrice()