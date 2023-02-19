from network_logic import NetworkLogic
class Client:
    @staticmethod
    def main():
        NetworkLogic.start_unix_socket_client()

if __name__ == "__main__":
    Client.main()
