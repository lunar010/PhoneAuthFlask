from flask import Flask
import random

app = Flask(__name__)

@app.route("//api/v1/create[<number>]")
def main(number):
    global load
    global auth_num
    with open('./data/auth', "a") as f: 
        auth_num = random.randint(100001, 999998)
        f.write(str(auth_num) + "\n")

    from twilio.rest import Client 
    account_sid = 'SID' ; auth_token = 'AUTH' 
    client = Client(account_sid, auth_token) 
    froms = "+1 612-778-4602"
    message = client.messages.create(to=f"+82 {number}", from_=froms, body=f"[이름없음] 인증번호 {auth_num} 를 입력하세요.") 
    print(f"To: {number} From: {froms} SID: {message.sid} Content: {auth_num}")

    return message.sid

@app.route("//api/v1/auth[<code>]")
def auth(code):
    global load
    with open('./data/auth') as f: 
        load = f.read()

    if code in load:
        with open('./data/auth') as f:
            with open("./data/auth", "r") as f: 
                lines = f.readlines() 
                with open("./data/auth", "w") as f: 
                    for line in lines: 
                        if line.strip("\n") != str(code): 
                            f.write(line)
        return "Code valid"
    else:
        return "Code invalid"

if __name__ == "__main__":
    app.run()