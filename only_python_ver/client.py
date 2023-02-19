import socket
import sys
import json

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sever_address = "./tcp_socket_file"

try:
    sock.connect(sever_address)
    print("Successfully connected.")
except socket.error as e:
    print(e)
    sys.exit(1)

try:
    #create JSON file by stdin/stdout
    method = input("Enter method name in the following options:\nfloor(float x), nroot(int n, int x), reverse(str s), validAnagram(str s1, str s2), sort(list[str] strArr)\n")
    params = input("Paramter?").strip().split(" ")
    param_types = input("Paramter type?").strip().split(" ")
    request_dict = {
        "method" : method,
        "params" : params,
        "param_types" : param_types,
        "id" : sever_address
    }
    request = json.dumps(request_dict)
    print(request)
    sock.sendall(bytes(request, encoding = "utf-8"))
    print("Sent request to the server.")
    sock.settimeout(2)
    try:
        response = sock.recv(256)
        print("Response from server is following contents.")
        print(response.decode())
    except TimeoutError:
        print("Socket timeout, ending listening for server messages.")
finally:
    print("Disconect from the server.")
    sock.close()