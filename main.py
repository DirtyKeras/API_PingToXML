# main.py
from multiprocessing import Process
import time
import os

def run_flask():
    os.system('python scripts/endPoints.py')

def run_monitoring():
    os.system('python scripts/pingToAnyIP.py')

if __name__ == '__main__':
    flask_process = Process(target=run_flask)
    monitoring_process = Process(target=run_monitoring)

    flask_process.start()
    monitoring_process.start()

    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping processes...")
        flask_process.terminate()
        monitoring_process.terminate()
