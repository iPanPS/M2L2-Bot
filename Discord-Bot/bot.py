import discord
from discord.ext import commands
import random
import os
import requests
description = '''An example bot to showcase the discord.ext.commands extension
module.'''

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

bot = commands.Bot(command_prefix='?', description=description, intents=intents)

@bot.event
async def on_ready():
    print(f'We have logged in as {bot.user}')

async def on_member_join(self, member):
    guild = member.guild
    if guild.system_channel is not None:
        to_send = f'Welcome {member.mention} to {guild.name}!'
        await guild.system_channel.send(to_send)

@bot.command()
async def hello(ctx):
    await ctx.send(f'Hi! I am a bot {bot.user}!')

@bot.command()
async def roll(ctx, dice: str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await ctx.send('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await ctx.send(result)


@bot.command(description='For when you wanna settle the score some other way')
async def choose(ctx, *choices: str):
    """Chooses between multiple choices."""
    await ctx.send(random.choice(choices))

@bot.command()
async def joined(ctx, member: discord.Member):
    """Says when a member joined."""
    await ctx.send(f'{member.name} joined {discord.utils.format_dt(member.joined_at)}')

@bot.command()
async def repeat(ctx, times: int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await ctx.send(content)

@bot.command()
async def meme(ctx):
    img_name = random.choice(os.listdir('images'))
    with open(f'images/{img_name}','rb') as f:
        # Mari simpan file perpustakaan/library Discord yang dikonversi dalam variabel ini!
                    picture = discord.File(f)
   # Kita kemudian dapat mengirim file ini sebagai tolok ukur!
    await ctx.send(file=picture)
    
def get_duck_image_url():    
    url = 'https://random-d.uk/api/random'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('duck')
async def duck(ctx):
    '''Setelah kita memanggil perintah bebek (duck), program akan memanggil fungsi get_duck_image_url'''
    image_url = get_duck_image_url()
    await ctx.send(image_url)

def get_meme_image_url():    
    url = 'https://meme-api.com/gimme'
    res = requests.get(url)
    data = res.json()
    return data['url']


@bot.command('random-meme')
async def duck(ctx):
    image_url = get_meme_image_url()
    await ctx.send(image_url)

organik = [
     'daun',
     'sisa makanan',
     'sayur atau buah busuk',
     'ranting pohon',
     'bangkai hewan',
]
anorganik = [
     'plastik',
     'ban bekas',
     'botol plastik',
     'kaca',
     'minyak goreng'
]

@bot.command()
async def cek_sampah(ctx):
     await ctx.send('ketik sampah yang ingin diketahui :')
     msg = await bot.wait_for("message")
     if msg.content in organik:
          await ctx.send(f'buanglah **{msg.content}** di tempat sampah **organik**')
     elif msg.content in anorganik:
          await ctx.send(f'buanglah **{msg.content}** di tempat sampah **anorganik**')
     else:
          return await ctx.send(f'**{msg.content}** belum masuk daftar sampah')

bot.run("token")
