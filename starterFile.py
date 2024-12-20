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

rawData = getInput()
if rawData == None:
    exit(1)
    