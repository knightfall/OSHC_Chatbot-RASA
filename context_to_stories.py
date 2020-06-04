import glob
import json
import os

global count
count = 0


# Function to convert JSON string from file to
def convert_to_objects(filename):
    global count
    count += 1
    print(count)
    json_file = open(filename, encoding="utf8")
    examples = open(filename.replace('.json', '_usersays_en.json'), encoding="utf8")
    return {**json.loads(json_file.read()), "examples":
        json.loads(examples.read())}


# Get all json files
intents_path = os.path.join(os.getcwd(), 'data', 'dflow', 'intents')

# Ignore filenames for user examples
files = set(glob.glob(f'{intents_path}/*')) - set(glob.glob(f'{intents_path}/*usersays*'))
objects = list(map(convert_to_objects, files))

import networkx as nx

G = nx.DiGraph()

for obj in objects:
    G.add_node(obj['name'], **obj)

for obj in objects:
    if obj['responses']:
        for r in obj['responses']:
            for ctx in r['affectedContexts']:
                out_ctx = ctx['name']
                G.add_edge(obj['name'], out_ctx)

import matplotlib.pyplot as plt

#for line in nx.generate_adjlist(G):
    #print(line)
# write edgelist to grid.edgelist
nx.write_edgelist(G, path="grid.edgelist", delimiter=":")
# read edgelist from grid.edgelist
H = nx.read_edgelist(path="grid.edgelist", delimiter=":")

nx.draw(H)
plt.show()
# Collect all possible paths from top to bottom
for path in nx.all_simple_paths(G, source='DWI', target='Bye'):
    print(path)

paths_list = list(nx.all_simple_paths(G, source='DWI', target='Bye'))

global story_texts

for i, paths in enumerate(paths_list):
    story_text = ''
    story_text += f'## story_{i}\n'

    for edge in paths:
        story_text += f'* {edge[0]} \n -  {edge[1]} \n'
    story_texts.append(story_text)
    # Store the data in file
open('stories.md', 'w').write('\n'.join(story_texts))
