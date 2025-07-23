import json

input_file = "frazy.txt"
output_file = "frazy_kredyt_hipoteczny.jsonl"
keyword = "kredyt hipoteczny"

with open(input_file, "r", encoding="utf-8") as fin, open(output_file, "w", encoding="utf-8") as fout:
    for line in fin:
        query = line.strip()
        if query:
            fout.write(json.dumps({"keyword": keyword, "query": query}, ensure_ascii=False) + "\n")

print("Zapisano do:", output_file)
