import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import api
import time
import webbrowser
from pygame import mixer

def parse_add(query):
    queryp = []
    ret = 0
    part_name = 0
    query = query.split()
    has_price = 0

    query.pop(0)

    for i in range(len(query)):
        if (query[i][0] == "-"):
            # If class query (-class)
            if (query[i] == "-class"):
                if (query[i+1] in api.classes):
                    queryp.append(["class", query[i+1]])
                    continue

            # If stat query (-hp, -speed, -skill, -morale)
            if (query[i][1:] in api.stats):
                if (int(query[i+1]) and int(query[i+2])):
                    if int(query[i+1]) <= int(query[i+2]):
                        if int(query[i+1]) >= 27 and int(query[i+2]) <= 61:
                            queryp.append([query[i][1:], int(query[i+1]), int(query[i+2])])
                            continue

            # If part query (-part)
            if (query[i] == "-part"):
                part_list = []
                for j in range(i+1, len(query)):
                    if (query[j][0] == "-"):
                        break

                    part_list.append(query[j].replace('\'', '').replace('[', '').replace(']', '').replace(',', ''))
                queryp.append(["part", part_list])

            # If price query
            if (query[i] == "-price"):
                if (query[i+1]):
                    if (float(query[i+1])):
                        queryp.append(["price", float(query[i+1])])
                        has_price = 1
                        continue

    if (not queryp or has_price == 0):
        print("Empty query. Did you type it right?")
        return -1
    else:
        return queryp

def savetofile(queries):
    f = open("config.txt", "w")
    f.write("")
    f.close()

    f = open("config.txt", "a")
    for i in queries:
        line = ""
        for j in i:
            for k in j:
                word = str(k)
                if (word == "part" or word == "class" or word == "price" or word in api.stats):
                    word = "-" + word
                word.replace(',', '')
                word.replace('\"', '')
                word.replace('[', '')
                word.replace(']', '')
                line = line + word + " "
        f.write(line[:-1] + "\n")
    f.close()

    print("")
    print("Saved to config.txt")
    print("")

def loadfromfile():
    queries = []
    f = open("config.txt", "r")
    print("")
    for i in f.readlines():
        parsed_query = parse_add("add " + i)
        if (parsed_query != -1):
            print("Query added: ", end="")
            print(parsed_query)
            print("")
            queries.append(parsed_query)

    print("Loaded successfully")
    print("")
    return queries

def start(queries):
    mixer.init()
    mixer.music.load("alarm.mp3")

    skipped_axies = []
    while (True):
        for i in queries:
            response = api.get_axie_brief_list(i)
            axies_list = api.retrieve_axies_list(response)
            
            if not axies_list:
                print("No axie founds for the query: {0}".format(i))
                continue

            cheapest = api.get_cheapest(axies_list, skipped_axies)
            price_target = api.get_price_min(i)
            skipped_axies.append(cheapest[0])

            if (cheapest[1] <= price_target):
                print("")
                print("Cheaper Axie detected!")
                print("Axie ID: " + cheapest[0])
                print("Price: $" + str(cheapest[1]))
                print("Added this axie to the ignore list since it has already been notified.")
                print("###########################################")
                mixer.music.play()
                webbrowser.open('https://marketplace.axieinfinity.com/axie/'+cheapest[0], new=2)

        time.sleep(10)

def main():
    queries = []
    answer = ""

    while (True):
        print("1. add [-class class] [-[stat] 27 61] [-part part-name part-name part-name part-name] [-price value]")
        print("2. show")
        print("3. remove")
        print("4. save")
        print("5. load")
        print("6. help")
        print("7. start")
        answer = input("Input: ")

        if ("add" in answer):
            parsed_query = parse_add(answer)

            if (parsed_query != -1):
                print("")
                print("Query added: ", end="")
                print(parsed_query)
                queries.append(parsed_query)

            print("")
        elif ("show" in answer):
            c = 0
            print("")
            for i in queries:
                print(str(c) + ". ", end="")
                print(i)
                c = c + 1
            print("")
        elif ("remove" in answer):
            queries = api.remove_query(queries)
            print("")
        elif ("save" in answer):
            savetofile(queries)
        elif ("load" in answer):
            queries = loadfromfile()
        elif ("help" in answer):
            print("Example: add class beast speed 57-61 part piercing-sound price 0.25")
            print("")
        elif ("start" in answer):
            break

    start(queries)

if __name__ == "__main__":
    main()
