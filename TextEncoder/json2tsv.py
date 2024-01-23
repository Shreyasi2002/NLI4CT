import json
import re

def process(input_path, output_path):
    json_data = json.load(open(input_path))
    with open(output_path, 'w') as o:
        for i, json_obj in json_data.items():
            for k, v in json_obj.items():
                v = re.sub(r'\t', ' ', v)
                v = re.sub(r'\\t', ' ', v)
                v = v.replace('\n', ' ')
                while '  ' in v:
                    v = v.replace('  ', ' ')
                json_obj[k] = v
            o.write(f"{i}\t{json_obj['sentence1'].strip()}\t{json_obj['sentence2'].strip()}\t{json_obj['gold_label'].strip()}\n")

if __name__ == '__main__':
    process('../training-data/TSV_DATA/dev_tsv.json', '../training-data/TSV_DATA/dev.tsv')
    process('../training-data/TSV_DATA/train_tsv.json', '../training-data/TSV_DATA/train.tsv')