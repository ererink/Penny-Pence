import schedule, time

def 함수():

    print('아자자')

def 함수2():
    print('우루루')

schedule.every(1).seconds.do(함수)
schedule.every(2).seconds.do(함수2)
cnt = 0
while True:
    schedule.run_pending()
    cnt += 1
    if cnt > 5:
        schedule.cancel_job(함수)