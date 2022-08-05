import json
import yaml

# yamlを読み込んでlistで返却します
def read_json() -> list[str]:
    with open('genshinwords.json', 'r',encoding="utf-8") as f:
        return json.load(f)

# ymalに一次配列のlistを上書きします
def write_json(words: list[str]):
    with open('genshin.json', 'w',encoding="utf-8") as f:
        json.dump(words, f,)

# ymalに一次配列のlistを上書きします
def write_yaml(words: list[str]):
    with open('genshinH.yaml', 'w',encoding="utf-8_sig") as f:
        yaml.dump(words,f,default_flow_style=False,allow_unicode=True)

l = dict()

for n in read_json():
    print(n)
    if "tags" in n and "character-main" in n.get("tags"):
        #l.append({"name":n["ja"],"zh":n["zhCN"],"en":n["en"]})
        #l[n["ja"]] = {"jh":n["en"],"zh":n["zhCN"],"en":n["en"]}
        l[n["ja"]] = {"ja":n["ja"]}
        continue

write_yaml(l)


