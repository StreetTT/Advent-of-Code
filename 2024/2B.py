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
    if ascending != None: # Rising/Falling Check, Cannot be checked if no precedent has been set
        if (currLevel < prevLevel and ascending) or (currLevel > prevLevel and not ascending):
            return False, ascending 
    
    diff = prevLevel - currLevel

    if abs(diff) in (1,2,3): # Gradual Difference Check
        if diff > 0:
            if (ascending == None or not ascending):
                return True, False
        elif diff < 0:
            if (ascending == None or ascending):
                return True, True
    return False, ascending

rawData = getInput()
if rawData == None:
    exit(1)

safeMatrix = {}
# My answer is between 506 and 460
rawData = rawData.split("\n")
for reportIndex, report in enumerate(rawData):
    report = report.split(" ")
    report = list(map(lambda x: (int(x)), report))
    rawData[reportIndex] = report
    prevLevelIndex = 0
    currLevelIndex = 1
    safe = True
    dir = None
    unsafeCount = 0
    safeMatrix.update({
        reportIndex: {
            "curr" : -1,
            "prev" : -1,
            "count" : 0
        }
    })
    while currLevelIndex < len(report):
        safe, dir = safetyCheck(report[prevLevelIndex], report[currLevelIndex], dir)
        if not safe:
            unsafeCount += 1
            if unsafeCount == 1:
                safeMatrix[reportIndex].update({
                    "curr" : currLevelIndex,
                    "prev" : prevLevelIndex,
                    "dir": dir,
                    "count" : 1
                })
        currLevelIndex += 1
        prevLevelIndex += 1
    safeMatrix[reportIndex].update({
        "count" : unsafeCount
    })
safeCount = list(map(lambda x: safeMatrix[x]["count"] == 0, safeMatrix)).count(True)
print("First Pass")
print("Safe", safeCount)
print("Unsafe", (len(safeMatrix) - safeCount))

for reportIndex, report in enumerate(rawData):
    if safeMatrix[reportIndex]["count"] not in (1,2):
        continue
    prevLevelIndex = safeMatrix[reportIndex]["prev"]
    currLevelIndex = safeMatrix[reportIndex]["curr"] + 1
    safe = True
    dir = None if prevLevelIndex == 0 else safeMatrix[reportIndex]["dir"]
    unsafeCount = 0
    while currLevelIndex < len(report) and safe:
        safe, dir = safetyCheck(report[prevLevelIndex], report[currLevelIndex], dir)
        if not safe:
            unsafeCount += 1
        currLevelIndex += 1
        prevLevelIndex += 1
        if prevLevelIndex == safeMatrix[reportIndex]["curr"]:
            prevLevelIndex += 1
    safeMatrix[reportIndex].update({"count" : unsafeCount})
safeCount = list(map(lambda x: safeMatrix[x]["count"] == 0, safeMatrix)).count(True)
print("Second Pass")
print("Safe", safeCount)
print("Unsafe", (len(safeMatrix) - safeCount))