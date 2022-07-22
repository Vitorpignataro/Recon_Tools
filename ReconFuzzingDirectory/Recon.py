from threading import Thread
from queue import Queue
from time import  time
from tabulate import tabulate
import sys
from unittest import result
import requests
import re




# Global vars
listaDeDiretorios = []
listaStatusCode = []
listaChars = []
urlAttack = sys.argv[1]
filePath = sys.argv[2]
hiddenStatusCode = ''
hiddenChars = ''

if len(sys.argv) == 4:
    hiddenStatusCode = sys.argv[3]
elif len(sys.argv) == 5:
    hiddenStatusCode = sys.argv[3]
    hiddenChars = sys.argv[4]

hiddenChars = re.sub('[^0-9]', ' ', hiddenChars)
hiddenStatusCode = re.sub('[^0-9]', ' ', hiddenStatusCode)
listaStatusCode = (hiddenStatusCode.split())
listaChars = (hiddenChars.split())




#In case of run the script manually use hardcode input bellow

'''
filePath = 'wordlist.txt'
urlAttack = 'https:/you_target_url/RECON'
'''


#Class responsible for starting the thread system
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



#Color Palette for any types of status code response
class ResultColors:
    OK = '\033[92m'
    REDIRECT = '\033[34m'
    ERROR = '\033[91m'
    ServerError = '\033[93m'
    PATTERN = '\033[0m'
    BOLD = '\033[1m'


#Extract all words from user wordlist
def ListaDiretorios(file):
    with open(f'ReconFuzzingDirectory/{file}', 'r') as urls:
        for url in urls:
            url = url.rstrip('\n')
            listaDeDiretorios.append(url)
    urls.close()


#Print result based on status code response
def ExibeResultado(url, statuscode, charset):
    if statuscode >= 200 and statuscode < 300 and str(statuscode) not in listaStatusCode and str(charset) not in listaChars:
        print(f'{url} <-> {ResultColors.OK}{statuscode}{ResultColors.PATTERN} Chars: {charset}\n', flush=True)
    elif statuscode >= 300 and statuscode < 399 and str(statuscode) not in listaStatusCode and str(charset) not in listaChars:
        print(f'{url} <-> {ResultColors.REDIRECT}{statuscode}{ResultColors.PATTERN} Chars: {charset}\n', flush=True)
    elif statuscode >= 400 and statuscode < 499 and str(statuscode) not in listaStatusCode and str(charset) not in listaChars:
        print(f'{url} <-> {ResultColors.ERROR}{statuscode}{ResultColors.PATTERN} Chars: {charset}\n', flush=True)
    elif statuscode >= 500 and statuscode < 599 and str(statuscode) not in listaStatusCode and str(charset) not in listaChars:
        print(f'{url} <-> {ResultColors.ServerError}{statuscode}{ResultColors.PATTERN} Chars: {charset}\n', flush=True)


#Make requests through the words extracted from the user file
def FuzzingRequest(Diretorio, urlAttack):
    urlAttack = urlAttack.replace('RECON', Diretorio)
    try:
        response = requests.get(urlAttack)
        ExibeResultado(urlAttack, response.status_code, len(response.text))
    except requests.exceptions.ConnectionError:
        print(f'{urlAttack} <-> Connection refused\n') 


def main():
    timeStart = time()
    queue = Queue()
    ListaDiretorios(filePath)

    for worker in range(30):
        worker = startWorks(queue)
        worker.daemon = True
        worker.start()

    for fuzzlist in listaDeDiretorios:
        queue.put(fuzzlist)

    queue.join()
    timePassed = time()
    print(f'Execution time: {ResultColors.BOLD}{timePassed - timeStart}')


if __name__ == '__main__':
    main()
    
