import json
import yaml

# yamlを読み込んでlistで返却します
def read_json() -> list[str]:
    with open('genshin_avater.json', 'r',encoding="utf-8") as f:
        return json.load(f)

# ymalに一次配列のlistを上書きします
def write_json(words: list[str]):
    with open('genshin_avater.json', 'w',encoding="utf-8") as f:
        json.dump(words, f,)

# ymalに一次配列のlistを上書きします
def write_yaml(words: list[str]):
    with open('genshin_avater.yaml', 'w',encoding="utf-8_sig") as f:
        yaml.dump(words,f,default_flow_style=False,allow_unicode=True)

l = dict()

for n in read_json():
    print(n)
    hoge = n["id"]
    l[hoge] = {"iconName": n["iconName"],"sideIconName": n["sideIconName"],"bodyType": n["bodyType"],"weaponType": n["weaponType"]}
    continue

write_yaml(l)


