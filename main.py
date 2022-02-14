import csv

storyNodes = {}
nextNodes = {}

# load and process storyNodes
with open('storyData/storyNodes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        storyNodes[row["node_ID"]] = {
            "output": row["output"],
            "user_input_needed": row["user_input_needed"],
            "next_node_ID": row["next_node_ID"]
        }
        line_count += 1

# load and process nextNodes
with open('storyData/nextNodes.csv', mode='r') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            line_count += 1
        
        if (row["node_ID"] not in nextNodes):
            nextNodes[row["node_ID"]] = {
                row["resp_option"]: row["next_node_ID"]
            }
        else:
            nextNodes[row["node_ID"]].update({
                row["resp_option"]: row["next_node_ID"]
            })    
        
        line_count += 1