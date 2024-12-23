"""
Documentation:
https://docs.kraken.com/api/docs/rest-api/get-asset-info
"""
import requests

url = "https://api.kraken.com/0/public/Assets"

payload = {}
headers = {
  'Accept': 'application/json'
}

source_data = requests.request("GET", url, headers=headers, data=payload)

# print(type(source_data.json()), "\n")
# print(source_data.json(), "\n")


url = "https://api.kraken.com/0/public/Ticker"
data = requests.request("GET", url, headers=headers, data=payload)
tckerExists = False

#check to see if ticker is accesible by the database
while tckerExists == False:
  #ticker of coin we're looking for
  tcker = input ("Enter Ticker Symbol : ")
  try: 
      tcker_data = data.json()["result"][tcker]
      tckerExists = True
  except:
      print("That ticker symbol does not exist.")
      print("Did you mean any of these?")
      #sql stuff here
      #TODO: WHERE tcker is in the name
      #CHECK: From the original database, tcker:BTC should cover TBTCUSD, TBTCXBT, TBTCEUR, WBTCEUR, WBTCUSD, WBTCXBT, WBTCXBT




print("Searching for " + "'" + tcker + "'")

#print(tcker_data)

print("Ask price since API pull is: ", tcker_data['a'][0])
print("Bid price since API pull is: ", tcker_data['b'][0])
print("Last trade closed is: ", tcker_data['c'][0])
print("WVAP based on one day is: ", tcker_data['p'][0])
print("Number of trades within the last 24 hours is: ", tcker_data['t'][1])


print("Day low is:  ", tcker_data['l'][0])
print("Day high is: ", tcker_data['h'][0])
print("Day opening is : ", tcker_data['o'])