from mailjet_rest import Client
import os
from flask_smorest import Blueprint, abort
from flask.views import MethodView
from flask import jsonify

blp = Blueprint("Email", "email", description="Operation for email")


@blp.route("/send")
class SendEmail(MethodView):
  def post(self):
    api_key = '****************************1234'
    api_secret = '****************************abcd'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
      'Messages': [
        {
          "From": {
            "Email": "msivakumars@hotmail.com",
            "Name": "Sivakumar"
          },
          "To": [
            {
              "Email": "msivakumars@hotmail.com",
              "Name": "Sivakumar"
            }
          ],
          "Subject": "Greetings from Mailjet.",
          "TextPart": "My first Mailjet email",
          "HTMLPart": "<h3>Dear passenger 1, welcome to <a href='https://www.mailjet.com/'>Mailjet</a>!</h3><br />May the delivery force be with you!",
          "CustomID": "AppGettingStartedTest"
        }
      ]
    }
    result = mailjet.send.create(data=data)

    return jsonify(
      {
        "status_code": result.status_code,
        "result": result.json()
      }
    )
    # print(result.status_code)
    # print(result.json())
