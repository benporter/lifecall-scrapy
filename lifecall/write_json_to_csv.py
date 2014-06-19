import json
import re
import csv

f = csv.writer(open("addresses.csv", "wb+"))
f.writerow(["state", "url", "address"])

with open("scraped_data.json") as json_file:
    json_data = json.load(json_file)
    for j in json_data:
        try: 
            temp_state = j['state'][0]
        except:
            temp_state = "Missing State"
        for t in j['fulltext']:
            f.writerow([temp_state,
                j['url'],
                re.sub('\s+',' ',t.encode('utf-8'))]) 
                
