import sys
from threading import Thread
from queue import Queue
import pyfiglet
import socket

banner = pyfiglet.figlet_format('PORT SCANNER')
print(banner)

target = sys.argv[1]
print(target) 

socket.gethostbyname(target)

#Thread class
class startWorks(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            port = self.queue.get()
            try:
                portProcessing(port)
            except Exception as e:
                print(e)

            finally:
                self.queue.task_done()

#Port processor using socket
def portProcessing(port):
    #socket.AF_INET -> é a familia do endereço, neste caso ipv4
    #SOCK_STREAM -> é um socket para TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    socket.setdefaulttimeout(1)

    #conecta a uma URL
    result = s.connect_ex((target, port))

    if result == 0:
        print("Port {} is open".format(port))
    s.close


#Main function
def main():
    queue = Queue()
    for worker in range(40):
        worker = startWorks(queue)
        worker.daemon = True
        worker.start()
    
    for port in range(1, 444):
        queue.put(port)

    queue.join()
    

if __name__ == '__main__':
    main()




