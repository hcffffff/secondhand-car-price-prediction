import json

with open("115928025.json",'r') as load_f:
    load_dict = json.load(load_f)
    print(load_dict['dataRough'])