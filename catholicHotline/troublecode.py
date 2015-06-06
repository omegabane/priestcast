def get_oldest_task_sid():
    tasks = twilio_task_router_client.tasks(workspace_sid).list()
    oldest_task = tasks[0]
    for task in tasks:
        if task.age > oldest_task.age:
            oldest_task = task
    return oldest_task.sid


@app.route('/handle_priest_input', methods=['GET', 'POST'])
def handle_priest_call():
    response = twiml.Response()
    response.say("Hi Father Joe. Connecting you to the Catholic Hotline requester now.", voice="alice")
    reservations = twilio_task_router_client.reservations(workspace_sid, get_oldest_task_sid()).list()
    reservation = [rsv for rsv in reservations if rsv.worker_sid == "WKa7932883678ca716e6b08e1451e4a69d"] #next(rsv for rsv in reservations if rsv.sid=="WKa7932883678ca716e6b08e1451e4a69d")
    requests.post("https://taskrouter.twilio.com/v1/Workspaces/WS529cc3e217f338ed477aea71f208a6a0/Tasks/" +
                  reservation.task_sid + "/Reservations/" + reservation.sid, data={"reservation_status":"accepted"},
                  auth=('ACf07837c042d5b5a4cbce45f5b93239a7', 'bafa08318cea96ce943972c9cad4a58e'))
    response.dial("4085409994", callerId="4153001404")
    return response.toxml()
