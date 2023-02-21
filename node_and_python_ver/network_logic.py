import socket
import os
import json
from logic import Logic

class NetworkLogic:
    @staticmethod
    def start_unix_socket_server() -> None:
        with socket.socket(socket.AF_UNIX, socket.SOCK_STREAM) as sock:
            SERVER_ADDRESS = "./tcp_socket_file"

            NetworkLogic._bind_socket(sock, SERVER_ADDRESS)
            while True:
                connection, client_address = sock.accept()
                try:
                    logic = Logic()
                    while True:
                        request = NetworkLogic._receive_data(connection)
                        if request:
                            response = NetworkLogic._process_request(request, logic, SERVER_ADDRESS)
                            connection.sendall(response.encode("utf-8"))
                        else:
                            break
                finally:
                    print("Connection closing...")
                    connection.close()

    @staticmethod
    def _bind_socket(sock: socket.socket, address: str) -> None:
        try:
            os.unlink(address)
        except OSError:
            pass

        sock.bind(address)
        sock.listen(2)
        print(f"Listening on {address}")
    
    @staticmethod
    def _receive_data(sock: socket.socket) -> str:
        data = sock.recv(256)
        if data:
            return data.decode("utf-8")
        return ""

    @staticmethod
    def _process_request(request: str, logic: Logic, address: str) -> str:
        request_dict = json.loads(request)
        result = logic.parse_request(request_dict)
        result_type = str(type(result))
        response_dict = {
            "results": result,
            "result_types": result_type,
            "id": address,
        }
        response = json.dumps(response_dict)
        return response
    
