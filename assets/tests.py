import schedule
import time
import datetime

def test_function():
    now = datetime.datetime.now()
    print("test code- 현재 시간 출력하기")
    print(now)

# 1초마다 test_function을 동작시키자
schedule.every(0.5).seconds.do(test_function)

# 무한 루프를 돌면서 스케쥴을 유지한다.
while True:
    schedule.run_pending()
    time.sleep(1)