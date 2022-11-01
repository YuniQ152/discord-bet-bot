import discord
from discord import app_commands
from discord.ext import commands, tasks
import os
from dotenv import load_dotenv
from database import *
from random import randint

load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = 785849670092980225

class Bot(commands.Bot):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(command_prefix="..", activity=discord.Activity(type=discord.ActivityType.playing, name="어떻게 봇 이름이 오백원 ㅋㅋ"), intents=intents)

    async def setup_hook(self):
        await self.tree.sync(guild = discord.Object(id = GUILD_ID))
        print(f"logged in as {bot.user} (ID: {bot.user.id})")
        print("------------")
        tasks_loop.start()
    
    # async def on_command_error(self, ctx, error):
    #     await ctx.reply(error, ephemeral = False)

bot = Bot()

@tasks.loop(seconds=10)
async def tasks_loop():
    await bot.wait_until_ready()
    pass

@bot.hybrid_command(name="가입", aliases=["register", "reg", "ㄱㅇ"], with_app_command=True, description="유저 정보를 봇에 등록합니다. 오백원 봇의 도박 등의 기능을 이용하려면 필요합니다.")
# @app_commands.describe(channel="공동농장을 조회할 채널. (입력하지 않을 경우 현재 채널)")
@app_commands.guilds(discord.Object(id = GUILD_ID))
async def register(ctx: commands.Context):
    update_user_data(ctx.author)
    await ctx.defer(ephemeral = True)
    await ctx.reply(f"{ctx.author.mention}님이 가입되었습니다.")

@bot.hybrid_command(name="도박", aliases=["bet", "ㄷㅂ", "eq"], with_app_command=True, description="골드를 걸고 도박을 진행합니다.")
@app_commands.describe(bet="도박할 코인")
@app_commands.guilds(discord.Object(id = GUILD_ID))
async def register(ctx: commands.Context, bet: int):
    update_user_data(ctx.author)
    await ctx.defer(ephemeral = True)

    diamond, gold = load_user_money(ctx.author)
    if gold == 0:
        await ctx.reply(f"보유하고 있는 🪙가 없어서 도박을 진행할 수 없습니다.")
        return
    elif gold == 1:
        await ctx.reply(f"현재 1🪙를 보유하고 있어 1🪙로 도박해야 합니다.")
        return
    if not 1 <= bet <= gold:
        await ctx.reply(f"1🪙와 {gold}🪙 사이로 도박해야 합니다.")
        return

    rand = randint(0, 1)
    if rand == 1: # win
        result = change_user_gold(ctx.author, bet)
        await ctx.reply(f"도박에 성공해서 {bet}🪙를 얻었습니다.\n현재 {result}🪙를 보유하고 있습니다.")
    else: # lose
        result = change_user_gold(ctx.author, bet * -1)
        await ctx.reply(f"{bet}🪙를 걸고 도박했지만 실패했습니다...\n현재 {result}🪙를 보유하고 있습니다.")

bot.run(TOKEN)