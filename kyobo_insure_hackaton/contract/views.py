from django.shortcuts import render
import json
import socket
import base64 as b64
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from .models import *

sock_url = "ss5h.namsu.xyz"
sock_port = 9947


def sock_send(data):
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.connect((sock_url, sock_port))
    sock.send(data)
    response = sock.recv(4096).decode()

    return response


def send_data(data):
    request_data = {"function": "register", "data": b64.b64encode(data.encode("utf-8")).decode("utf-8")}
    request = json.dumps(request_data) + "\n"
    request = request.encode()
    response = json.loads(sock_send(request))

    return response["contract_addr"]


def recv_data(contract_addr):
    request_data = {"function": "search", "contract_addr": contract_addr}
    request = json.dumps(request_data) + "\n"
    request = request.encode()
    response = json.loads(sock_send(request))

    return b64.b64decode(response["data"]).decode("utf-8")


def socket_test(requests):
    contract_addr = send_data(requests.GET.get("val"))
    print("recv from server - ", contract_addr)
    data = recv_data(contract_addr)
    print("recv from server - ", data)
    return HttpResponse(contract_addr + " " + data)

def contract_list(requests):
    contracts = ContractLog.objects.all()
    datas = []
    for contract in contracts:
        contract_addr = contracts["contract_addr"]
        datas.append(json.loads(recv_data(contract_addr)))
    for data in datas:
        print(data)
    return HttpResponse("a")

@csrf_exempt
def new_contract(requests):
    name = requests.POST.get("name")
    ins_title = requests.POST.get("ins_title")
    ins_fee = requests.POST.get("ins_fee")
    ins_price = requests.POST.get("ins_price")
    ins_saled_price = requests.POST.get("ins_saled_price")

    contract_addr = send_data(json.dumps(
        {"name": name, "ins_title": ins_title, "ins_fee": ins_fee, "ins_price": ins_price,
         "ins_saled_price": ins_saled_price}))

    ContractLog.objects.create(name=name, contract_addr=contract_addr)

    return HttpResponse(json.dumps({"status": "success"}))
