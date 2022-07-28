import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
import os

class HogestoryCog(commands.Cog):

    def __init__(self, bot):
        print('謎ストーリー初期化')
        self.bot = bot

    with open('./hogestory.yaml', mode='rt', encoding='utf-8_sig') as file:
        stack: list[list[str]] = yaml.unsafe_load(file)

    #ランダム抽出をここでやっちゃう作戦
    def word(shuffle):
        with open('./hogestory.yaml', 'r',encoding="utf-8_sig") as f:
            data = yaml.unsafe_load(f)
            hogehoge = data['story']
            if shuffle == True:
                hogehoge = random.sample(hogehoge, len(hogehoge))
            #randomwordが完成したシャッフル
            hoge = ''.join(hogehoge)
        return hoge

    lang_codes: list[str] = ['en', 'it', 'ne', 'ko', 'de']

    tr = Translator()

    def random_transe(word: str, lang: str, loop: int, lang_codes: list[str]) -> str:
        if loop == 0:
            return HogestoryCog.tr.translate(word, src=lang, dest='ja').text
        else:
            random.shuffle(lang_codes)
            tmp_lang = lang_codes.pop()
            return HogestoryCog.random_transe(
                word=HogestoryCog.tr.translate(
                    word, src=lang, dest=tmp_lang).text,
                lang=tmp_lang,
                loop=loop - 1,
                lang_codes=lang_codes
            )

    #コマンドグループを定義っ！！！
    story = SlashCommandGroup('story', 'test')

    @story.command(name="get",description="謎の物語を表示します")
    async def story_get(
            self,
            ctx: discord.ApplicationContext,
            ):
        await ctx.respond(HogestoryCog.word(shuffle=False))

    #いつどこランダム排出
    @story.command(name="shuffle",description="謎の物語をシャッフルします")
    async def story_shuffle(
            self,
            ctx: discord.ApplicationContext,
            ):
        await ctx.respond(HogestoryCog.word(shuffle=True))

    @story.command(name="set",description="謎の物語に文章を追加します。最初に「ところで」や「しかし」など接続詞をいれるとランダム抽出でいい感じになります。")
    async def story_set(
        self,
        ctx: discord.ApplicationContext,
        content: Option(str, required=True, description="追加する文章（短いほうが面白いです）を設定してください。最初に「ところで」や「しかし」など接続詞をいれるとランダム抽出でいい感じになります。", ),
        ):

        with open('./hogestory.yaml', 'r+',encoding="utf-8_sig") as f:
            data = yaml.safe_load(f)
            hogedata = data['story']
            hogedata.append(content)
            print (hogedata)
            data['story'] = hogedata
            print (data)
            f.seek(0)
            yaml.dump(data, f,default_flow_style=False,allow_unicode=True)
        await ctx.respond(f"{content}を追加しました。")

    @story.command(name='trans', description='謎の物語を再翻訳で支離滅裂な文章に変換します')
    async def storytrans(
        self, 
        ctx, 
        loop: Option(int, description='再翻訳回数を上げて精度を低めます デフォルト loop=1', min_value=1, max_value=5, default=1, required=False)
        ):
        await ctx.respond(f'翻訳前 : {HogestoryCog.word()}')
        dest_word = HogestoryCog.random_transe(
            word=HogestoryCog.word(shuffle=True),
            lang='ja',
            loop=loop,
            lang_codes=copy(HogestoryCog.lang_codes)
        )
        await ctx.interaction.edit_original_message(content=f'翻訳前 : {HogestoryCog.word()}\n翻訳後 : {dest_word}')

def setup(bot):
    bot.add_cog(HogestoryCog(bot))