lineList = []
with open('張老師美國ITS趨勢(第一場).txt', encoding='utf8') as f:
    for line in f.readlines():
        #line = line[:-1]
        lineList.append(line)

with open('cddd.txt', 'w', encoding='utf8') as f:
    for line in lineList:
        f.write('00:' + line)