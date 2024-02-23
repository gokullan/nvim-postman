import json

def toKebab(string):
    words = "".join(string.lower().split("-")).split(" ")
    words = [w for w in words if w]
    return "-".join(words)

def toCamelCase(string):
    camelCap = "".join([w.capitalize() for w in string.lower().split("-")])
    return camelCap[0].lower() + camelCap[1:]

def writeToFile(data):
    with open(data["filename"] + ".sh", "w") as curlFile:
        curlFile.writelines([
            f"curl --location --request {data['method']} \\\n",
            f"\"{data['url']}\" \\\n",
        ])
        curlHeaders = [f"--header \"{header}:${toCamelCase(header)}\" \\\n" 
                       for header in data["headers"]]
        curlFile.writelines(curlHeaders)
        if data["method"] != 'GET':
            curlFile.write(f"--data '{data['body']}'")

def parseContents(data):
    items = data["item"]
    for item in items:
        # handling folders inside a collection
        if "item" in item:
            parseContents(item)
        else:
            fileData = {
                "filename": "./partner-api/" + toKebab(item["name"]),
                "method": item["request"]["method"],
                "url": item["request"]["url"]["raw"],
                "headers": [header["key"] for header in item["request"]["header"]]
            }
            if fileData["method"] != 'GET':
                fileData["body"] = item["request"]["body"]["raw"]
            print(fileData["filename"])
            writeToFile(fileData)

def parse():
    # try:
    if 1:
        jsonFileName = "/home/d2c-gokulas/Postman/DTC-PostOrderProcessing Copy.postman_collection.json"
        jsonfileHandler = open(jsonFileName)
        jsonData = json.load(jsonfileHandler)
        parseContents(jsonData)
        jsonfileHandler.close()
    # except Exception as err:
    #    print(err)

if __name__ == "__main__":
    parse()
