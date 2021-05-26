import requests
import json
import smtplib

URL = 'https://min-api.cryptocompare.com/data/price?fsym=DOGE&tsyms=INR'

def getDogePrice():
    response = requests.request('GET', URL)
    response = json.loads(response.text)
    f = open(r'C:\Users\Mittu\Desktop\DogeAlert\previous_value.txt', 'r')
    previous_value  = f.read()
    if response['INR'] >= float(previous_value) + 1:
        msg = '\nThe price of DogeCoin has increased by {} rupees!\nPrevious value : {}\nCurrent value : {}'.format(round(response['INR'] - float(previous_value), 2), previous_value, response['INR'])
        print(msg)
        sendEmail(previous_value, float(response['INR']), msg)
        sendTelegramMessage(msg)
    elif response['INR'] <= float(previous_value) - 1:
        msg = '\nThe price of DogeCoin has decreased by {} rupees!\nPrevious value : {}\nCurrent value : {}'.format(round(float(previous_value) - response['INR'], 2), previous_value, response['INR'])
        print(msg)
        sendEmail(previous_value, float(response['INR']), msg)
        sendTelegramMessage(msg)
    else:
        print('DogeCoin stable!\nPrevious value : {}\nCurrent value : {}'.format(previous_value, response['INR']))
    f = open(r'C:\Users\Mittu\Desktop\DogeAlert\previous_value.txt', 'w')
    f.write(str(response['INR']))
    f.close()

def sendEmail(previous_value, current_value, msg):
    TO = ['vikhyath456@gmail.com']
    message = 'Subject: {}\n\n{}'.format('DogeCoin price update', msg)
    for addr in TO:
        s = smtplib.SMTP('smtp.gmail.com', 587)
        s.starttls()
        s.login('vikhyath456@gmail.com', 'PASWWORD')
        s.sendmail(from_addr='vikhyath456@gmail.com', to_addrs=addr, msg=message)

def sendTelegramMessage(message):
    url = "https://api.telegram.org/" + 'botBOTID' + "/sendMessage"
    data = {
        "chat_id": '@CHAT_ID',
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