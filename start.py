import discord
import json
import requests


with open('secrets.json') as file_object:
    data = json.load(file_object)
    file_object.close()
    token = data["token"]
    name = data["name"]
    app_id = data["app_id"]
    permissions = data["permissions"]
    panel_api_key = data["panel_api_key"]
    serverID = data["serverID"]
    panelURL = data["panelURL"]
    print(name)



intents = discord.Intents.default()
intents.message_content = True

bot = discord.Bot(intents=intents)

@bot.event
async def on_ready():
    print("Ready!")

@bot.slash_command()
async def connected(ctx):
    name = ctx.author.name
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'Authorization': 'Bearer apikey',
    }
    response = requests.get((panelURL + 'api/application/servers/external/' + serverID), headers=headers)
    content = response.content
    json_response = content.decode('utf-8').replace("'", '"')
    data = json.loads(json_response)
    errorCode = data['errors'][0]['code']
    errorStatus = data['errors'][0]['status']
    errorDetail = data['errors'][0]['detail']
    connectedPlayers = "0/60"
    
    if errorStatus == "401":
        connectedPlayers = "Error"
    
    embed=discord.Embed(title="Atlas Administrator", color=0xfbff00)
    embed.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/5/53/Pok%C3%A9_Ball_icon.svg/1200px-Pok%C3%A9_Ball_icon.svg.png")
    embed.add_field(name="Code", value=errorCode, inline=True)
    embed.add_field(name="Status", value=errorStatus, inline=True)
    embed.add_field(name="Detail", value=errorDetail, inline=True)
    embed.add_field(name="Connected Players", value=connectedPlayers, inline=True)
    await ctx.respond(embed=embed)

print("Invitation Link: https://discord.com/api/oauth2/authorize?client_id=" + app_id + "&permissions=" + permissions + "&scope=bot")
bot.run(token)
