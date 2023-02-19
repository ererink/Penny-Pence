import csv
from collections import deque


# IT 섹터
def it_sector():
    it_average = [0] * 40
    it_AVG = deque()

    # import 에러 방지용 주석처리
    # it_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\IT\\네이버 주가(10년).csv",
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\IT\\다우기술 주가(10년).csv", 
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\IT\\카카오 주가(10년).csv"])

    # while it_address:
    #     with open(it_address.popleft(), 'r') as f:
    #         reader = csv.reader(f)
    #         header = next(reader)
    #         column_index = header.index('percent')
    #         column_data = []
    #         for row in reader:
    #             column_data.append(row[column_index])
    #         new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거

    #         for i in range(len(new_column_data)):
    #             number = new_column_data.popleft()
    #             it_average[i] += float(number)
  
    for i in it_average:
        num = round(i/3, 2)
        it_AVG.append(num)
    print(it_AVG)
    return it_AVG

# Game 섹터
def game_sector():
    game_average = [0] * 40
    game_AVG = deque()

    # import 에러 방지용 주석처리
    # game_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\게임\\엔씨소프트 주가(10년).csv",
    #                       "C:\\Users\\이명학\\Desktop\\주가 10년\\게임\\위메이드 주가(10년).csv", 
    #                       "C:\\Users\\이명학\\Desktop\\주가 10년\\게임\\컴투스 주가(10년).csv"])

    # while game_address:
    #     with open(game_address.popleft(), 'r') as f:
    #         reader = csv.reader(f)
    #         header = next(reader)
    #         column_index = header.index('percent')
    #         column_data = []
    #         for row in reader:
    #             column_data.append(row[column_index])
    #         new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거

    #         for i in range(len(new_column_data)):
    #             number = new_column_data.popleft()
    #             game_average[i] += float(number)

    for i in game_average:
        num = round(i/3, 2)
        game_AVG.append(num)
    print(game_AVG)
    return game_AVG



# Bio 섹터
def bio_sector():
    bio_average = [0] * 40
    bio_AVG = deque()

    # import 에러 방지용 주석처리
    # bio_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\바이오\\셀트리온 주가(10년).csv", 
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\바이오\\신풍제약 주가(10년).csv",
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\바이오\\유한양행 주가(10년).csv"])

    # while bio_address:
    #     with open(bio_address.popleft(), 'r') as f:
    #         reader = csv.reader(f)
    #         header = next(reader)
    #         column_index = header.index('percent')
    #         column_data = []
    #         for row in reader:
    #             column_data.append(row[column_index])
    #         new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거

    #         for i in range(len(new_column_data)):
    #             number = new_column_data.popleft()
    #             bio_average[i] += float(number)

    for i in bio_average:
        num = round(i/3, 2)
        bio_AVG.append(num)
    print(bio_AVG)
    return bio_AVG



# 반도체 섹터
def sc_sector():
    sc_average = [0] * 40
    sc_AVG = deque()

    # import 에러 방지용 주석처리
    # sc_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\반도체\\LG디스플레이 주가(10년).csv", 
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\반도체\\삼성전자 주가(10년).csv",
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\반도체\\삼성전자 주가(10년).csv"])

    # while sc_address:
    #     with open(sc_address.popleft(), 'r') as f:
    #         reader = csv.reader(f)
    #         header = next(reader)
    #         column_index = header.index('percent')
    #         column_data = []
    #         for row in reader:
    #             column_data.append(row[column_index])
    #         new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거

    #         for i in range(len(new_column_data)):
    #             number = new_column_data.popleft()
    #             sc_average[i] += float(number)

    for i in sc_average:
        num = round(i/3, 2)
        sc_AVG.append(num)
    print(sc_AVG)
    return sc_AVG


# 엔터테인먼트 섹터
def enter_sector():
    enter_average = [0] * 40
    enter_AVG = deque()

    # import 에러 방지용 주석처리
    # enter_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\엔터\\JPY 주가(10년).csv", 
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\엔터\\SM 주가(10년).csv",
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\엔터\\YG플러스 주가(10년).csv"])

    # while enter_address:
    #     with open(enter_address.popleft(), 'r') as f:
    #         reader = csv.reader(f)
    #         header = next(reader)
    #         column_index = header.index('percent')
    #         column_data = []
    #         for row in reader:
    #             column_data.append(row[column_index])
    #         new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거

    #         for i in range(len(new_column_data)):
    #             number = new_column_data.popleft()
    #             enter_average[i] += float(number)

    for i in enter_average:
        num = round(i/3, 2)
        enter_AVG.append(num)
    print(enter_AVG)
    return enter_AVG


# 자동차 섹터
def automobile_sector():
    automobile_average = [0] * 40
    automobile_AVG = deque()

    # import 에러 방지용 주석처리
    # automobile_address = deque(["C:\\Users\\이명학\\Desktop\\주가 10년\\자동차\\기아차 주가(10년).csv", 
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\자동차\\현대모비스 주가(10년).csv",
    #                     "C:\\Users\\이명학\\Desktop\\주가 10년\\자동차\\현대차 주가(10년).csv"])

    # while automobile_address:
    #     with open(automobile_address.popleft(), 'r') as f:
    #         reader = csv.reader(f)
    #         header = next(reader)
    #         column_index = header.index('percent')
    #         column_data = []
    #         for row in reader:
    #             column_data.append(row[column_index])
    #         new_column_data = deque(list(filter(None, column_data))) # 빈 열 제거

    #         for i in range(len(new_column_data)):
    #             number = new_column_data.popleft()
    #             automobile_average[i] += float(number)

    for i in automobile_average:
        num = round(i/3, 2)
        automobile_AVG.append(num)
    print(automobile_AVG)
    return automobile_AVG


if __name__ == "__main__":
    it_sector()
    game_sector()
    bio_sector()
    sc_sector()
    enter_sector()
    automobile_sector()