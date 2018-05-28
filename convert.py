import csv
from os import listdir
from os.path import isfile, join
import os
import sys
import json
from collections import defaultdict


def json_to_csv(file):
    with open('Input/'+file, 'r', encoding='utf-8') as f:
        json_f = json.load(f)

    with open('Output/answers.csv', 'w+', encoding='utf-8', newline='') as csvfile:
        fieldnames = ['Label', 'Original_Message', 'Final_Message', 'Comments']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for header, text in json_f.items():
            # Reduction condition 1 (value is nested list)
            if type(text) is list:
                # write the first row
                writer.writerow({'Label': header, 'Original_Message': text[0].replace('\n', '\\n')})
                # rest of the items in separate rows
                for sub_item in text[1:]:
                    writer.writerow({'Original_Message': sub_item.replace('\n', '\\n')})
            # Reduction condition default
            else:
                writer.writerow({'Label': header, 'Original_Message': text.replace('\n', '\\n')})


def csv_to_json(file):
    with open('Input/'+file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        answer_dict = defaultdict(lambda: [])  # dictionary to save to json

        prev_label = ''  # used to hold the value of previous label for lists
        for row in reader:
            label = row['Label'] if row['Label'] != '' else prev_label
            answer_dict[label].append(
                row['Final_Message'] if row['Final_Message'] != '' else row['Original_Message']
            )
            prev_label = label

        for k, v in answer_dict.items():
            if len(v) == 1:
                answer_dict[k] = v[0]

        with open('Output/answers.json', 'w+', encoding='utf-8') as json_f:
            json.dump(answer_dict, json_f, indent=4)


for directory in ['./Input', './Output']:
    if not os.path.exists(directory):
        os.makedirs(directory)

input_files = [f for f in listdir("./Input") if isfile(join("./Input", f))]
if len(input_files) != 1:
    print("Put only one file in Input folder ")
    sys.exit()
else:
    input_file = input_files[0]

extension = os.path.splitext(input_file)[1]
if extension == '.json':
    json_to_csv(input_file)
elif extension == '.csv':
    csv_to_json(input_file)
else:
    print("The input file must be json or csv")
    sys.exit()
