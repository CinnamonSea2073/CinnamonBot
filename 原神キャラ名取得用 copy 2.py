import json
import yaml

# yamlを読み込んでlistで返却します
def read_json() -> list[str]:
    with open('characters.json', 'r',encoding="utf-8") as f:
        return json.load(f)

# ymalに一次配列のlistを上書きします
def write_json(words: list[str]):
    with open('genshin_avater.json', 'w',encoding="utf-8") as f:
        json.dump(words, f,)

# ymalに一次配列のlistを上書きします
def write_yaml(words: list[str]):
    with open('characters.yaml', 'w',encoding="utf-8_sig") as f:
        yaml.dump(words,f,default_flow_style=False,allow_unicode=True)

l = dict()
n = dict()
d = read_json()

for n in d:
    print(n)
    try:
        l[n] = {"NameId": str(d[n]["NameTextMapHash"]),"sideIconName": d[n]["SideIconName"],"Element": d[n]["Element"]}
    except:
        continue

write_yaml(l)


