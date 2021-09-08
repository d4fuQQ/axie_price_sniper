import requests

classes = ["beast", "plant", "bug", "mech", "dusk", "aquatic", "bird", "reptile", "dawn"]
stats = ["hp", "speed", "skill", "morale"]

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

def get_axie_brief_list(query_list):
  criteria = {}
  has_price = 0

  for i in range(len(query_list)):
    for j in range(len(query_list[i])):
      # Class
      if (query_list[i][j] == 'class'):
        criteria['classes'] = [query_list[i][j+1][0].upper() + query_list[i][j+1][1:]]
        #print("Class: {0}".format(query_list[i][j+1]))
      # Stats
      elif (query_list[i][j] in stats):
        criteria[query_list[i][j]] = [query_list[i][j+1], query_list[i][j+2]]
        #print("{0}: {1}-{2}".format(query_list[i][j], query_list[i][j+1], query_list[i][j+2]))
      # Parts list
      elif (query_list[i][j] == 'part'):
        criteria['parts'] = query_list[i][j+1]
        #print(query_list[i][j+1])
      elif (query_list[i][j] == 'price'):
        has_price = 1

  if (has_price == 0):
    print("Alert: no min price at the query: {0}".format(query_list))

  query = axie_brief_list
  query["variables"]["criteria"] = criteria
  r = requests.post('https://graphql-gateway.axieinfinity.com/graphql', json = query)

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
