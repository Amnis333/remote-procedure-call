import * as net from 'net';
import * as readline from 'readline';
import * as path from 'path';
import * as os from "os";

export class SocketClient {
    public static async startUnixSocketClient(): Promise<void> {
        const socket = new net.Socket();
        const SERVER_ADDRESS = path.join(os.homedir(), "tcp_socket_file");
        console.log("SERVER_ADDRESS is here:" + SERVER_ADDRESS);

        SocketClient.connectToServer(socket, SERVER_ADDRESS);
        
        const methodName = await SocketClient.promptUser("Enter method name in the following options:\nfloor(float x), nroot(int n, int x), reverse(str s), validAnagram(str s1, str s2), sort(list[str] strArr)\n");
        const params = await SocketClient.promptUser("Parameter?");
        const paramTypes = await SocketClient.promptUser("Parameter type?");
        const requestDict = {
        "method": methodName,
        "params": params.trim().split(" "),
        "paramTypes": paramTypes.trim().split(" "),
        "id": SERVER_ADDRESS,
        };
        const request = JSON.stringify(requestDict);
        console.log(`Sending request: ${request}`);
        socket.write(request, 'utf-8');
        console.log("Sent request to the server.");

        socket.on('data', (data: Buffer) => {
        console.log(`Response from server: ${data.toString()}`);
        });
        socket.on('timeout', () => {
        console.log("Socket timeout, ending listening for server messages.");
        });
        socket.on('close', () => {
        console.log("Disconnect from server...");
        });
    }

    private static async promptUser(question: string): Promise<string> {
        console.log(question);
        const rl = readline.createInterface({
            input: process.stdin,
            output: process.stdout
        });
        return new Promise<string>(resolve => {
        rl.question(question, (answer) => {
            resolve(answer);
            rl.close();
        });
        });
    }

    private static connectToServer(socket: net.Socket, address: string): void {
        try {
        socket.connect(address);
        console.log("Successfully connected.");
        } catch (error) {
        console.error(error);
        process.exit(1);
        }
    }
}


