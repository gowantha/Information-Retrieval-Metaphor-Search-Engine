import os
import json
from datetime import datetime

# Opening JSON file
json_file = open('F:\#Semester7\CS4642 - Data Mining & Information Retrieval\Information-Retrieval-Metaphor-Search-Engine\corp.json',encoding="utf-8")

# returns JSON object as
# a dictionary
data = json.load(json_file)
with open("songs_csv_with_features_updated.json", "w",encoding="utf-8") as outfile:
    for json_ in data['songs']:
        json.dump(json_, outfile,ensure_ascii=False)
        outfile.write('\n')
json_file.close()