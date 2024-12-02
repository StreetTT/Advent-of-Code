import requests
from os.path import exists
from os import getenv
from datetime import datetime

def getInput(test=False):
    day = int((datetime.now()).strftime("%d"))
    year = int((datetime.now()).strftime("%Y"))
    fileName = f"{str(year)}/Day{str(day)}{'Test' if test else ''}Input.txt"
    fileExists = exists(fileName)
    if not (fileExists):
        myToken = getenv('AoC_token')
        url = f"https://adventofcode.com/{str(year)}/day/{str(day)}/input"
        cookies = {"session": myToken}
        headers = {"Cookie": f"session={myToken}"}
        r = requests.get(url, headers=headers, cookies=cookies)
        if r.status_code == 200:
            data = r.text
            f = open(fileName, "w")
            f.write(data[:-1])
            f.close()
        else:
            print("FAILED")
            print(
                f"/api/alerts response: {r.status_code}: {r.reason} \n{r.content}"
            )
            return None
    f = open(fileName, "r")
    data = f.read()
    f.close()
    return data

def safetyCheck(prevLevel, currLevel, ascending):
    if ascending != None:
        if currLevel < prevLevel and ascending:
            return False, None
        elif currLevel > prevLevel and not ascending:
            return False, None 
    
    diff = prevLevel - currLevel

    if diff > 0:
        if (ascending == None or not ascending) and abs(diff) in (1,2,3):
            return True, False
        else:
            return False, None
    elif diff < 0:
        if (ascending == None or ascending) and abs(diff) in (1,2,3):
            return True, True
        else:
            return False, None
    return False, None

rawData = getInput()
if rawData == None:
    exit(1)

safeCount = 0
rawData = rawData.split("\n")
for report in rawData:
    report = report.split(" ")
    report = list(map(lambda x: (int(x)), report))
    dir = None
    for level in range(1, len(report)):
        safe, dir = safetyCheck(report[level-1], report[level], dir)
        if not safe:
            break
    if safe:
        safeCount += 1
print(safeCount)