import socket
import threading
import json


class DBotServer:
    def __init__(self, botlist):
        self.threads = []
        self.bots = {}

        # get list of bots
        with open(botlist) as f:
            self.bots = json.load(f)

        # try to connect to them
        for i in self.bots:
            self.bots[i]['active'] = 'Unknown'

    def start_server(self):
        t = threading.Thread(target=self.serve, args=(50042,))
        self.threads.append(t)
        t.start()

    def connect_bot(self, name):
        if name in self.bots:
            try:
                HOST = '10.0.0.7'
                PORT = int(self.bots[name]['port'])

                print(f'request to connect to bot {name}')
                self.bots[name]['socket'] = socket.create_connection((HOST, PORT))
            except ConnectionRefusedError:
                self.bots[name]['active'] = "Inactive"


    def serve(self, port):
        # activity message
        print(f'serving on port {port}')

        # parameters
        HOST = ''
        PORT = port

        # connect
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((HOST, PORT))
            s.listen(1)
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(1024)
                        if not data:
                            break
                        conn.sendall(self.response(data.decode()))

    def response(self, mess):
        # grab command
        msplit = mess.split(' ', 1)
        command = msplit[0]

        # grab parameters if exists
        if len(msplit) == 2:
            mess = msplit[1]
        else:
            mess = ''

        # ## INTERNAL COMMANDS ## #

        if command == 'botlist':
            ret = {}
            for i in self.bots:
                ret['name'] = i
                ret['active'] = self.bots[i]['active']
            return json.dumps(ret).encode()
        elif command == 'connect':
            if mess != '':
                self.connect_bot(mess)

        # ## EXTERNAL COMMANDS ## #

        elif command == 'htm':
                return self.bot_command(mess)

        return mess.encode()

    def bot_command(self, message):
        print(f'message to send: {message}')
        self.sock.sendall(str.encode(message))
        data = self.sock.recv(1024)
        print('Received', data.decode())
        return data

    def ping(bot):
        # base cases
        if bot not in self.bots:
            return False
        if 'active' not in self.bots[bot]:
            return False

        # the goods
        try:
            sock = self.bots[bot]['socket']
            sock.sendall(str('ping').encode())
            data = sock.recv(1024)
        except ConnectionRefusedError:
            return False

# where dreams become reality
server = DBotServer('botlist.json')
server.start_server()
