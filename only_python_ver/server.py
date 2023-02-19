import socket
import os
import logic
import json

sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
server_address = './tcp_socket_file'

try:
    os.unlink(server_address)
except FileNotFoundError:
    pass

sock.bind(server_address)
sock.listen(2)

while True:
    connection, client_address = sock.accept()
    try:
        print('Successfully connected client-side.')
        logic = logic.Logic()
        while True:
            #Receiving JSON from client-side
            request = connection.recv(256)
            print("request: ", request)
            if request:
                results = logic.translate_JSON_to_function(json.loads(request.decode()))
                result_type = str(type(results))
                print(type(results))            
                response_str = {
                    "results" : results,
                    "result_types" : result_type,
                    "id" : server_address
                }
                print(type(response_str), response_str)
                response = json.dumps(response_str)
                connection.sendall(bytes(response, "utf-8"))
            else:
                break
            
    finally:
        print('Closing socket')
        connection.close()

