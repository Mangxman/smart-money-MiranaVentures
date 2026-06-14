import schedule
import time

def job():

    print("scan smart money")

schedule.every(1).minutes.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)