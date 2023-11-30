import yaml
import discord
from discord.ext import commands
from discord import Option, OptionChoice, SlashCommandGroup
from googletrans import Translator
import random
import copy
from lib.yamlutil import yaml
import cogs.point as point

path = 'hogestory.yaml'

hogestory = yaml(path=path)


class HogestoryCog(commands.Cog):

    def __init__(self, bot):
        print('謎ストーリー初期化')
        self.bot = bot

    # yamlを読み込んでlistで返却します
    def read_yaml() -> list[str]:
        return (hogestory.load_yaml({"story": []}))['story']

    # ymalに一次配列のlistを上書きします
    def write_yaml(story: list[str]):
        hogestory.save_yaml({"story": story})

    lang_codes: list[str] = ['en', 'it', 'ne', 'ko', 'de']

    tr = Translator()

    icon = "https://images-ext-2.discordapp.net/external/2FdKTBe_yKt6m5hYRdiTAkO0i0HVPkGDOF7lkxN6nO8/%3Fsize%3D128%26overlay/https/crafatar.com/avatars/5d3e654c29bb4ae59e3a5df78372597b.png"

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

    # コマンドグループを定義っ！！！
    story = SlashCommandGroup('story', 'test')

    @story.command(name="get", description="謎の物語を表示します")
    async def story_get(
            self,
            ctx: discord.ApplicationContext,
    ):
        embed = discord.Embed(
            color=0x1e90ff, description="".join(HogestoryCog.read_yaml()))
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=HogestoryCog.icon)
        await ctx.respond(embed=embed)

    # いつどこランダム排出
    @story.command(name="shuffle", description="謎の物語をシャッフルします")
    async def story_shuffle(
            self,
            ctx: discord.ApplicationContext,
    ):
        story = HogestoryCog.read_yaml()
        random.shuffle(story)
        embed = discord.Embed(
            color=0x1e90ff, description=''.join(story))
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=HogestoryCog.icon)
        await ctx.respond(embed=embed)

    @story.command(name="set", description="謎の物語に文章を追加します。最初に「ところで」や「しかし」など接続詞をいれるとランダム抽出でいい感じになります。")
    async def story_set(
        self,
        ctx: discord.ApplicationContext,
        content: Option(str, required=True, description="追加する文章（短いほうが面白いです）を設定してください。最初に「ところで」や「しかし」など接続詞をいれるとランダム抽出でいい感じになります。", ),
    ):

        hogedata = HogestoryCog.read_yaml()
        hogedata.append(content)
        HogestoryCog.write_yaml(hogedata)
        point.GamesCog.getpoint(ctx.author.id,ctx.author.name,10000)
        await ctx.respond(f"追加ありがとう！10,000円が追加されました。")
        embed = discord.Embed(color=0x1e90ff, description=f"{content}を追加しました。")
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=HogestoryCog.icon)
        await ctx.respond(embed=embed)

    @story.command(name="remove", description="謎の物語から文章を削除します。")
    async def story_remove(
        self,
        ctx: discord.ApplicationContext,
        content: Option(str, required=True, description="削除する文章を設定してください。", ),
    ):
        story = HogestoryCog.read_yaml()
        result = f'{content}はストーリーに含まれていません'

        if content in story:
            story.remove(content)
            HogestoryCog.write_yaml(story)
            result = "処理が完了しました"

        embed = discord.Embed(color=0x1e90ff, description=result)
        embed.set_footer(text="made by CinnamonSea2073",
                         icon_url=HogestoryCog.icon)
        await ctx.respond(embed=embed)

    @story.command(name='trans', description='謎の物語を再翻訳で支離滅裂な文章に変換します')
    async def storytrans(
        self,
        ctx,
        loop: Option(int, description='再翻訳回数を上げて精度を低めます デフォルト loop=1',
                     min_value=1, max_value=5, default=1, required=False)
    ):
        story = ''.join(HogestoryCog.read_yaml())
        await ctx.respond(f'翻訳前 :\n{story}')
        dest_word = HogestoryCog.random_transe(
            word=story,
            lang='ja',
            loop=loop,
            lang_codes=copy.copy(HogestoryCog.lang_codes)
        )
        await ctx.interaction.edit_original_message(content=f'翻訳前 :\n{story}\n翻訳後 :\n{dest_word}')


def setup(bot):
    bot.add_cog(HogestoryCog(bot))
