import json
import os
# from nltk.tree import Tree
# from stanfordcorenlp import StanfordCoreNLP
from functools import reduce

# nlp = StanfordCoreNLP(r'./stanford-corenlp-full-2018-02-27')

# def constituency_parse(sentence):
#     # Perform constituency parsing using Stanford CoreNLP
#     parse_tree = nlp.parse(sentence)
    
#     # Convert the parse tree string to an NLTK Tree object
#     tree = Tree.fromstring(parse_tree)
#     print(tree)
    
#     return tree

# def convert_to_binary_parse(tree):
#     # Convert a constituency parse tree to a binary parse tree
#     if isinstance(tree, str):
#         # Base case: leaf node (word)
#         return tree
#     elif len(tree) == 1:
#         # Unary production: only one child
#         return convert_to_binary_parse(tree[0])
#     else:
#         # Binary production: two children
#         left_child = convert_to_binary_parse(tree[0])
#         right_child = convert_to_binary_parse(tree[1])
#         return f"({left_child} {right_child})"

def collect_data(data):
    data_expanded = []
    for _id, value in data.items():
        temp = {}
        temp["id"] = _id
        sec_id = value.get("Secondary_id")
        temp["section_id"] = value["Section_id"]
        temp["statement"] = value["Statement"]
        temp["primary_id"] = value["Primary_id"]
        temp["label"] = value["Label"]
        if sec_id is not None:
            temp["secondary_id"] = sec_id

        data_expanded.append(temp)
    
    CT_files = os.listdir("../training-data/CT_json")
    if ".DS_Store" in CT_files:
        CT_files.remove(".DS_Store")
    CT_files_data = {}
    for file in CT_files:
        path = f"../training-data/CT_json/{file}".encode('latin-1')
        path = path.decode('utf-8')
        content = json.load(open(path))
        CT_files_data[file[:-5]] = content

    samples = []
    for sample in data_expanded:
        primary_evidence = ", ".join(CT_files_data[sample['primary_id']][sample['section_id']])
        sentence = f"For the primary trial participants, {primary_evidence}"
        secondary_evidence = sample.get("secondary_id")
        if secondary_evidence:
            secondary_evidence = ", ".join(CT_files_data[sample['secondary_id']][sample['section_id']])
            sentence = f"{sentence}; For the secondary trial participants, {secondary_evidence}"
        temp = {"id": sample['id'], "clinical_trial":sentence, "hypothesis":sample['statement'], "label":sample['label']}
        samples.append(temp)
    
    return samples

# Similar to the format of MedNLI
def create_json(file_name, data):
    samples = collect_data(data)
    json_dict = {}
    for s in samples:
        json_dict[s["id"]] = {"sentence1":s["clinical_trial"], "sentence2":s["hypothesis"], "gold_label":s["label"]}
    
    with open(f"../training-data/TSV_DATA/{file_name}.json", "w") as f:
        json.dump(json_dict, f, indent=4)


if __name__ == "__main__":
    data = json.load(open('../training-data/train.json'))
    create_json("train_tsv", data)
    data = json.load(open('../training-data/dev.json'))
    create_json("dev_tsv", data)