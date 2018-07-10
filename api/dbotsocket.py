import socket
import threading
import discord


class DBotSocket:
    def __init__(self, port):
        self.stats = {}
        self.active = False

        # start the server
        t = threading.Thread(target=self.serve, args=(port,))
        t.start()

    def fill_stats(self, client):
        # servers and channels
        self.stats['servers'] = {}

        # get servers
        for i in client.servers:
            sname = i.name
            self.stats['servers'][sname] = {}
            self.stats['servers'][sname]['id'] = i.id
            self.stats['servers'][sname]['channels'] = {}

            # get channels
            for j in i.channels:
                cname = j.name
                self.stats['servers'][sname]['channels'][cname] = j.id

        # set active


    def serve(self, port):
        print(f'serving on port {port}')
        HOST = ''
        PORT = port

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
                        m = 'This is from HTM'
                        conn.sendall(m.encode())
