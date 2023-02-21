import { SocketClient } from './client_nw_logic';


class Client{
    public static main(){
        SocketClient.startUnixSocketClient();
    }
}

Client.main()