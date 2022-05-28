from datetime import datetime, timedelta

class subtitleComparison:

    class otherErrors(Exception):
        def __init__(self, cause, message):
            self.cause = cause
            self.message = message
        def __str__(self):
            return self.cause + ': ' + self.message

    def __init__(self, primaryFile, referenceFile):
        self.primaryFile = primaryFile
        self.referenceFile = referenceFile
        self.subtitleDict = {}

    def get_recordTime_and_content(self, str):
        # 從字串中取出字幕時間，並包成datetime格式回傳
        return datetime.strptime(str[0:8], '%H:%M:%S'), str[8:]

    def get_recordTime_delta_list(self, time, deltaSecond):
        result = []
        for deltaSecond in range(-deltaSecond, deltaSecond):
            result.append(time + timedelta(seconds=deltaSecond))
        return result

    def read_file(self, fileName):
        result = []
        try:
            with open(fileName, encoding='utf8') as f:
                for line in f.readlines():
                    line = line[:-1]  # 字串後發有換行符號"\n" -> 需去除
                    result.append(line)
        except FileNotFoundError:
            print(f'Can not find file {fileName}')
        return result

    def update_subtitle_dictionary(self, subtilteFile):
        for line in subtilteFile:
            recordTime, content = self.get_recordTime_and_content(str=line)
            self.subtitleDict.update({recordTime: content})  # 打開我的並且記錄成dict

    def execute_comparispon(self):
        referenceFileResult = self.read_file(fileName=self.referenceFile)
        count = 0
        for time in self.subtitleDict:
            flag = 0  #用於指出讀取時間是否有落在指定時間區間內
            for line in referenceFileResult:
                recordTime = self.get_recordTime_and_content(line)[0]
                # 確認讀取時間是否有落在指定時間區間內
                timeDeltaList = self.get_recordTime_delta_list(time=recordTime, deltaSecond=2)
                if time in timeDeltaList:
                    flag = 1
                    break
            if flag == 0:
                print(f"{datetime.strftime(time, '%H:%M:%S')} *{self.subtitleDict[time]}")
                count += 1
        print(f"共找到 {count} 個不同處")

    def main(self):
        result = self.read_file(fileName=self.primaryFile)
        self.update_subtitle_dictionary(subtilteFile=result)
        self.execute_comparispon()

if __name__ == '__main__':
    file1 = '1006 文字檔.txt' #雅風的
    file2 = '張老師美國ITS趨勢(第二場).txt'  #我的
    subtitleComparison = subtitleComparison(primaryFile=file2, referenceFile=file1)  # 建立物件
    subtitleComparison.main()