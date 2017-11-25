from django.shortcuts import render
import json
import socket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

sock_url = "ss5h.namsu.xyz"
sock_url = "175.202.94.120"
sock_port = 9946


def send_to_server(request):
    request = json.dumps(request) + "\n"
    request = request.encode()
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sock_url, sock_port))
    sock.send(request)
    response = sock.recv(4096).decode()
    print(response)
    response = json.loads(response)

    return response


def socket_test(requests):
    request_data = {"function": "register", "name": "hi", "time": "fuck", "product": "a"}
    response = send_to_server(request_data)
    contract_addr = response["contract_addr"]
    request_data = {"function": "search", "contract_addr": contract_addr}
    return HttpResponse(send_to_server(request_data))
