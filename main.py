"""
main.py

Main.py é responsável por iniciar o processo o programa completamente, através de duas threads, uma para manter o
servidor de aplicação via flask para poder receber requisições e comunicar com o cliente, seus processos estão
detalhados em server.py e outra thread para manter o fluxo da aplicação, baseado no processo descrito em app.py.
Entre a inicialização de uma thread e outra, foi alocado um tempo de 3s de espera para que haja tempo hábil do
servidor de aplicação ativar seus serviços antes do restante do processo começar a enviar requisições.

Para casos onde for iniciado através de uma máquina diferente de um raspberry pi, é necessário inserir uma variável
de ambiente ENV_TYPE=DEV, para que as bilbiotecas exclusivas do microcomputador não sejam carregadas e causem erros
de importação, podendo ser então iniciado e testado em outros tipos de computadores e sistemas operacionais em geral.

"""


import threading
import time

import server
import app

if __name__ == '__main__' :
    threadMain = threading.Thread(target=app.main)
    threadServer = threading.Thread(target=server.startServer)

    threadServer.start()
    time.sleep(3)
    threadMain.start()