import csv
from collections import deque


# IT 섹터
IT_average = [0] * 40
IT_AVG = []
IT_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\IT\\네이버 주가(10년).csv", "C:\\Users\\이명학\\Desktop\\주가 10년\\IT\\다우기술 주가(10년).csv", "C:\\Users\\이명학\\Desktop\\주가 10년\\IT\\카카오 주가(10년).csv"])

while IT_address:
    with open(IT_address.popleft(), 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        column_index = header.index('percent')
        column_data = []
        for row in reader:
            column_data.append(row[column_index])
        new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거
        # print(new_column_data)
        new_column_data.pop() # 마지막 요소 제거
        # print(len(new_column_data))
        # print(new_column_data)
        re_number = 0
        # print(len(new_column_data))
        for i in range(len(new_column_data)):
            number = new_column_data.popleft()
            IT_average[i] += float(number)
            # print(number)

for i in IT_average:
    num = round(i/3, 2)
    IT_AVG.append(num)
print(IT_AVG)

# Game 섹터
game_average = [0] * 40
game_AVG = []
game_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\게임\\엔씨소프트 주가(10년).csv", "C:\\Users\\이명학\\Desktop\\주가 10년\\게임\\위메이드 주가(10년).csv", "C:\\Users\\이명학\\Desktop\\주가 10년\\게임\\컴투스 주가(10년).csv"])

while game_address:
    with open(game_address.popleft(), 'r') as f:
        reader = csv.reader(f)
        header = next(reader)
        column_index = header.index('percent')
        column_data = []
        for row in reader:
            column_data.append(row[column_index])
        new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거
        # print(new_column_data)
        new_column_data.pop() # 마지막 요소 제거
        # print(len(new_column_data))
        # print(new_column_data)
        re_number = 0
        # print(len(new_column_data))
        for i in range(len(new_column_data)):
            number = new_column_data.popleft()
            game_average[i] += float(number)
            # print(number)

for i in game_average:
    num = round(i/3, 2)
    game_AVG.append(num)
print(game_AVG)