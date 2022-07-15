from dataclasses import replace
from msilib.schema import Directory
from queue import Queue
from threading import Thread
from queue import Queue
import sys
import requests


# Variaveis Globais
filePath = 'wordlist.txt'
listaDeDiretorios = []
urlAttack = 'https://google.com.br/RECON'



class startWorks(Thread):
    def __init__(self, queue):
        Thread.__init__(self)
        self.queue = queue

    def run(self):
        while True:
            diretorio = self.queue.get()
            try:
                FuzzingRequest(diretorio, urlAttack)

            except Exception as e:
                print(e)

            finally:
                self.queue.task_done()


def ListaDiretorios(file):
    with open(f'ReconFuzzingDirectory/{file}', 'r') as urls:
        for url in urls:
            url = url.rstrip('\n')
            listaDeDiretorios.append(url)


def FuzzingRequest(Diretorio, urlAttack):
    urlAttack = urlAttack.replace('RECON', Diretorio)
    response = requests.get(urlAttack)
    if(response.status_code == 200):
        return print(f'{urlAttack} {response.status_code}')


def main():
    queue = Queue()
    ListaDiretorios(filePath)

    for worker in range(30):
        worker = startWorks(queue)
        worker.daemon = True
        worker.start()

    for fuzzlist in listaDeDiretorios:

        queue.put(fuzzlist)

    queue.join()






if __name__ == '__main__':
    main()
    

