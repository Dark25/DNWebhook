from socket import socket
from socket import AF_INET, SOCK_STREAM


def check_port(ip):
    a_socket = socket(AF_INET, SOCK_STREAM)
    status_code = a_socket.connect_ex((ip, 14500))
    if status_code == 0:
        status = "Online"
    else:
        status = "Offline"

    a_socket.close()
    return status
