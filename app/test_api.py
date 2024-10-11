import requests

res = requests.post("http://192.168.1.10:5000/api?insert", json={
                        "title":"Чтоьо осмыслинное",
                        "text":"afdhadfhjftjadhvdjafdja"
                    })


if res.ok:
    print(res.json())
