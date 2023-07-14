import discord
from discord.ext import commands
from discord import app_commands
import requests

BOT_TOKEN = "ABCD" #change this to your own bot token

BOT_CHANNEL = 1234 #change this to your own bot channel

intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix= commands.when_mentioned_or('!'), intents=intents)

mygroup = app_commands.Group(name="greetings", description="Welcomes Users")

blockWords = ["lol","test","mad"]

@bot.event
async def on_ready():
    print("Bot is ready")

    bot.tree.add_command(mygroup)

    try:
        synced = await bot.tree.sync()
        print(f'Synced {len(synced)} Command(s)')
    except Exception as e:
        print(e)

@bot.event
async def on_member_join(member):
    channel = bot.get_channel(BOT_CHANNEL)
    name = member.display_name
    pfp = member.display_avatar
    embed = discord.Embed(title="Welcome to this discord channel", 
                          description="It is a very cool channel", 
                          colour=discord.Colour.random())
    embed.set_author(name="{}".format(name))
    embed.set_thumbnail(url="{}".format(pfp))
    embed.add_field(name="This is a field", value="This field is just a value")
    embed.set_footer(text="Hope you enjoy your time in this server!")
    await channel.send(embed=embed)

@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(BOT_CHANNEL)
    await channel.send("Goodbye, you will be deeply missed :(")

@bot.event
async def on_message(message):
    author = message.author
    content = message.content
    await bot.process_commands(message)
    print("{}: {}".format(author, content))
    if message.author != bot.user:
        for text in blockWords:
            if "Moderator" not in str(message.author.roles) and text.lower() in str(message.content.lower()):
                await message.delete()
                await message.channel.send("Please don't use that word here!")
                return

@bot.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await channel.send("{}: {}".format(author, content))

@bot.event
async def on_message_edit(before, after):
    if before.author == bot.user: 
        return
    author = before.author
    pfp = author.display_avatar
    before_content = before.content
    after_content = after.content
    channel = before.channel
    embed = discord.Embed(title="Changes were made", colour=discord.Colour.random())
    embed.set_author(name="{}".format(author))
    embed.set_thumbnail(url="{}".format(pfp))
    embed.add_field(name="Before:", value="{}".format(before_content), inline=False)
    embed.add_field(name="After:", value="{}".format(after_content))
    await channel.send(embed=embed)

    ## await channel.send("Before: {}".format(before_content))
    ## await channel.send("After: {}".format(after_content))

@bot.event
async def on_reaction_add(reaction, user):
    if user == bot.user:
        return
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send("{} has added {} to the message: {}".format(name, emoji, content))

@bot.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message.content
    await channel.send("{} has removed {} to the message: {}".format(name, emoji, content))

@bot.command()
async def ping(ctx):
    mention = await ctx.send("pong")
    await ctx.message.add_reaction("🏓")

@bot.command()
async def delete(ctx, user: discord.User):
    async for message in ctx.channel.history(limit=None):
        if message.author == user:
            await message.delete()
            break

@bot.command()
@commands.has_any_role("Moderator")
async def ban(ctx, user:discord.Member):
    print(str(ctx.author.roles)+"hi")
    if user in ctx.guild.members:
        await user.ban()
        await ctx.send(f"Banned user: {user.display_name} for reason of treason!")
    else:
        await ctx.send("User not found")

@bot.command()
@commands.has_any_role("Moderator")
async def unban(ctx, name:str):
    notFound = True
    async for entry in ctx.guild.bans(limit = None):
        user = entry.user
        entryName = user.display_name
        if entryName == name:
            await ctx.guild.unban(user)
            await ctx.send(f"User: {user.display_name} has been unbanned!")
            notFound = False
    if notFound == True:
        await ctx.send("User not found")

def get_joke(category):
    if category == 'general':
        joke_url = 'https://official-joke-api.appspot.com/random_joke'
        try:
            response = requests.get(joke_url)
            joke_data = response.json()
            if 'setup' in joke_data and 'punchline' in joke_data:
                return f"{joke_data['setup']}\n{joke_data['punchline']}"
        except requests.exceptions.RequestException:
            pass
    elif category == 'dadjokes':
        joke_url = 'https://icanhazdadjoke.com/'
        headers = {'Accept': 'application/json'}
        try:
            response = requests.get(joke_url, headers=headers)
            joke_data = response.json()
            if 'joke' in joke_data:
                return joke_data['joke']
        except requests.exceptions.RequestException:
            pass
    return None

@bot.command()
async def joke(ctx, category=None):
    if not category:
        category = 'general'

    joke = get_joke(category)
    if joke:
        await ctx.send(joke)
    else:
        await ctx.send("Sorry, I couldn\'t find a joke at the moment.")

@bot.tree.command(description='Greets user')
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f'Hey {interaction.user.mention} !')

@mygroup.command(description='Pings user')
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f'Ping {interaction.user.mention} !')

@mygroup.command(description='Pongs user')
async def pong(interaction: discord.Interaction):
    await interaction.response.send_message(f'Pong {interaction.user.mention} !')

bot.run(BOT_TOKEN)