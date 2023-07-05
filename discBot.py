import discord 
from discord.ext import commands
from discord import app_commands
BOT_TOKEN = "ABCD" #change this to your own bot token

BOT_CHANNEL =  1234 #change this to your own bot channel

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix = commands.when_mentioned_or("!"), intents = intents)

mygroup = app_commands.Group(name="greetings", description="Welcomes users")

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
    embed = discord.Embed(title="Welcome to the server", 
                          description="Welcome to the server {}".format(member.mention), 
                          colour = discord.Colour.random())
    embed.set_author(name="{}".format(name))
    embed.set_thumbnail(url="{}".format(pfp))
    embed.add_field(name="This is field", value="This field is just a value")
    embed.set_footer(text="Hope you enjoy your time in this server!")
    ##await channel.send("Welcome to the server {}".format(member.mention))
    await channel.send(embed=embed)
    
@bot.event
async def on_member_remove(member):
    channel = bot.get_channel(BOT_CHANNEL)
    await channel.send("Goodbye, you will be missed")
    
@bot.event
async def on_message(message):
    author = message.author
    content = message.content
    print("{}: {}".format(author,content))

@bot.event
async def on_message_delete(message):
    author = message.author
    content = message.content
    channel = message.channel
    await channel.send("{}: {}".format(author,content))

@bot.event
async def on_message_edit(before,after):
    if before.author == bot.user:
        return;
    author = before.author
    before_content = before.content
    after_content = after.content
    channel = before.channel
    await channel.send("{}: {}".format(author,before_content))
    await channel.send("{}: {}".format(author,after_content))

@bot.event
async def on_reaction_add(reaction,user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message
    await channel.send("{} has reacted with {} to the message {}".format(name,emoji, content))

@bot.event
async def on_reaction_remove(reaction,user):
    channel = reaction.message.channel
    name = user.name
    emoji = reaction.emoji
    content = reaction.message
    await channel.send("{} has removed their reaction of {} to the message {}".format(name,emoji, content))

@bot.command()
async def ping(ctx):    
    message = await ctx.send("Pong!")
    await ctx.add_reaction("🏓") #can be either ctx or message

@bot.command()
async def delete(ctx, user:discord.User):
    async for message in ctx.channel.history(limit = None):
        if message.author == user and message.id != ctx.message.id:
            await message.delete()  

@bot.tree.command(description="Greets user")
async def hello(interaction: discord.Interaction):
    await interaction.response.send_message(f"Hey {interaction.user.mention}!")

@mygroup.command(description="Pings user")
async def ping(interaction: discord.Interaction):
    await interaction.response.send_message(f"Ping {interaction.user.mention}!")

@mygroup.command(description="Pongs user")
async def pong(interaction: discord.Interaction):
    await interaction.response.send_message(f"Pong {interaction.user.mention}!")

bot.run(BOT_TOKEN)