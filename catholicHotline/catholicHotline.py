from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient, TwilioTaskRouterClient
import os

app = Flask(__name__)


twilio_rest_client = TwilioRestClient(os.environ["CATHOLIC_HOTLINE_ACCOUNT_SID"], os.environ["CATHOLIC_HOTLINE_AUTH_TOKEN"])
twilio_task_router_client = TwilioTaskRouterClient(os.environ["CATHOLIC_HOTLINE_ACCOUNT_SID"], os.environ["CATHOLIC_HOTLINE_AUTH_TOKEN"])


@app.route('/')
def hello_world():
    return 'Hello World!'


@app.route('/handle_parishioner_call', methods=['GET', 'POST'])
def handle_parishioner_call():
    response = twiml.Response()
    with response.gather(action="/handle_parishioner_input", numDigits=1) as gather:
        gather.play("https://api.twilio.com/2010-04-01/Accounts/AC8134d776156f3b4db00b12102990a2df/Recordings/" +
                    "RE5846d320e148fc55e3d6353ad1fc09a1.wav")
    response.play("https://api.twilio.com/2010-04-01/Accounts/AC8134d776156f3b4db00b12102990a2df/Recordings/" +
                  "REeb538c41c4d8587bf5273a14d269d644.wav")
    with response.gather(action="/handle_parishioner_input", numDigits=1) as gather:
        gather.play("https://api.twilio.com/2010-04-01/Accounts/AC8134d776156f3b4db00b12102990a2df/Recordings/"+
                    "RE5846d320e148fc55e3d6353ad1fc09a1.wav")
    response.play("https://api.twilio.com/2010-04-01/Accounts/AC8134d776156f3b4db00b12102990a2df/Recordings/" +
                  "REeb538c41c4d8587bf5273a14d269d644.wav")
    with response.gather(action="/handle_parishioner_input", numDigits=1) as gather:
        gather.play("https://api.twilio.com/2010-04-01/Accounts/AC8134d776156f3b4db00b12102990a2df/Recordings/" +
                    "RE5846d320e148fc55e3d6353ad1fc09a1.wav")
    response.play("https://api.twilio.com/2010-04-01/Accounts/AC8134d776156f3b4db00b12102990a2df/Recordings/" +
                  "REeb538c41c4d8587bf5273a14d269d644.wav")
    return response.toxml()


def prompt_caller_successful_request():
    response = twiml.Response()
    response.play("https://api.twilio.com/2010-04-01/Accounts/AC8134d776156f3b4db00b12102990a2df/Recordings/" +
                  "RE9bf2fe077ce0ac5dc88209d610d6cda5.wav")
    return response


@app.route('/handle_parishioner_input', methods=['GET', 'POST'])
def handle_parishioner_input():
    response = prompt_caller_successful_request()
    send_message_to_caller_contacting_priests()
    contact_priests()
    return response.toxml()


def contact_priests():
    phone_numbers = twilio_rest_client.phone_numbers.search(
        country="US",
        area_code="415",
        type="local"
    )
    phone_number = twilio_rest_client.phone_numbers.purchase(
        phone_number=phone_numbers[0].phone_number,
        voice_url="http://dan.ngrok.io/handle_priest_call?requester_number=" + request.values.get('From'),
    )
    twilio_rest_client.messages.create(
        to="number",
        from_=phone_number.phone_number,
        body="Hi Fr. Joe, you have an incoming call from the Catholic Hot line. Please call " +
             phone_number.phone_number + " to be connected."
    )


def send_message_to_caller_contacting_priests():
    caller_number = request.values.get('From')
    twilio_rest_client.messages.create(
        to=caller_number,
        from_="+14154506600",
        body="Thanks for the call. We're contacting priests now. Expect a call in the next few minutes."
    )


@app.route('/handle_priest_call', methods=['GET', 'POST'])
def handle_priest_call():
    requester_number = request.args.get('requester_number')
    response = twiml.Response()
    response.say("Hi Father Jeff, now connecting you with the Catholic Hotline requester.", voice="alice")
    response.dial(requester_number, callerId="+14154506600")
    return response.toxml()


if __name__ == '__main__':
    app.debug=True
    app.run()
