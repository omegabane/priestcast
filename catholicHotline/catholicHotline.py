from flask import Flask, request
from twilio import twiml
from twilio.rest import TwilioRestClient, TwilioTaskRouterClient
import flask
import requests
import os

app = Flask(__name__)


twilio_rest_client = TwilioRestClient(os.environ["CATHOLIC_HOTLINE_ACCOUNT_SID"], os.environ["CATHOLIC_HOTLINE_AUTH_TOKEN"])
twilio_task_router_client = TwilioTaskRouterClient(os.environ["CATHOLIC_HOTLINE_ACCOUNT_SID"], os.environ["CATHOLIC_HOTLINE_AUTH_TOKEN"])
workspace_sid = os.environ["CATHOLIC_HOTLINE_WORKSPACE_SID"]


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
    queue_hot_line_call()
    return response.toxml()


def send_message_to_caller_contacting_priests():
    caller_number = request.values.get('From')
    twilio_rest_client.messages.create(
        to=caller_number,
        from_="+14153001404",
        body="Thanks for the call. We're contacting priests now. Expect a call in the next few minutes."
    )


def queue_hot_line_call():
    twilio_task_router_client.tasks(workspace_sid).create(
        attributes="{\"number\":\""+ request.values.get('From') +"\"}",#"{'number':'" + request.values.get('From') + "'}",
        assignment_status='pending',
        workflow_sid="WWaed381a0a7024eea2a4e6002a0ab6841",
        timeout="12000"
    )


@app.route('/reserve_priest_for_requester', methods=['GET', 'POST'])
def reserve_priest_for_requester():
    twilio_rest_client.messages.create(
        to="8023775400",
        from_="+14153001380",
        body="Hi Fr. Joe, you have an incoming call from the Catholic Hot line. Please call (415) 300-1380 to be connected."
    )
    return flask.jsonify("")


@app.route('/handle_priest_call', methods=['GET', 'POST'])
def handle_priest_call():
    response = twiml.Response()
    workers = twilio_task_router_client.workers(workspace_sid).list()
    worker = next(worker for worker in workers if request.values.get("From") in worker.attributes)
    response.say("Hi "+worker.friendly_name+". Connecting you to the Catholic Hotline requester now.", voice="alice")
    tasks = twilio_task_router_client.tasks(workspace_sid).list()
    task = next(task for task in tasks if task.assignment_status=="reserved")
    reservations = twilio_task_router_client.reservations(task.sid).list()
    reservations
    requests.post("https://taskrouter.twilio.com/v1/Workspaces/WS529cc3e217f338ed477aea71f208a6a0/Tasks/" +
                  task + "/Reservations/" + reservation_sid, data={"ReservationStatus":"accepted"},
                  auth=('ACf07837c042d5b5a4cbce45f5b93239a7', 'bafa08318cea96ce943972c9cad4a58e'))
    # reservation_sid = request.values.get('ReservationSid')
    # requests.post("https://taskrouter.twilio.com/v1/Workspaces/WS529cc3e217f338ed477aea71f208a6a0/Tasks/" +
    #               task_sid + "/Reservations/" + reservation_sid, data={"ReservationStatus":"accepted"},
    #               auth=('ACf07837c042d5b5a4cbce45f5b93239a7', 'bafa08318cea96ce943972c9cad4a58e'))
    # response.dial("4085409994", callerId="4153001404")
    print worker.friendly_name
    return response.toxml()


if __name__ == '__main__':
    app.debug=True
    app.run()
