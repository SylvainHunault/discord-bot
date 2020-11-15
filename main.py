import discord
from emoji import EMOJI_ALIAS_UNICODE as EMOJIS
from discord.ext.tasks import loop
from datetime import datetime
from datetime import date

# How To:
##  Mention a user
###  await channel.send("Message received <@%s>".format(user.id))
##  Talk to user in private message
###  await user.send("Reaction received!")
## Write message that will auto delete
### await channel.send("Hello I will auto delete myselff in 5 seconds!", delete_after=5.0)

VERSION = "1.0.0"
HELP_MSG = """
this is a help message
"""

# Fill in those variables for your discord server, the channel the bot will use,
# the specific reactions it will inspect and the roles it will manage.
GENERAL_CHANNEL_ID=#FILL IN with the ID of a channel
ROLE_MANAGEMENT_CHANNEL_ID=#ILL IN with ID of channel to manage roles
GUILD_ID=#FILL IN with server ID
# The emoji package is very usefull to get the emojis you want by using the same text discord chat uses
EMOJI_A=EMOJIS[':white_check_mark:']
EMOJI_B=EMOJIS[':x:']
EMOJI_TEST=EMOJIS[':dragon_face:']
ROLE_A_ID=#FILL IN with ROLE ID on your server
ROLE_B_ID=#FILL IN with the role ID you want on your server

class MyClient(discord.Client):
    # Saves the msg used to manage the roles
    def init(self):
        self.role_mngmt_msg = ""

    def is_me(self,m):
        return m.author == self.user

    async def on_ready(self):
        print("Ready roaaarrr!")
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # Remove messages in the channel ROLE_MANAGEMENT, write a message and give it 2 reactions
        channel = self.get_channel(ROLE_MANAGEMENT_CHANNEL_ID)
        await channel.purge(limit=100, check=self.is_me)
        self.role_mngmt_msg = await channel.send("React to "+EMOJI_A+"for role A or "+EMOJI_B+"for role B")
        await self.role_mngmt_msg.add_reaction(EMOJI_A)
        await self.role_mngmt_msg.add_reaction(EMOJI_B)
        self.my_background_task.start()

    async def on_message(self, message):
        channel = message.channel
        # We do not want the bot the react to itself
        if message.author == self.user.id:
            return
        if message.content == "b!version":
            await channel.send(VERSION)
        elif message.content == "b!help":
            await channel.send(HELP_MSG)

    async def on_reaction_add(self, reaction, user):
        channel = reaction.message.channel
        #discord.utils.get(client.get_all_channels(), id=payload.channel_id)
        emoji = reaction.emoji
        message = reaction.message

        # We do not want the bot to react to its own reactions ever
        if user.id == client.user.id:
            return

        # Get guild then roles
        guild = discord.utils.get(client.guilds, id=GUILD_ID)
        role_a = guild.get_role(ROLE_A_ID)
        role_b = guild.get_role(ROLE_B_ID)
        # Handle reactions from post to change roles and ackownledge in the channel via a temporary message
        # then remove reaction once handled
        if message.id == self.role_mngmt_msg.id:
            if emoji == str(""+EMOJI_A):
                await user.add_roles(role_a)
                await user.remove_roles(role_b)
                await channel.send("<@{s}> you have been added to {a} and removed from {b}!".format(s=user.id, a=role_a.mention, b=role_b.mention), delete_after=2.0)
            elif emoji == str(""+EMOJI_B):
                await user.add_roles(role_b)
                await user.remove_roles(role_a)
                await channel.send("<@{s}> you have been added to {b} and removed from {a}!".format(s=user.id, b=role_b.mention, a=role_a.mention), delete_after=2.0)
            await reaction.remove(user)

# Background task that sends a message very minute
    @loop(minutes=1)
    async def my_background_task(self):
        day = date.today()
        weekday = day.weekday()
        time = datetime.now()
        channel = self.get_channel(GENERAL_CHANNEL_ID)
        await channel.send(EMOJI_TEST+" {t}".format(t=time))
        if(weekday==5):
            await channel.send("Today is Saturday! Yeah!")

    @my_background_task.before_loop
    async def my_background_task_before(self):
        await self.wait_until_ready()

# This token is secret, do not reveal, do not commit publically.
# Bot token from: https://discord.com/developers/application > application > bot > token
# Read token from local file token.txt
my_token_file = open("token.txt", "r")
# Read token without the \n at the end of the line, maybe there is better way to do this
token = my_token_file.readline().split('\n')[0]
client = MyClient()
client.run(token)
