import interactions
import json
import requests

with open('./config.json', 'r') as f:
  data = json.load(f)

def write_json(new_data, filename='data.json'):
    with open(filename,'r+') as file:
        file_data = json.load(file)
        file_data["link"].append(new_data)
        file.seek(0)
        json.dump(file_data,file,indent=4)

URL = "http://"+data["ServerIP"]+":"+data["ServerPort"]+"/dynamic.json"        
        
bot = interactions.Client(token=data["token"])

if data["richpresense"]:
@bot.event()
async def on_ready():
    while True:
        try:
            r = requests.get(url=URL)
            UrlData = r.json()
            await bot.change_presence(interactions.ClientPresence(activities=[interactions.PresenceActivity(name=str(UrlData["clients"])+" / "+str(UrlData["sv_maxclients"])+" Joueurs ❤️‍🔥",type=interactions.PresenceActivityType.GAME)]))
        except:
            await bot.change_presence(interactions.ClientPresence(activities=[interactions.PresenceActivity(name="Serveur éteint",type=interactions.PresenceActivityType.GAME)]))
        await asyncio.sleep(60)


if data["SlashCommand"]:
    @bot.command(
        name="form",
        description="Affiche l'embed pour le formulaire de whitelist",
        default_member_permissions=interactions.Permissions.MANAGE_ROLES,
        scope=int(data["guildId"]),
    )
    async def formulaire(ctx: interactions.CommandContext):
        button = interactions.Button(
            style=interactions.ButtonStyle.PRIMARY,
            label="Formulaire",
            custom_id="question"
        )
        row = interactions.ActionRow(components=[button])
        #######################################################
        #########   Vous devez modifier l'embed ###############
        #######################################################

        embed = interactions.Embed(title="Douane", color=0x318bdb,   description="Bienvenue sur notre serveur !")
        embed.set_author(name="Reglement",icon_url="https://craftaria.fr/img/reglement-craftaria.png")
        embed.add_field(name="1 ère étape",value="Mettre le texte souhaitez")
        embed.add_field(name="2 ème étape",value="Mettre le texte souhaitez")
        embed.add_field(name="3 ème étape",value="Mettre le texte souhaitez")
        embed.set_image("https://craftaria.fr/img/reglement-craftaria.png")
        await ctx.send(embeds=embed, components=row)

@bot.component("question")
async def send_modal(ctx: interactions.CommandContext):
    modal = interactions.Modal(
        title="Formulaire",
        custom_id="form",
        components=[
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                custom_id="name",
                label="Votre nom et prénom RP."
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                custom_id="age",
                label="Votre âge."
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                custom_id="bg",
                label="Votre Background(Lien GDOC UNIQUEMENT)."
            ),
            interactions.TextInput(
                style=interactions.TextStyleType.SHORT,
                custom_id="rp",
                label="Orientation RP.",
                placeholder="Civil,LSDP,BCSO,EMS,Illégal"
            )
        ]
    )

    await ctx.popup(modal)

@bot.modal("form")
async def modal_response(ctx : interactions.CommandContext, name: str,age: str,bg: str,rp: str):
    user = ctx.author
    userid = user.id
    userid = int(userid)
    ##########################################################
    ############    BUTTONS pour les reponse    ##############
    ##########################################################
    refus = interactions.Button(
        style=interactions.ButtonStyle.DANGER,
        label="Refusé",
        custom_id="refus"
    )
    second = interactions.Button(
        style=interactions.ButtonStyle.DANGER,
        label="2 eme chance",
        custom_id="second"
    )
    wait = interactions.Button(
        style=interactions.ButtonStyle.SECONDARY,
        label="En attente de whitelist (RP)",
        custom_id="sanspapier"
    )
    whitelist = interactions.Button(
        style=interactions.ButtonStyle.SUCCESS,
        label="Whitelisté",
        custom_id="whitelist"
    )
    if data["secondechance"]:
        row = interactions.ActionRow(components=[refus,second,wait,whitelist])
    else:
        row = interactions.ActionRow(components=[refus,wait,whitelist])
    ###########################################################
    ############    Embed au formulaire STAFF    ##############
    ###########################################################
    embed = interactions.Embed(title=f"Formulaire de {user}",color=0x318bdb)
    embed.add_field(name="Nom et prenom RP", value=name)
    embed.add_field(name="Age", value=age)
    embed.add_field(name="Background", value=bg)
    embed.add_field(name="Orientation RP", value=rp)
    embed.add_field(name="ID Discord",value=userid)
    channel = interactions.Channel(** await bot._http.get_channel(data["StaffChannel"]), _client=bot._http)
    if data["ChannelLog"]:
        channellog = interactions.Channel(** await bot._http.get_channel(data["LogChannel"]), _client=bot._http)
    f = open('data.json')
    dataload = json.load(f)
    reply = False
    for i in dataload["link"]:
        if i["playerid"] == userid and not (i["msg"] == 0):
            reply = True
    if reply == False:
        await ctx.send("Les douanier ont bien recu ton formulaire, merci de bien vouloir patientez dans le channel \"attente de douane\"",ephemeral=True)
        msg = await channel.send(embeds=embed, components=row)
        value = {"msg":int(msg.id),"playerid":int(userid)}
        write_json(value)
        if data["ChannelLog"]:
            await channellog.send(embeds=embed)
    else:
        await ctx.send("tu as deja envoyer ton formulaire au douanier",ephemeral=True)


@bot.component("whitelist")
async def whitelist(ctx : interactions.CommandContext):
    ############################################################
    ############    Embed au envoyer au joueur    ##############
    ############################################################
    embed = interactions.Embed(title=f"Passage de douane",color=0x00FF00)
    embed.add_field(name="**Félicitations !**", value="Bravo, maintenant tu es arrivé en ville avec tes papiers en poches, bon courage et bon jeu !")
    with open('data.json') as f:
        dataload = json.load(f)
    for i in dataload["link"]:
        if i["msg"] == ctx.message.id:
            userid = i["playerid"]
            i["msg"] = 0
            with open ("data.json", "w") as f:
                json.dump(dataload, f)
    member = interactions.Member(**await bot._http.get_member(data["guildId"],userid),_client=bot._http)
    await ctx.message.delete()
    await member.add_role(data["roleWhitelist"],data["guildId"])
    await member.remove_role(data["roleSemiWhitelist"],data["guildId"])
    await member.remove_role(data["roleUnWhitelist"],data["guildId"])
    await member.send(embeds=embed)
    await ctx.send("Envoyé",ephemeral=True)

@bot.component("sanspapier")
async def sanspapier(ctx : interactions.CommandContext):
    ############################################################
    ############    Embed au envoyer au joueur    ##############
    ############################################################
    embed = interactions.Embed(title=f"Passage de douane",color=0x00FFFF)
    embed.add_field(name="**Félicitations !**", value="Bravo, maintenant tu peux te rendre en jeu et un douanier va te donner tes papiers nécessaire à ton intégration à Los Santos.")
    with open('data.json') as f:
        dataload = json.load(f)
    for i in dataload["link"]:
        if i["msg"] == ctx.message.id:
            userid = i["playerid"]
    member = interactions.Member(**await bot._http.get_member(data["guildId"],userid),_client=bot._http)
    await member.add_role(data["roleSemiWhitelist"],data["guildId"])
    await member.remove_role(data["roleUnWhitelist"],data["guildId"])
    await member.send(embeds=embed)
    await ctx.send("Envoyé",ephemeral=True)

if data["secondechance"]:
    @bot.component("second")
    async def second(ctx : interactions.CommandContext):
        #Chercher dans le fichier data.json l'id du joueur
        with open('data.json') as f:
            dataload = json.load(f)
        for i in dataload["link"]:
            if i["msg"] == ctx.message.id:
                userid = i["playerid"]
                msgid = i["msg"]
        member = interactions.Member(**await bot._http.get_member(data["guildId"],userid),_client=bot._http)
        lien = f"https://discord.com/channels/"+str(data["guildId"])+"/"+str(data["StaffChannel"])+"/"+str(msgid)
        ############################################################
        ############    Embed au envoyer au joueur    ##############
        ############################################################
        embed = interactions.Embed(title=f"Passage de douane",color=0xFF641E)
        embed.add_field(name="Seconde chance !", value="Malheureusement, tu n'as pas réussis ton passage en douane mais tu as le droit à une seconde chance profites-en !")
        ##################################################################################
        ############    Embed au envoyer au staff pour la seconde chance    ##############
        ##################################################################################
        embedseconde = interactions.Embed(title=f"Seconde chance de {member}",color=0xFF641E)
        embedseconde.add_field(name="Id Discord",value=int(member.id))
        embedseconde.add_field(name="lien vers le formulaire",value=lien)
        #channel staff
        channel = interactions.Channel(** await bot._http.get_channel(data["secondchannel"]), _client=bot._http)
        await ctx.send("Envoyé",ephemeral=True)
        #send dans le channel staff
        await channel.send(embeds=embedseconde)
        #envoye au joueur
        await member.send(embeds=embed)


@bot.component("refus")
async def refus(ctx : interactions.CommandContext):
    ############################################################
    ############    Embed du envoyer au joueur    ##############
    ############################################################
    embed = interactions.Embed(title=f"Passage de douane",color=0xFF0000)
    embed.add_field(name="Refusé !", value="Malheureusement, tu n'as pas réussis ton passage en douane, nous te souhaitons une bonne continuation !")
    with open('data.json') as f:
        dataload = json.load(f)
    for i in dataload["link"]:
        if i["msg"] == ctx.message.id:
            userid = i["playerid"]
            i["msg"] = 0
            with open ("data.json", "w") as f:
                json.dump(dataload, f)
    member = interactions.Member(**await bot._http.get_member(data["guildId"],userid),_client=bot._http)
    await ctx.message.delete()
    await member.send(embeds=embed)
    await ctx.send("Envoyé",ephemeral=True)

bot.start()
