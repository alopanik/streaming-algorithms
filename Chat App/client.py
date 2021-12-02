import socket
import threading
import time

class ClientNode:
    def __init__(self):
        self.node = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        port_and_ip = ('127.0.0.1', 12345)
        self.node.connect(port_and_ip)

    def send_sms(self, SMS):
        self.node.send(SMS.encode())

    def receive_sms(self):
        while True:       
            data = self.node.recv(1024).decode()
            print(data)

    def main(self):
        while True:
            message = input()
            self.send_sms(message)


print("""

 __          __  _                                        
 \ \        / / | |                                       
  \ \  /\  / /__| | ___ ___  _ __ ___   ___               
   \ \/  \/ / _ \ |/ __/ _ \| '_ ` _ \ / _ \              
    \  /\  /  __/ | (_| (_) | | | | | |  __/              
     \/  \/ \___|_|\___\___/|_| |_| |_|\___|              
  _          _   _                                        
 | |        | | | |                                       
 | |_ ___   | |_| |__   ___                               
 | __/ _ \  | __| '_ \ / _ \                              
 | || (_) | | |_| | | |  __/                              
  \__\___/   \__|_| |_|\___|                              
  _       _____ _    _                   _                
 | |     / ____| |  | |                 | |               
 | |    | (___ | |__| |   __ _ _ __   __| |               
 | |     \___ \|  __  |  / _` | '_ \ / _` |               
 | |____ ____) | |  | | | (_| | | | | (_| |               
 |______|_____/|_|  |_|  \__,_|_| |_|\__,_|               
  ____  _                         ______ _ _ _            
 |  _ \| |                       |  ____(_) | |           
 | |_) | | ___   ___  _ __ ___   | |__   _| | |_ ___ _ __ 
 |  _ <| |/ _ \ / _ \| '_ ` _ \  |  __| | | | __/ _ \ '__|
 | |_) | | (_) | (_) | | | | | | | |    | | | ||  __/ |   
 |____/|_|\___/ \___/|_| |_| |_| |_|    |_|_|\__\___|_|   
   _____ _           _                                    
  / ____| |         | |       /\                          
 | |    | |__   __ _| |_     /  \   _ __  _ __            
 | |    | '_ \ / _` | __|   / /\ \ | '_ \| '_ \           
 | |____| | | | (_| | |_   / ____ \| |_) | |_) |          
  \_____|_| |_|\__,_|\__| /_/    \_\ .__/| .__/           
                                   | |   | |              
                                   |_|   |_|              

By Bret Francis, Jeremy Randolph, and Andrew Lopanik

Jaccard similarity threshold set to 75%

Press Enter to Submit
""")
print("Start typing >>>")


Client = ClientNode()
always_receive = threading.Thread(target=Client.receive_sms)
always_receive.daemon = True
always_receive.start()
Client.main()
