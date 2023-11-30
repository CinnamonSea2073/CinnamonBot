from lib.yamlutil import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
import os
import cogs.point as point

itudokoYaml = yaml("itudoko.yaml")


class ItudokoCog(commands.Cog):

    def __init__(self, bot):
        print('いつどこ初期化')
        self.bot = bot

    # ランダム抽出をここでやっちゃう作戦

    def word():
        data = itudokoYaml.load_yaml()
        itu = random.choice(data['itu'])
        dokode = random.choice(data['dokode'])
        darega = random.choice(data['darega'])
        donoyouni = random.choice(data['donoyouni'])
        naniwosita = random.choice(data['naniwosita'])
        message = f"{itu}\n{dokode}\n{darega}\n{donoyouni}\n{naniwosita}"
        # randomwordが完成したランダム抽出
        return message

    lang_codes: list[str] = ['en', 'it', 'ne', 'ko', 'de']

    tr = Translator()

    itudoko_list = [
        OptionChoice(name='いつ', value='itu'),
        OptionChoice(name='どこで', value='dokode'),
        OptionChoice(name='だれが', value='darega'),
        OptionChoice(name='どのように', value='donoyouni'),
        OptionChoice(name='何をした', value='naniwosita')
    ]

    def random_transe(word: str, lang: str, loop: int, lang_codes: list[str]) -> str:
        if loop == 0:
            return ItudokoCog.tr.translate(word, src=lang, dest='ja').text
        else:
            random.shuffle(lang_codes)
            tmp_lang = lang_codes.pop()
            return ItudokoCog.random_transe(
                word=ItudokoCog.tr.translate(
                    word, src=lang, dest=tmp_lang).text,
                lang=tmp_lang,
                loop=loop - 1,
                lang_codes=lang_codes
            )

    # コマンドグループを定義っ！！！
    itudoko = SlashCommandGroup('itudoko', 'test')

    # いつどこランダム排出
    @itudoko.command(name="get", description="いつどこで誰が何をしたかランダムで排出します")
    async def itudoko_get(
            self,
            ctx: discord.ApplicationContext,
    ):
        await ctx.respond(ItudokoCog.word())

    @itudoko.command(name="set", description="いつどこで誰が何をしたかに単語を追加します")
    async def itudoko_set(
        self,
        ctx: discord.ApplicationContext,
        choice: Option(str, choices=itudoko_list, required=True, description="追加する項目を設定してください", ),
        content: Option(str, required=True, description="追加する単語を設定してください", ),
    ):

        data = itudokoYaml.load_yaml()
        hogedata = data[choice]
        hogedata.append(content)
        print(hogedata)
        data[choice] = hogedata
        print(data)
        itudokoYaml.save_yaml(data)
        await ctx.respond(f"{choice}に{content}を追加しました。")
        point.GamesCog.getpoint(ctx.author.id,ctx.author.name,10000)
        await ctx.respond(f"追加ありがとう！10,000円が追加されました。")

    @itudoko.command(name='trans', description='再翻訳で支離滅裂な文章に変換します')
    async def itudokotrans(
        self,
        ctx,
        loop: Option(int, description='再翻訳回数を上げて精度を低めます デフォルト loop=1',
                     min_value=1, max_value=5, default=1, required=False)
    ):
        word = ItudokoCog.word()
        await ctx.respond(f'翻訳前 : {word}')
        dest_word = ItudokoCog.random_transe(
            word=word,
            lang='ja',
            loop=loop,
            lang_codes=copy.copy(ItudokoCog.lang_codes)
        )
        await ctx.interaction.edit_original_message(content=f'翻訳前 :\n{word}\n翻訳後 :\n{dest_word}')


def setup(bot):
    bot.add_cog(ItudokoCog(bot))
