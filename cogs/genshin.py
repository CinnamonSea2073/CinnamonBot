import discord
from discord.ui import Select,View,Button
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
import math
import aiohttp
from lib.yamlutil import yaml
import traceback
from typing import List

uidListYaml = yaml(path='uid.yaml')
uidList = uidListYaml.load_yaml()
dataYaml = yaml(path='genshin_avater.yaml')
data = dataYaml.load_yaml()
charactersYaml = yaml(path='characters.yaml')
characters = charactersYaml.load_yaml()
genshinJpYaml = yaml(path='genshinJp.yaml')
genshinJp = genshinJpYaml.load_yaml()
icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"
l: list[discord.SelectOption] = []
gctx = discord.ApplicationContext

class uidselectView(View):
    @discord.ui.select(
            placeholder="表示するUIDを指定してね",
            options=l
        )
    async def select_callback(self, select:discord.ui.Select, interaction):
        global gctx
        await gctx.interaction.edit_original_message(content="アカウント情報読み込み中...")  
        embed = await GenshinCog.getApi(self,uid=select.values[0])
        await gctx.interaction.edit_original_message(content="キャラ情報読み込み中...")  
        #view = View()
        #getListで、IDが入ったリストを持ってくる
        #とりあえずIDの数だけボタンを生成
        hoge = []
        for id in await GenshinCog.getList(self,uid=select.values[0]):
            hoge.append(id)
        await gctx.respond(content=None,embed=embed,view=TicTacToe(hoge, select.values[0]))

async def getCharacter(uid,id):
    url = f"https://enka.network/u/{uid}/__data.json"
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            resp = await response.json()
    name = characters[id]["NameId"]
    name = genshinJp[name]
    embed = discord.Embed( 
                        title=name,
                        color=0x1e90ff, 
                        description="多分リアルタイムだよ", 
                        url=url 
                        )
    print(id)
    id = int(id)
    try:
        for n in resp['avatarInfoList']:
            if n["avatarId"] == id:
                chara = n
                print("hogehogheogheohgpoihvgp;ogiazwqp;oabwo")
                break
            else:
                continue
        for n in resp['playerInfo']["showAvatarInfoList"]:
            print(n["avatarId"])
            if n["avatarId"] == id:
                level = n["level"]
                print("hogehogehoge")
                break
            else:
                continue
        hoge = characters[str(id)]["sideIconName"]
        embed.set_author(name=resp['playerInfo']['nickname'],
                icon_url=f"https://enka.network/ui/{hoge}.png"
                )
        embed.add_field(inline=True,name="キャラレベル",value=f"{level}lv")
        embed.add_field(inline=True,name="キャラ突破レベル",value=str(chara["propMap"]["1002"]["ival"]))
        embed.add_field(inline=True,name="HP",
            value=f'{str(round(chara["fightPropMap"]["1"]))} + {str(round(chara["fightPropMap"]["2000"]) - round(chara["fightPropMap"]["1"]))} = {str(round(chara["fightPropMap"]["2000"]))}'
        )
        embed.add_field(inline=True,name="攻撃力",
            value=f'{str(round(chara["fightPropMap"]["4"]))} + {str(round(chara["fightPropMap"]["2001"]) - round(chara["fightPropMap"]["4"]))} = {str(round(chara["fightPropMap"]["2001"]))}'
        )
        embed.add_field(inline=True,name="防御力",
            value=f'{str(round(chara["fightPropMap"]["7"]))} + {str(round(chara["fightPropMap"]["2002"]) - round(chara["fightPropMap"]["7"]))} = {str(round(chara["fightPropMap"]["2002"]))}'
        )
        embed.add_field(inline=True,name="会心率",
            value=f'{str(round(chara["fightPropMap"]["20"] *100))}%'
        )
        embed.add_field(inline=True,name="会心ダメージ",
            value=f'{str(round(chara["fightPropMap"]["22"]*100))}%'
        )
        embed.add_field(inline=True,name="元素チャージ効率",
            value=f'{str(round(chara["fightPropMap"]["23"]*100))}%'
        )
        embed.add_field(inline=True,name="元素熟知",
            value=f'{str(round(chara["fightPropMap"]["28"]))}'
        )
        buf = 1
        if round(chara["fightPropMap"]["30"]*100) > 0:
            embed.add_field(inline=True,name="物理ダメージ",
                value=f'{str(round(chara["fightPropMap"]["30"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["30"])
        elif round(chara["fightPropMap"]["40"]*100) > 0:
            embed.add_field(inline=True,name="炎元素ダメージ",
                value=f'{str(round(chara["fightPropMap"]["40"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["40"])
        elif round(chara["fightPropMap"]["41"]*100) > 0:
            embed.add_field(inline=True,name="雷元素ダメージ",
                value=f'{str(round(chara["fightPropMap"]["41"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["41"])
        elif round(chara["fightPropMap"]["42"]*100) > 0:
            embed.add_field(inline=True,name="水元素ダメージ",
                value=f'{str(round(chara["fightPropMap"]["42"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["42"])
        elif round(chara["fightPropMap"]["43"]*100) > 0:
            embed.add_field(inline=True,name="草元素ダメージ",
                value=f'{str(round(chara["fightPropMap"]["43"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["42"])
        elif round(chara["fightPropMap"]["44"]*100) > 0:
            embed.add_field(inline=True,name="風元素ダメージ",
                value=f'{str(round(chara["fightPropMap"]["44"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["44"])
        elif round(chara["fightPropMap"]["45"]*100) > 0:
            embed.add_field(inline=True,name="岩元素ダメージ",
                value=f'{str(round(chara["fightPropMap"]["45"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["45"])
        elif round(chara["fightPropMap"]["46"]*100) > 0:
            embed.add_field(inline=True,name="氷元素ダメージ",
                value=f'{str(round(chara["fightPropMap"]["46"]*100))}%'
            )
            buf += round(chara["fightPropMap"]["46"])
        tmp = 1 + round(chara["fightPropMap"]["20"]) * round(chara["fightPropMap"]["22"])
        embed.add_field(inline=False,name="**ダメージ計算結果（雑計算）**",
            value=f'{str(round(chara["fightPropMap"]["4"]) * tmp * buf)}'
        )
        temp = []
        for myvalue in chara["skillLevelMap"].values():
            temp.append(f"{myvalue}")
        embed.add_field(inline=False,name="天賦レベル",
            value="\n".join(temp)
        )
        for n in chara["equipList"]:
            hoge = str(n["flat"]["setNameTextMapHash"])
            print(hoge)
            name = genshinJp[hoge]
            equip = genshinJp[n["flat"]["equipType"]]
            main = genshinJp[n["flat"]["reliquaryMainstat"]["mainPropId"]]
            hoge = []
            for b in n["flat"]["reliquarySubstats"]:
                name_ = genshinJp[b["appendPropId"]]
                value_ = b["statValue"]
                hoge.append(f"{name_}：{value_}")
            embed.add_field(inline=True,name=f'聖遺物：{equip}\n{name}\n{main}：{n["flat"]["reliquaryMainstat"]["statValue"]}\n{n["reliquary"]["level"]-1}lv\n',
                value="\n".join(hoge)
            )
    except KeyError:
        #raise
        embed.add_field(inline=False,name="エラー",value="多分キャラ詳細が非公開だと思われるよ。原神の設定で後悔設定にしてね。")
    embed.set_footer(text="made by CinnamonSea2073", icon_url=icon)
    return embed

class TicTacToeButton(discord.ui.Button["TicTacToe"]):
    def __init__(self, label: str, uid: str, dict):
        super().__init__(style=discord.ButtonStyle.secondary, label=label)
        self.dict = dict
        self.uid = uid

    async def callback(self, interaction: discord.Interaction):
        assert self.view is not None
        view: TicTacToe = self.view

        self.style = discord.ButtonStyle.success
        content = self.label
        #ラベル（名前）からIDを割り出す
        #多分「名前：iD」ってなってるはず
        id = self.dict[self.label]
        print(interaction.user.id)
        for child in self.view.children:
            child.style = discord.ButtonStyle.gray
        await interaction.response.edit_message(content=content, embed=await getCharacter(self.uid, id), view=None)

class TicTacToe(discord.ui.View):
    children: List[TicTacToeButton]

    def __init__(self, data, uid):
        super().__init__(timeout=190)
        names = []
        dict = {}
        #入ってきたidを名前にしてリスト化
        for id in data:
            id = str(id)
            print(id)
            name = characters[id]["NameId"]
            print(name)
            name = genshinJp[name]
            print(name)
            names.append(name)
            dict.update({name: id})
            print(dict)
        #名前をラベル、ついでにdictとuidも送り付ける
        for v in names:
            self.add_item(TicTacToeButton(v,uid,dict))

class GenshinCog(commands.Cog):

    def __init__(self, bot):
        print('genshin初期化')
        self.bot = bot
        global l
        for uid, v in uidList.items():
            print(v['uid'])
            print(v['user'])
            l.append(discord.SelectOption(label=str(uid), description=v['user']))

    async def getApi(self,uid):
        url = f"https://enka.network/u/{uid}/__data.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                resp = await response.json()
        try:
            embed = discord.Embed( 
                                title="あなたの原神ステータスだよ",
                                color=0x1e90ff, 
                                description="多分リアルタイムだよ", 
                                url=url 
                                )
                                
            hoge = data[resp['playerInfo']['profilePicture']['avatarId']]['iconName']
            embed.set_author(name=resp['playerInfo']['nickname'],
                icon_url=f"https://enka.network/ui/{hoge}.png"
            )
            embed.add_field(inline=False,name="ユーザーネーム",value=resp['playerInfo']['nickname'])
            try:
                embed.add_field(inline=False,name="ステータスメッセージ",value=resp['playerInfo']['signature'])
            except:
                print("hoge")
            embed.add_field(inline=False,name="レベル",value=resp['playerInfo']['level'])
            embed.add_field(inline=False,name="世界ランク",value=resp['playerInfo']['worldLevel'])
            embed.add_field(inline=False,name="深境螺旋",value=f"第{resp['playerInfo']['towerFloorIndex']}層 第{resp['playerInfo']['towerLevelIndex']}間")
            embed.set_footer(text="made by CinnamonSea2073", icon_url=icon)
            return embed
        except:
            embed = discord.Embed( 
                    title=f"エラーが発生しました。APIを確認してからもう一度お試しください。\n{url}",
                    color=0x1e90ff, 
                    url=url 
                    )
            return embed

    async def getList(self,uid):
        url = f"https://enka.network/u/{uid}/__data.json"
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                resp = await response.json()
                resalt = []
        for id in resp["playerInfo"]["showAvatarInfoList"]:
            resalt.append(id["avatarId"])
        return resalt

    genshin = SlashCommandGroup('genshin', 'test')

    @genshin.command(name="get", description="UUIDからキャラ情報を取得します")
    async def genshin_get(
            self,
            ctx: discord.ApplicationContext,
    ):
        await ctx.respond("読み込み中")
        global gctx
        gctx = ctx
        view = uidselectView()
        await ctx.send(content="読み込み完了", view=view)

    @genshin.command(name="set", description="あなたのUIDを設定します")
    async def genshin_set(
            self,
            ctx: discord.ApplicationContext,
            uid: Option(int, required=True, description="UIDを指定しやがれってんだ!!!（？）", )
    ):
        if str(uid) in uidList:
            await ctx.respond("既に登録済みです")
            return
        await ctx.respond("読み込み中")
        print(uid)
        user = await self.getApi(uid)
        try:
            url = f"https://enka.network/u/{uid}/__data.json"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    resp = await response.json()
            uidList[str(uid)] = {"uid": uid, "name": ctx.author.name, "user": resp['playerInfo']['nickname'], "level": resp['playerInfo']['level'], "world": resp['playerInfo']['worldLevel']}
            uidListYaml.save_yaml(uidList)
            global l
            l.append(discord.SelectOption(label=str(uid), description=resp['playerInfo']['nickname']))
            await ctx.send(f"<@{ctx.author.id}>\nUID多分設定できたで\nuid : **{uid}**\nusername : **{resp['playerInfo']['nickname']}**")
        except:
            await ctx.send(f"<@{ctx.author.id}>\n<@698127042977333248>\nなんかエラー起きたよ\nuid : **{uid}**\nhttps://enka.network/u/{uid}/__data.json")
            await self.bot.get_partial_messageable(1009731664412426240).send(f"```{traceback.format_exc()}``")
            raise

    @genshin.command(name="relord", description="【管理者限定】登録されてるプレイヤーの情報を更新します。")
    @commands.has_permissions(manage_messages=True)
    async def genshin_getList(
            self,
            ctx: discord.ApplicationContext,
    ):
        await ctx.respond("読み込み中...")
        embed = discord.Embed( 
            title="原神ステータスだよ",
            color=0x1e90ff, 
            )
        await ctx.send("くっそ時間かかるよ")
        for uid in uidList:
            url = f"https://enka.network/u/{uid}/__data.json"
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    resp = await response.json()
            await ctx.send(f"読み込み中「{resp['playerInfo']['nickname']}」")
            uidList[str(uid)] = {"uid": uid, "name": uidList[uid]['name'], "user": resp['playerInfo']['nickname'], "level": resp['playerInfo']['level'], "world": resp['playerInfo']['worldLevel']}
            uidListYaml.save_yaml(uidList)
            embed.add_field(
                name=uidList[uid]['user'],
                value=f"UID：{uid}\nレベル：{uidList[uid]['level']}\nランク：{uidList[uid]['world']}"
            )
        embed.set_footer(text="made by CinnamonSea2073", icon_url=icon)
        await ctx.send(embed=embed)

    @genshin.command(name="getlist", description="登録されてるプレイヤーの情報をまとめて取得します")
    async def genshin_getList(
            self,
            ctx: discord.ApplicationContext,
    ):
        await ctx.respond("読み込み中...")
        embed = discord.Embed( 
            title="原神ステータスだよ",
            color=0x1e90ff, 
            )
        for uid in uidList:
            embed.add_field(
                name=uidList[uid]['user'],
                value=f"UID：{uid}\nレベル：{uidList[uid]['level']}\nランク：{uidList[uid]['world']}"
            )
        embed.set_footer(text="made by CinnamonSea2073", icon_url=icon)
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(GenshinCog(bot))