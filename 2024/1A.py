import requests
from os.path import exists
from os import getenv
from datetime import datetime

def getInput(test=False):
    day = 1 #int((datetime.now()).strftime("%d"))
    year = 2024 #int((datetime.now()).strftime("%Y"))
    fileExists = exists(f"{str(year)}/Day{str(day)}Input.txt")
    if not (fileExists):
        myToken = getenv('AoC_token')
        url = f"https://adventofcode.com/{str(year)}/day/{str(day)}/input"
        cookies = {"session": myToken}
        headers = {"Cookie": f"session={myToken}"}
        r = requests.get(url, headers=headers, cookies=cookies)
        if r.status_code == 200:
            data = r.text
            f = open(f"{str(year)}/Day{str(day)}Input.txt", "w")
            f.write(data[:-1])
            f.close()
        else:
            print("FAILED")
            print(
                f"/api/alerts response: {r.status_code}: {r.reason} \n{r.content}"
            )
            return None
    if test:
        f = open(f"{str(year)}/Day{str(day)}TestInput.txt", "r")
    else:
        f = open(f"{str(year)}/Day{str(day)}Input.txt", "r")
    data = f.read()
    f.close()
    return data

rawData = getInput()
if rawData == None:
    exit(1)
rawData = rawData.split("\n")
left = []
right = []
for i in rawData:
    i = i.split("   ")
    left.append(int(i[0]))
    right.append(int(i[1]))
left.sort()
right.sort()
sum = 0
for i in range(len(left)):
    sum += abs(left[i] - right[i])
print(sum)