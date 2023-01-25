import requests

Code = """Your Script"""
Token = "YOUR_TOKEN"

requests.post(
    url="http://localhost:5000/_Page_",
        json={"code":Code, "description":"_Description_", "user":"_User_", "pass":"_Pass_"}, 
            headers={"Authorization": f"Bearer {Token}"}) # < Will send the data to API