import glob
import json
import os
import re
import yaml


def convert_to_objects(filename):
    #global count
    #count += 1
    #print(count)
    json_file = open(filename, encoding="utf8")
    examples = open(filename.replace('.json', '_usersays_en.json'), encoding="utf8")
    return {**json.loads(json_file.read()), "examples":
        json.loads(examples.read())}


intents_path = os.path.join(os.getcwd(), 'intents')

# Ignore filenames for user examples
files = set(glob.glob(f'{intents_path}/*')) - set(glob.glob(f'{intents_path}/*usersays*'))
objects = list(map(convert_to_objects, files))
varasd = 0

global reponsedic
responsedic = {"beging": "1"}

global count
count = 0

for obj in objects:
    print(count)
    count += 1
    name = obj['name'].replace('_', '')
    name = name.replace('-', '')
    name = name.replace('.', '')
    name = "utter_" + name
    response = obj['responses'][0]['messages'][0]['speech']
    dict = {name: response}
    responsedic.update(dict)


with open(r'file.yaml', 'w') as file:
    for i in responsedic:
        file.write("  "+ i + ":" + "\n    - "+ "text: \"" + str(responsedic[i]) + "\"\n" )
    file.close()





varasd=1
