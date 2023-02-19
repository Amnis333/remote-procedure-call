import socket
import os
import json
import sys
from logic import Logic

class NetworkLogic:
    @staticmethod
    def start_unix_socket_server():
        # Use staticmethod decorator to indicate that this method does not use instance variables
        # Rename the method to follow snake_case naming convention
        # Move the import of logic module inside the method to avoid importing unnecessary modules
        # Use a try-except block to catch OSError instead of FileNotFoundError which is more specific to files
        # Change the constant server_address to use an uppercase naming convention
        # Use a with statement to automatically close the socket
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            SERVER_ADDRESS = './tcp_socket_file'
            try:
                os.unlink(SERVER_ADDRESS)
            except OSError:
                pass

            sock.bind(SERVER_ADDRESS)
            sock.listen(2)

            while True:
                connection, client_address = sock.accept()
                try:
                    print('Successfully connected client-side.')
                    logic = Logic()
                    while True:
                        # Receiving JSON from client-side
                        request = connection.recv(256)
                        print("request: ", request)
                        if request:
                            results = logic.translate_JSON_to_function(json.loads(request.decode()))
                            result_type = str(type(results))
                            print(result_type)            
                            response_str = {
                                "results" : results,
                                "result_types" : result_type,
                                "id" : SERVER_ADDRESS
                            }
                            response = json.dumps(response_str)
                            connection.sendall(response.encode("utf-8"))
                        else:
                            break
                    
                finally:
                    print('Closing socket')
                    connection.close()
    
    @staticmethod
    def start_unix_socket_client():
        # Use staticmethod decorator to indicate that this method does not use instance variables
        # Rename the method to follow snake_case naming convention
        # Change the constant sever_address to use an uppercase naming convention
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            SERVER_ADDRESS = "./tcp_socket_file"

            try:
                sock.connect(SERVER_ADDRESS)
                print("Successfully connected.")
            except socket.error as e:
                print(e)
                sys.exit(1)

            try:
                method = input("Enter method name in the following options:\nfloor(float x), nroot(int n, int x), reverse(str s), validAnagram(str s1, str s2), sort(list[str] strArr)\n")
                params = input("Paramter?").strip().split(" ")
                param_types = input("Paramter type?").strip().split(" ")
                request_dict = {
                    "method" : method,
                    "params" : params,
                    "param_types" : param_types,
                    "id" : SERVER_ADDRESS
                }
                request = json.dumps(request_dict)
                print(request)
                sock.sendall(request.encode("utf-8"))
                print("Sent request to the server.")
                sock.settimeout(2)
                try:
                    response = sock.recv(256)
                    print("Response from server is following contents.")
                    print(response.decode())
                except socket.timeout:
                    print("Socket timeout, ending listening for server messages.")
            finally:
                print("Disconnect from the server.")