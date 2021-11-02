# import socket programming library
import socket
import pandas as pd
import numpy as np
# import thread module
from _thread import *
import threading

print_lock = threading.Lock()


dataset = pd.read_csv('googleplaystore.csv')
Category = dataset["Category"]
Cat_unique = np.unique(Category)



# thread function
def threaded(c):
    while True:

        # data received from client
        data = c.recv(1024)
        data1 = data.decode('utf-8')
        data1 = data1.split(" ",1)
        
        print(data1)
        
        if data1[0] == 'QUIT':
            remessage = 'BYE BYE'
        
        elif data1[0] == 'HELLO':
            remessage = 'HELLO::AlperBozyel'
        
        elif data1[0] == 'LIST':
            remessage = 'Categories::'
            for i in range (0,len(Cat_unique)): 
                remessage += str(Cat_unique[i])+"::"
                                
        elif data1[0] == 'APP':
            df = dataset.loc[dataset["App"] == data1[1]]
            if df.empty:
                remessage = 'NOTFOUND'
                c.sendall(remessage.encode('utf-8'))
                break
            
            remessage = "PROPS::"
            for i in range (1,11):                
                remessage += str(df.iloc[0,i])+"::"    
                              
        else:
            remessage = 'ERROR'
        
        c.sendall(remessage.encode('utf-8'))
    # connection closed
    c.close()


def Main():
    host = "127.0.0.1"

    # reverse a port on your computer
    # in our case it is 12345 but it
    # can be anything
    port = 12345
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((host, port))
    print("socket binded to port", port)

    # put the socket into listening mode
    s.listen(5)
    print("socket is listening")

   # print(Cat_unique)
    
    # a forever loop until client wants to exit
    while True:
        # establish connection with client
        c, addr = s.accept()

        # lock acquired by client
        print_lock.acquire()
        print('Connected to :', addr[0], ':', addr[1])

        # Start a new thread and return its identifier
        start_new_thread(threaded, (c,))
    s.close()   


if __name__ == '__main__':
    Main()
    
    


