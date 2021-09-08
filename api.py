import requests

classes = ["beast", "plant", "bug", "mech", "dusk", "aquatic", "bird", "reptile", "dawn"]
stats = ["health", "speed", "skill", "morale"]

axie_brief_list = {
  "operationName": "GetAxieBriefList",
  "variables": {
    "from": 0,
    "size": 24,
    "sort": "PriceAsc",
    "auctionType": "Sale",
    "criteria": {}
  },
  "query": "query GetAxieBriefList($auctionType: AuctionType, $criteria: AxieSearchCriteria, $from: Int, $sort: SortBy, $size: Int, $owner: String) {\n  axies(auctionType: $auctionType, criteria: $criteria, from: $from, sort: $sort, size: $size, owner: $owner) {\n    total\n    results {\n      ...AxieBrief\n      __typename\n    }\n    __typename\n  }\n}\n\nfragment AxieBrief on Axie {\n  id\n  name\n  stage\n  class\n  breedCount\n  image\n  title\n  battleInfo {\n    banned\n    __typename\n  }\n  auction {\n    currentPrice\n    currentPriceUSD\n    __typename\n  }\n  parts {\n    id\n    name\n    class\n    type\n    specialGenes\n    __typename\n  }\n  __typename\n}\n"
}

def get_query(query_name, query_list):
  if (query_name == "axie_brief_list"):
    criteria = {}

    for i in query_list:
      for j in range(len(i)):
        if (i[j] in stats):
          if (i[j] == "health"):
            criteria['hp'] = [i[j + 1], i[j + 2]]
          else:
            criteria[i[j]] = [i[j + 1], i[j + 2]]
          continue

        if (i[j] == "class"):
          criteria['classes'] = [i[j+1][0].upper() + i[j+1][1:]]
          continue

        if (i[j] == "part"):
          criteria['parts'] = i[j + 1]
          continue

    query = axie_brief_list
    query["variables"]["criteria"] = criteria
    r = requests.post('https://axieinfinity.com/graphql-server-v2/graphql', json = query)

    return r

def retrieve_axies_list(response):
  axies_list = []
  if response:
    axies_list.extend(response.json()['data']['axies']['results'])

  return axies_list

def get_cheapest(axies_list, skipped_axies):
  cheapest = [0, 100000]

  for i in axies_list:
    if (i["battleInfo"]["banned"] == False):
      if (float(i["auction"]["currentPriceUSD"]) <= cheapest[1]):
        if (not i["id"] in skipped_axies):
          cheapest[1] = float(i["auction"]["currentPriceUSD"])
          cheapest[0] = i["id"]
  
  return cheapest

def get_price_min(query):
  for i in range(len(query)):
    for j in query[i]:
      if (j == "price"):
        return float(query[i][1])

def axies_total(response):
  return response.json()['data']['axies']['total']

def remove_query(query):
  while (True):
    counter = 0

    print("")

    for i in query:
      print(str(counter) + ". " + str(query[counter]))
      counter = counter + 1

    answer = int(input("Input: "))
    if (answer >= 0 and answer < len(query)):
      print("Removed query at position ", str(answer))
      query.pop(answer)

      return query
