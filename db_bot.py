import json
from openai import OpenAI
import os
import sqlite3
from time import time

print('Running db_bot.py...')

fdir = os.path.dirname(__file__)
def getPath(fname):
    return os.path.join(fdir, fname)

# SQLITE -----------------------------
sqliteDbPath = getPath("aidb.sqlite")
setupSqlPath = getPath("setup.sql")
setupSqlDataPath = getPath("setupData.sql")

# Erase previous db
if os.path.exists(sqliteDbPath):
    os.remove(sqliteDbPath) 

sqliteCon = sqlite3.connect(sqliteDbPath) # create new db
sqliteCursor = sqliteCon.cursor()
with (
        open(setupSqlPath) as setupSqlFile,
        open(setupSqlDataPath) as setupSqlDataFile
    ):

    setupSqlScript = setupSqlFile.read()
    setupSQlDataScript = setupSqlDataFile.read()

sqliteCursor.executescript(setupSqlScript) # set up tables and keys
sqliteCursor.executescript(setupSQlDataScript) # set up tables and keys

def runSql(query):
    result = sqliteCursor.execute(query).fetchall()
    return result

# OPENAI ------------------------------
configPath = getPath("config.json")
print(configPath)
with open(configPath) as configFile:
    config = json.load(configFile)

openAiClient = OpenAI(
    api_key = config["openaiKey"],
    organization = config["orgId"]
)

def getChatGptResponse(content):
    stream = openAiClient.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": content}],
        stream=True,
    )

    responseList = []
    for chunk in stream:
        if chunk.choices[0].delta.content is not None:
            responseList.append(chunk.choices[0].delta.content)

    result = "".join(responseList)
    return result

def sanitizeForJustSql(value):
    gptStartSqlMarker = "```sql"
    gptEndSqlMarker = "```"
    if gptStartSqlMarker in value:
        value = value.split(gptStartSqlMarker)[1]
    if gptEndSqlMarker in value:
        value = value.split(gptEndSqlMarker)[0]

    return value

# QUESTIONS -----------------------------------
questions = [
    "Which buildings have gluten free items?",
    "Can you pick a random soy free snack and tell me where to find it?",
    "Which building has the most vending machines?",
    "Which vending machine items meet all dietary restrictions?",
    "Can you give me a list of all the items in a random vending machine?",
    "Can you give me the location of the vending machine with the most items in stock?",
    "What are all the low dairy items available?",
    "I am allergic to nuts and my friend has Celiac Disease. Can you tell us where a vending machine is with snacks both of us can eat?"
]


# STRATEGIES -----------------------------------
commonSqlOnlyRequest = "Writing in SQlite, give a select statement that answers the question. Please only give the select statement and do not say anything else."
strategies = {
    "zero_shot": setupSqlScript + commonSqlOnlyRequest,
    "single_domain_double_shot": (setupSqlScript + 
                   " Can you give me a list of all the nut free snacks? " + 
                   " \nSELECT Name\nFROM VendingItem\nWHERE IsNutFree = 1;" +
                   commonSqlOnlyRequest)
}

# RUN AND OUTPUT -----------------------------------
for strategy in strategies:
    responses = {"strategy": strategy, "prompt_prefix": strategies[strategy]}
    questionResults = []
    for question in questions:
        print(question)
        error = "None"
        try:
            sqlSyntaxResponse = getChatGptResponse(strategies[strategy] + " " + question)
            sqlSyntaxResponse = sanitizeForJustSql(sqlSyntaxResponse)
            print(sqlSyntaxResponse)
            queryRawResponse = str(runSql(sqlSyntaxResponse))
            print(queryRawResponse)
            friendlyResultsPrompt = "I asked a question \"" + question +"\" and the response was \""+queryRawResponse+"\" Please, just give a concise response in a more friendly way? Please do not give any other suggests or chatter."
            friendlyResponse = getChatGptResponse(friendlyResultsPrompt)
            print(friendlyResponse)
        except Exception as err:
            error = str(err)
            print(err)

        questionResults.append({
            "question": question, 
            "sql": sqlSyntaxResponse, 
            "queryRawResponse": queryRawResponse,
            "friendlyResponse": friendlyResponse,
            "error": error
        })

    responses["questionResults"] = questionResults

    with open(getPath(f"response_{strategy}_{time()}.json"), "w") as outFile:
        json.dump(responses, outFile, indent = 2)


sqliteCursor.close()
sqliteCon.close()
print("Done!")