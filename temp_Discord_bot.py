import discord
from discord.ext import commands
import random
import asyncio

description = '''Bot created for the JSU Esports club to help make it a fun moderated community.'''
Client = discord.Client()
client = commands.Bot(command_prefix='?', description=description)
server = object()


@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    global server
    for serv in client.servers:
        server = serv
    print(str(server))
    print('------')


@client.command()
async def add(left : int, right : int):
    """Adds two numbers together."""
    await client.say(left + right)
    

@client.command()
async def roll(dice : str):
    """Rolls a dice in NdN format."""
    try:
        rolls, limit = map(int, dice.split('d'))
    except Exception:
        await client.say('Format has to be in NdN!')
        return

    result = ', '.join(str(random.randint(1, limit)) for r in range(rolls))
    await client.say(result)
    
@client.command()
async def flip():
    """Flips a coin and displays the result to the user"""
    coin = ["Heads", "Tails"]
    await client.say("The coin landed on " + random.choice(coin) + "!")
    
@client.command()
async def prune():
    """ADMIN/MOD ONLY: Allows an admin or moderator to remove inactive members from the server"""
    try:
        num_to_remove = await client.estimate_pruned_members(server=server, days=30)
        await client.say(str(num_to_remove) + " inactive members will be removed!")
        num_removed = await client.prune_members(server=server, days=30)
        await client.say(str(num_removed) + " inactive members were removed!")
    except discord.Forbidden:
        await client.say("You don't have permissions to use this command!")
    except discord.HTTPException:
        await client.say("The request was unable to be processed.")
    except discord.InvalidArgument:
        await client.say("Arguments supplied were invalid!")
    
    
@client.command()
async def lmgtfy(*search : str):
    """Takes a phrase and displays a Let Me Google That For You link with that phrase"""
    link_string = "http://lmgtfy.com/?q="
    for string in search:
        if string == search[len(search) - 1]:
            link_string += string
        else:
            link_string += string + "%20"
    await client.say(link_string)

@client.command()
async def role(member : str, role : str):
    """ADMIN/MOD ONLY: Allows a moderator or admin to set a role for a member"""
    moderator_role = discord.utils.get(server.roles, name="Sith Lords")
    admin_role = discord.utils.get(server.roles, name="admin")
    memberObj = server.get_member_named(member)
    if moderator_role in memberObj.roles or admin_role in memberObj.roles:
        roleObj = discord.utils.get(server.roles, name=role)
        try:
            await client.add_roles(memberObj, roleObj)
            await client.say(member + " was added to " + role + " role!")
        except discord.Forbidden:
            await client.say("No permission to add roles!")
        except discord.HTTPException:
            await client.say("Adding roles failed!")
    else:
        await client.say("You have no power here!")

@client.command(description='For when you wanna settle the score some other way')
async def choose(*choices : str):
    """Chooses between multiple choices."""
    await client.say(random.choice(choices))

@client.command()
async def repeat(times : int, content='repeating...'):
    """Repeats a message multiple times."""
    for i in range(times):
        await client.say(content)

@client.command()
async def joined(member : discord.Member):
    """Says when a member joined."""
    await client.say('{0.name} joined in {0.joined_at}'.format(member))
    
@client.command()
async def membersJoined():
    members = server.members
    for member in members:
        await client.say('{0.name} joined in {0.joined_at}'.format(member))

client.run('MzQ0MTI1NjE5NDM0NTUzMzQ0.DGoLgw.-JCP8SuSyMNoLbXuwn1jswapODA')