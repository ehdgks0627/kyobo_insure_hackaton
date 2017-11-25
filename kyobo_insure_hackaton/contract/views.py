from django.shortcuts import render
import json
import socket
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

sock_url = "ss5h.namsu.xyz"
sock_port = 9947


def sock_send(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sock_url, sock_port))
    sock.send(data)
    response = sock.recv(4096).decode()

    return response


def send_data(data):
    request_data = {"function": "register", "data": data}
    request = json.dumps(request_data) + "\n"
    request = request.encode()
    response = json.loads(sock_send(request))

    return response["contract_addr"]


def recv_data(contract_addr):
    request_data = {"function": "search", "contract_addr": contract_addr}
    request = json.dumps(request_data) + "\n"
    request = request.encode()
    response = json.loads(sock_send(request))

    return response["data"]


def socket_test(requests):
    contract_addr = send_data("fuck to jung hwan")
    print("recv from server - ", contract_addr)
    data = recv_data(contract_addr)
    print("recv from server - ", data)
    return HttpResponse("wow")
