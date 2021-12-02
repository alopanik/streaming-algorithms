import socket 
import threading
import pandas as pd
from hash_fns import *
from time import gmtime, strftime
from datasketch import MinHash, MinHashLSH




hateFile = pd.read_csv('Hate_Words.csv')
hateWords = list(hateFile['word'])

TwitchBloom = BloomFilter(hateWords)
lsh = MinHashLSH(threshold=0.75, num_perm=128)

minhashes = dict()
log = dict()
chat = {'Time' : [], 'Message' : []}

class ServerNode:
    def __init__(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_and_ip = ('127.0.0.1', 12345)
        self.node.bind(port_and_ip)
        self.node.listen(5)
        self.connection, addr = self.node.accept()

    def send_sms(self, SMS):
        self.connection.send(SMS.encode())

    def receive_sms(self):
        while True:
            data = self.connection.recv(1024).decode()
            timestamp = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            m1 = MinHash(num_perm=128)
            log[timestamp] = data
            toggle = True


            for i in str(data).split():
                if TwitchBloom.check_membership(i) == True:
                    toggle = False
                    print('BLOCKED!')
                    print('Timestamp: ', timestamp)
                    print('Message: ', log[timestamp])
                    print('Reason: ', 'Blocked for message containing a restricted word.')
                    print('\n')
                    print(pd.DataFrame(chat).to_string(index=False))
                    print('\n')
                    break
                else:
                    toggle = True
                    m1.update(i.encode('utf8'))

            if toggle == True:
                lsh.insert(timestamp, m1)
                minhashes[timestamp] = m1

                result = lsh.query(minhashes[timestamp]) 
                result.remove(timestamp)
                
                if len(result) > 0:
                    print('BLOCKED!')
                    print('Timestamp: ', timestamp)
                    print('Message: ', log[timestamp])
                    print('Reason: ', 'Blocked for having a 75%+ similar message in this window/bin.')
                    print('\n')
                    print(pd.DataFrame(chat).to_string(index=False))
                    print('\n')

                else:
                    chat['Time'].append(timestamp)
                    chat['Message'].append(data)
                    print(pd.DataFrame(chat).to_string(index=False))
                    print('\n')

    def main(self):
        while True:
            message = input()
            self.send_sms(message)

server = ServerNode()
always_receive = threading.Thread(target=server.receive_sms)
always_receive.daemon = True
always_receive.start()
server.main()
