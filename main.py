import threading
import time

import utils.libs.messageHUB as messageHUB

import server
import app

if __name__ == '__main__' :
    threadMain = threading.Thread(target=app.main)
    threadServer = threading.Thread(target=server.startServer)

    threadServer.start()
    time.sleep(3)
    threadMain.start()