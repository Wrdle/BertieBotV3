import discord
from discord.ext import commands
import time
import threading
import zmq

TOKEN = open("token.txt", "r").read()

client = commands.Bot(command_prefix = '.')

@client.event
async def on_ready():
    print('Bot is ready')

@client.command(pass_context=True)
async def echo(ctx):
    await client.say('ServerID: ' + ctx.message.server.id)
    await client.say('ChannelID: ' + ctx.message.channel.id)
    channel = client.get_channel(ctx.message.channel.id)
    print(type(channel.id))
    await client.send_message(channel, 'oof')

@client.command()
async def oof():
    await client.say('Testing')


def TCP():
    context = zmq.Context()
    socket = context.socket(zmq.REP)
    socket.bind("tcp://*:5555")

    while True:
        #  Wait for next request from client
        messageraw = str(socket.recv())[2:-1]
        message = messageraw.split(" ")

        # ALLCHANNELS, SPECIFICCHANNEL, USER, ROLE
        if message[0].upper() == 'ALLCHANNELS' and message[1].upper() == 'FROM':
            server = client.get_server(message[2])
            results = server.channels
            for x in results:
                print(x.name)

            socket.send(b'It Works!')

        elif message[0].upper() == 'SPECIFICCHANNEL':
            socket.send(b'SPECIFICCHANNEL')
        elif message[0].upper() == 'USER':
            socket.send(b'USER')
        elif message[0].upper() == 'ROLE':
            socket.send(b'ROLE')
        else:
            socket.send(b'Server Error')

tcpThread = threading.Thread(target=TCP)
tcpThread.start()

client.run(TOKEN)
