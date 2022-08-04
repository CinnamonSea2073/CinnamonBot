from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
import random
import urllib
import asyncio

icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

gameYaml = yaml('game.yaml')
genshinYaml = yaml('genshin.yaml')
genshinHYaml = yaml('genshinH.yaml')
genshinStarYaml = yaml('genshin_ster.yaml')

users = gameYaml.load_yaml()
words = genshinYaml.load_yaml()
jhwords = genshinHYaml.load_yaml()
sters = genshinStarYaml.load_yaml()

PERDATA = {0: 0.006, 1: 0.006, 2: 0.006, 3: 0.006, 4: 0.006, 5: 0.006, 6: 0.006, 7: 0.066, 8: 0.4, 9: 0.006,
           10: 0.006, 11: 0.006, 12: 0.006, 13: 0.006, 14: 0.006, 15: 0.006, 16: 0.066, 17: 0.4, 18: 0.006}


def getPer(top):
    for v in PERDATA:
        if top <= v:
            print(PERDATA[v])
            return PERDATA[v]


class GamesCog(commands.Cog):

    def __init__(self, bot):
        print('げーむ初期化.')
        self.bot = bot

    def embeded(title, description, url):
        embed = discord.Embed(title=title, color=0x1e90ff,
                              description=description)
        embed.set_image(url=url)
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=icon)
        return embed

    def point(id, name):
        global users
        if id not in users:
            users[id] = {"name": name, "point": 100, "top": 0}
            gameYaml.save_yaml(users)
        return users[id]["point"]

    def getpoint(id, name, point):
        global users
        if id in users:
            point += users[id]["point"]
            top = users[id]["top"]
        else:
            point += 100
            top = 0
        if name == None:
            name = users[id]['name']
        users[id] = {"name": name, "point": point, "top": top}
        gameYaml.save_yaml(users)
        return str(users[id]["point"])

    def genshinliset(id, name, top):
        global users
        if id not in users:
            users[id] = {"name": name, "point": 100, "top": top}
        else:
            users[id] = {"name": name, "point": users[id]["point"], "top": top}
        gameYaml.save_yaml(users)
        return

    def genshinget(id, name):
        global users
        top = 1
        if id in users:
            top += users[id]["top"]
            point = users[id]["point"]
        else:
            top += 0
            point = 100
        users[id] = {"name": name, "point": point, "top": top}

        gameYaml.save_yaml(users)
        return int(top)

    def genshingen(name):
        global words
        global jhwords
        if name in words:
            resalt = urllib.parse.quote(words[name]["zh"])
        elif name in jhwords:
            resalt = urllib.parse.quote(words[jhwords[name]["ja"]]["zh"])
        else:
            resalt = None
        return f"https://bbs.hoyolab.com/hoyowiki/picture/character/{resalt}/avatar.png"

    def genshinster(name):
        global sters
        return random.choice(sters[name])

    def genshinwish_engine(n):
        randomresalt = []
        roof = 0
        for num in range(n):
            roof += 1
            # 天井から確率を計算
            # hogeはリリース時に消せ（フラグ）
            hoge = roof/10
            per = getPer(hoge)
            three = 1 - per - 0.051
            five = per / 2
            if roof % 10 > 0:
                # 通常の確率。
                # さっき計算した確率をもとにガチャを回します。
                # 星5が出た場合は、星5が出なくなる天井カウント90に、
                # 星6が出た場合は天井カウントをリセットします。
                tmpresalt = random.choices(["3", "4", "5", "6"], weights=[
                                           three, 0.051, five, five])
                if "5" in tmpresalt:
                    roof = 90
                elif "6" in tmpresalt:
                    roof = 0
            elif roof % 10 == 0:
                # 星4天井システム。必ず星4以上を追加します。
                # さっき計算した確率をもとにガチャを回します。
                # 星5が出た場合は、星5が出なくなる天井カウント90に、
                # 星6が出た場合は天井カウントをリセットします。
                tmpresalt = random.choices(["3", "4", "5", "6"], weights=[
                                           three, 0.051, five, five])
                if "5" in tmpresalt:
                    roof = 90
                elif "6" in tmpresalt:
                    roof = 0
                elif "3" in tmpresalt:
                    tmpresalt = ["4"]
            if roof == 90:
                # 一度目の天井に達した確率。2/1の確率で5か6を追加。6の場合天井リセット。
                # 返信では90連で星5を確定で排出し、2/1の確率で恒常（ハズレ）かどうか変化するため、
                # 5か6を追加します。
                # 6が出た場合は天井リセットです。
                tmpresalt = random.choices(["5", "6"], weights=[0.5, 0.5])
                if "6" in tmpresalt:
                    roof = 0
            elif roof < 180:
                # 一度目の天井以降の確率。5は出ない。6の場合天井と確率リセット。
                # 計算した確率をもとにガチャを回します。
                # 恒常キャラ（ハズレ）が出た次の星5は確定で当たりが出るようになっているので、5は必ず排出されません。
                # 星6が出た場合は天井カウントをリセットします。
                if "5" in tmpresalt:
                    tmpresalt = ["6"]
                    roof = 0
            elif roof == 180:
                # 二度目の天井。確定で6を追加。ついでに天井リセット。
                tmpresalt = ["6"]
                roof = 0
            randomresalt.append("".join(tmpresalt))
        return randomresalt

    def genshinwish_counter(randomresalt):
        final_result = []
        for r in randomresalt:
            if r == "4":
                # 4が入ってるだけ繰り返します。2/1の確率で恒常星4となり、結果を文字列化、キャラ名取得、画像url生成、embed生成します
                sterresalt = random.choices(
                    ["four_1", "four_2"], weights=[0.5, 0.5])
                genshinname = GamesCog.genshinster("".join(sterresalt))
                final_result.append(f"★★★★   {genshinname}")
                continue
            elif r == "5":
                # 5が入ってるだけ繰り返します。恒常星5のキャラ名取得、画像url生成、embed生成し、送信します。
                genshinname = GamesCog.genshinster("five")
                final_result.append(f"**★★★★★**   **{genshinname}**")
                continue
            elif r == "6":
                # 星6（ピックアップキャラ）のキャラ名を取得、画像url生成、embed生成し、ガチャ演出のEmbedを編集します。
                genshinname = GamesCog.genshinster("six")
                final_result.append(f"**★★★★★**   **{genshinname}**")
                continue
            elif r == "3":
                # 星3という結果を追加しておきます。
                genshinname = "星3武器"
                # final_result.append(genshinname)
                continue
        return final_result

    Skip_list = [
        OptionChoice(name='ガチャ演出をスキップする', value=1),
        OptionChoice(name='ガチャ演出をスキップしない', value=0)
    ]

    icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

    # コマンドグループを定義っ！！！
    money = SlashCommandGroup('money', 'test')

    @money.command(name="check", description="所持金を確認します")
    async def check(
        self,
        ctx: discord.ApplicationContext,
    ):
        print(ctx.author.id)
        money = "{:,}".format(
            int(GamesCog.point(ctx.author.id, ctx.author.name)))
        await ctx.respond(f"現在のあなたの所持金は **{money}￥** です！")

    #@money.command(name="up", description="お金を増やします")
    async def up(
        self,
        ctx: discord.ApplicationContext,
        point: Option(int, required=True, description="追加する量を設定してください", )
    ):
        print(ctx.author.id)
        money = "{:,}".format(int(GamesCog.getpoint(
            ctx.author.id, ctx.author.name, point)))
        await ctx.respond(f"現在のあなたの所持金は **{money}￥** です！")

    @money.command(name="down", description="お金を減らします")
    async def down(
        self,
        ctx: discord.ApplicationContext,
        point: Option(int, required=True, description="減らす量を設定してください", )
    ):
        if point < 0:
            await ctx.respond(f":thinking:")
            return
        print(ctx.author.id)
        money = "{:,}".format(int(GamesCog.getpoint(
            ctx.author.id, ctx.author.name, -point)))
        await ctx.respond(f"現在のあなたの所持金は **{money}￥** です！")

    @money.command(name="genshin", description="ガチャシミュレーター実装前テストコマンド")
    async def genshin(
        self,
        ctx: discord.ApplicationContext,
        content: Option(str, required=True, description="キャラ名（ひらかなでもおｋ）", )
    ):
        picture = GamesCog.genshingen(content)
        if picture == "https://bbs.hoyolab.com/hoyowiki/picture/character/None/avatar.png":
            content = f" \"{content}\" は原神データベースに存在しません。"
        embed = discord.Embed(title=content, color=0x1e90ff,)
        embed.set_image(url=picture)
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=GamesCog.icon)
        await ctx.respond(embed=embed)

    @money.command(name="genshinwish_n", description="原神n回ガチャシミュレーター　※楓原万葉ピックアップ中！")
    async def genshinwish_n(
        self,
        ctx: discord.ApplicationContext,
        n: Option(int, required=False, description="ガチャを引く回数",
                  min_value=10, max_value=200, default=200)
    ):
        # 何か送信しないと応答なしと判断されてエラーを吐くので一応
        await ctx.respond("処理を開始中...")
        id = ctx.author.id
        name = ctx.author.name
        money = n*3200

        # 金銭消費しないならここをFalseに変えてね
        hogehogehogehoge = True
        if hogehogehogehoge == True:
            if GamesCog.point(id, name) < money:
                await ctx.send(f"<@{id}> お金が足りません。/money up で増やしてください。\nあなたの所持金は**{GamesCog.point(id,name)}￥**です。")
                iscommand = False
                await ctx.send("処理終了")
            else:
                GamesCog.getpoint(id, None, -money)
                await ctx.send(f"<@{id}> お金を{money}円消費しました。")
                iscommand = True
        elif hogehogehogehoge == False:
            iscommand = True

        # 上のコマンドで金銭が足りてたらレッツガチャ！
        if iscommand == True:

            embed = discord.Embed(title=f"ガチャ結果", color=0x1e90ff,)
            embed.add_field(
                name=f"<@{ctx.author.id}>\nガチャを引いた回数：{n}\n使った金額：約{n*320}円", value="=====================")
            await ctx.respond(embed=embed)

            # n回繰り返すやつ
            await ctx.send("ガチャを回しています...")
            randomresalt = GamesCog.genshinwish_engine(n)

            # 最後に出力です。ガチャ結果からキャラ名などをランダムで出し、画像として出力します。
            # ランダムの結果分（10回）forを回し、すべての要素を確認します。
            await ctx.send("ガチャ結果処理中...")
            final_resalt = GamesCog.genshinwish_counter(randomresalt)

            # ガチャ結果まとめ
            await ctx.send("処理完了")
            embed = discord.Embed(title="ガチャ結果", color=0x1e90ff,)
            embed.add_field(name="=====================",
                            value="\n".join(final_resalt))
            embed.set_footer(text="made by CinnamonSea2073",
                             icon_url=GamesCog.icon)
            await ctx.respond(embed=embed)

    @money.command(name="genshinwish", description="原神ガチャシミュレーター　※楓原万葉ピックアップ中！")
    async def genshinwish(
        self,
        ctx: discord.ApplicationContext,
        skip: Option(int, choices=Skip_list, required=False,
                     description="流れ星演出のスキップをするかどうか（書かない場合はスキップしない）")
    ):
        # 何か送信しないと応答なしと判断されてエラーを吐くので一応
        await ctx.respond("処理を開始中...")

        # 金銭消費しないならここをFalseに変えてね
        hogehogehogehoge = True
        if hogehogehogehoge == True:
            if GamesCog.point(ctx.author.id, ctx.author.name) < 3200:
                await ctx.send(f"<@{ctx.author.id}> お金が足りません。/money up で増やしてください。\nあなたの所持金は**{GamesCog.point(ctx.author.id,ctx.author.name)}￥**です。")
                iscommand = False
                await ctx.send("処理終了")
            else:
                GamesCog.getpoint(ctx.author.id, None, -3200)
                await ctx.send(f"<@{ctx.author.id}> お金を3,200円消費しました。")
                iscommand = True
        elif hogehogehogehoge == False:
            iscommand = True

        # 上のコマンドで金銭が足りてたらレッツガチャ！
        if iscommand == True:

            # skipに何も入ってなかったらとりあえずFalse突っ込んでおこうね
            if skip == None:
                skip = 0

            # 天井カウントを読み込みます。resaltが送信者の天井カウントです。
            await ctx.send("天井カウント処理中...")
            id = ctx.author.id
            name = ctx.author.name
            resalt = GamesCog.genshinget(id, name)

            # 確率を計算します。getPerにて、天井カウントから星5排出の確率を出し、その確率に応じてほかの確率も変化します。
            # perが本来の星5排出の確率ですが、2/1の確率で恒常キャラ（ハズレ星5）となるため、fiveはperの半分にしています。
            # 星3の排出率は、星4の排出確率が0.051（5.1%）固定なのを考慮したうえで合計が1になるように計算しています。
            await ctx.send("天井カウントより確率を計算中...")
            per = getPer(resalt)
            three = 1 - per - 0.051
            five = per / 2
            print(per)

            # 次に確率です。天井システムを考慮したうえで、10連分の結果をrandomresalt[]として出します。
            # 結果によっては天井カウントをリセットさせます。
            await ctx.send("ガチャ結果を処理中...")
            randomresalt = []
            if resalt < 9:
                # 完全に何も出していない状態での初期確率。確定で4を追加。
                # さっき計算した確率をもとに、9回ガチャを回します。その後、4を追加することで、疑似的に確定で星4を排出するようになっています。
                # 回している途中に星5が出た場合は、星5が出なくなる天井カウント9に、
                # 星6が出た場合は天井カウントをリセットします。
                # また、70連目当たりから確率が上昇するため、途中で星5か6が排出された際に確率を戻します。
                for num in range(9):
                    #tmpresalt = np.random.choice(["3","4","5","6"], p=[three,0.051,five,five])
                    tmpresalt = random.choices(["3", "4", "5", "6"], weights=[
                                               three, 0.051, five, five])
                    randomresalt.append("".join(tmpresalt))
                    print(randomresalt)
                    if "5" in randomresalt:
                        GamesCog.genshinliset(id, name, 9)
                        per = 0.006
                        three = 1 - per - 0.051
                        five = per / 2
                    elif "6" in randomresalt:
                        GamesCog.genshinliset(id, name, 0)
                        per = 0.006
                        three = 1 - per - 0.051
                        five = per / 2
                randomresalt.append("4")
            elif resalt == 9:
                # 一度目の天井に達した確率。2/1の確率で5か6を追加。6の場合天井リセット。
                # さっき計算した確率をもとに、9回ガチャを回します。その後、4を追加することで、疑似的に確定で星4を排出するようになっています。
                # また、一度目の天井では星5を確定で排出し、2/1の確率で恒常（ハズレ）かどうか変化するため、
                # ガチャ後に確定で5か6を追加します。
                # 6が出た場合は天井リセットです。
                for num in range(9):
                    tmpresalt = random.choices(["3", "4", "5", "6"], weights=[
                                               three, 0.051, five, five])
                    randomresalt.append("".join(tmpresalt))
                    print(randomresalt)
                    if "5" in randomresalt:
                        per = 0.006
                        three = 1 - per - 0.051
                        five = per / 2
                    elif "6" in randomresalt:
                        GamesCog.genshinliset(id, name, 0)
                        per = 0.006
                        three = 1 - per - 0.051
                        five = per / 2
                randomresalt.append("4")
                srinuke = random.choices(["5", "6"], weights=[0.5, 0.5])
                randomresalt.append("".join(srinuke))
                if "6" in srinuke:
                    GamesCog.genshinliset(id, name, 0)
            elif resalt < 18:
                # 一度目の天井以降の確率。確定で4を追加。5は出ない。6の場合天井と確率リセット。
                # 計算した確率をもとに、9回ガチャを回します。その後、4を追加することで、疑似的に確定で星4を排出するようになっています。
                # 恒常キャラ（ハズレ）が出た次の星5は確定で当たりが出るようになっているので、5は必ず排出されません。
                # 星6が出た場合は天井カウントをリセットします。
                # また、160連目当たりから確率が上昇するため、途中で星5か6が排出された際に確率を戻します。
                for num in range(9):
                    tmpresalt = random.choices(
                        ["3", "4", "6"], weights=[three, 0.051, per])
                    randomresalt.append("".join(tmpresalt))
                    print(randomresalt)
                    if "6" in randomresalt:
                        GamesCog.genshinliset(id, name, 0)
                        per = 0.006
                        three = 1 - per - 0.051
                randomresalt.append("4")
            elif resalt == 18:
                # 二度目の天井の確率。確定で6を追加。その他の確率は初期確率と同率。ついでに天井リセット。
                # さっき計算した確率をもとに、9回ガチャを回します。
                # 二度目の天井のため、確定で6を追加し、天井カウントをリセットします。
                # 天井では確率は0.6%固定なので、分岐は必要ありません。
                for num in range(9):
                    tmpresalt = random.choices(["3", "4", "5", "6"], weights=[
                                               three, 0.051, five, five])
                    randomresalt.append("".join(tmpresalt))
                    print(randomresalt)
                randomresalt.append("6")
                GamesCog.genshinliset(id, name, 0)

            # ここで結果ごとにガチャ演出をさせ、ガチャ演出後に次の処理が行われるよう非同期sleepさせます。
            # 5か6の場合は彗星もどきが金色に光る演出になります。
            # skipがTrueの場合は飛ばします。
            if skip == 0:
                await ctx.send("ガチャ結果による分岐処理中...")
                if "5" in randomresalt or "6" in randomresalt:
                    direction_embed = GamesCog.embeded(
                        None, None, "https://c.tenor.com/rOuL0G1uRpMAAAAC/genshin-impact-pull.gif")
                    msg = await ctx.send(embed=direction_embed)
                else:
                    direction_embed = GamesCog.embeded(
                        None, None, "https://c.tenor.com/pVzBgcp1RPQAAAAC/genshin-impact-animation.gif")
                    msg = await ctx.send(embed=direction_embed)
                await asyncio.sleep(5)
            await ctx.send("処理完了")

            # ガチャ演出のgifを貼ったEmbedを編集することで、どこからが今回のガチャ結果なのか見やすくします。。
            # skipがTrueだと演出gifを貼ったEmbedがないので編集せずに普通に送信します。
            resalt_embed = discord.Embed(title="ガチャ10連結果", color=0xff5254,)
            resalt_embed.set_footer(
                text="made by CinnamonSea2073", icon_url=GamesCog.icon)
            if skip == 0:
                await msg.edit(embed=resalt_embed)
            else:
                await ctx.send(embed=resalt_embed)

            # 最後に出力です。ガチャ結果からキャラ名などをランダムで出し、画像として出力します。
            # ランダムの結果分（10回）forを回し、すべての要素を確認します。
            final_result = []

            for r in randomresalt:
                if r == "4":
                    # 4が入ってるだけ繰り返します。2/1の確率で恒常星4となり、結果を文字列化、キャラ名取得、画像url生成、embed生成します
                    sterresalt = random.choices(
                        ["four_1", "four_2"], weights=[0.5, 0.5])
                    genshinname = GamesCog.genshinster("".join(sterresalt))
                    final_result.append(f"**{genshinname}**   ★★★★")
                    await ctx.respond(embed=GamesCog.embeded(f"{genshinname}    ★★★★", None, GamesCog.genshingen(genshinname)))
                    continue
                elif r == "5":
                    # 5が入ってるだけ繰り返します。恒常星5のキャラ名取得、画像url生成、embed生成し、送信します。
                    genshinname = GamesCog.genshinster("five")
                    final_result.append(f"**{genshinname}**   ★★★★★")
                    await ctx.respond(embed=GamesCog.embeded(f"{genshinname}    ★★★★★", None, GamesCog.genshingen(genshinname)))
                    continue
                elif r == "6":
                    # 星6（ピックアップキャラ）のキャラ名を取得、画像url生成、embed生成し、ガチャ演出のEmbedを編集します。
                    genshinname = GamesCog.genshinster("six")
                    final_result.append(f"**{genshinname}**   ★★★★★")
                    await ctx.respond(embed=GamesCog.embeded(f"{genshinname}    ★★★★★", None, GamesCog.genshingen(genshinname)))
                    continue
                elif r == "3":
                    # 星3という結果を追加しておきます。
                    genshinname = "星3武器"
                    final_result.append(genshinname)
                    continue

            # ガチャ結果まとめ
            # 天井の場合確率を100にするためのif
            if resalt == 90 or resalt == 180:
                resalt_per = 100
            else:
                resalt_per = per*100
            print(resalt_per)
            embed = discord.Embed(title=f"ガチャ結果", color=0x1e90ff,)
            embed.add_field(
                name=f"<@{ctx.author.id}>\nガチャを引いた回数：{resalt*10}\n使った金額：約{resalt*1600*2}円\n今回のガチャの★5確率：{resalt_per}%\n=====================", value="\n".join(final_result))
            embed.set_footer(text="made by CinnamonSea2073",
                             icon_url=GamesCog.icon)
            await ctx.respond(embed=embed)


def setup(bot):
    bot.add_cog(GamesCog(bot))
