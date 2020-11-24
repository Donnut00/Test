from pyrogram import Client, filters
from pyrogram.errors import UsernameNotOccupied, UsernameInvalid, UserNotParticipant, ChatWriteForbidden, UserAdminInvalid
from pyrogram.types import User
from pyrogram.raw import functions, types
import time
import os, sys




app = Client(
    "my_account",
    api_id=1584235,
    api_hash="9c540b7e922620d2b5c7c43ae1d28ba4"
)



@app.on_message(filters.command(["adduser"]) & filters.outgoing)
def add_member(Client, message) -> object:
    chatid = message.chat.id
    if len(message.text.split()) < 1:
        message.delete()
        message.reply("/adduser <**nome utente**>")
        return
    else:
        try:
            app.add_chat_members(chatid, message.text.split()[1])
            app.send_message(chatid, "Utente Aggiunto")

        except UsernameNotOccupied:
            app.send_message(chatid, "Utente Non Trovato")
        except UsernameInvalid:
            app.send_message(chatid, "Nome Utente Invalido")
        except UserAdminInvalid:
            app.send_message(chatid, "Non hai i permessi necessari per aggiungere gli utenti")
        except IndexError:
            message.reply("/adduser <**nome utente**>")
    return

@app.on_message(filters.command(["removeuser"]) & filters.outgoing)
def remove_member(Client, message):
    chatid = message.chat.id
    if len(message.text.split()) < 1:
        message.delete()
        message.reply("/removeuser <**nome utente**>")
    else:
        try:
            app.kick_chat_member(chatid, message.text.split()[1])
            app.send_message(chatid, "Utente Bannato")
        except UserNotParticipant:
            app.send_message(chatid, "L'utente non fa parte della chat")
        except UserAdminInvalid:
            app.send_message(chatid, "Non hai i permessi necessari per rimuovere l'utente")
        except IndexError:
            message.reply("/removeuser <**nome utente**>")

@app.on_message(filters.command(["CoFounder"]))
def promote_member(Client, message):
    chatid = message.chat.id
    if len(message.text.split()) < 1:
        app.send_message(chatid, "/Cofounder <**nome utente**>")
    else:

        try:
            app.promote_chat_member(chatid, message.text.split()[1], True, True, True, True, True, True, True, True)
            user = message.text.split()[1]
            app.send_message(chatid, f"**UserBot** >> Ho promosso a CoFounder {user}")
        except IndexError:
            app.send_message(chatid, "/CoFounder <**nome utente**>")

@app.on_message(filters.command(["Admin"]) & filters.outgoing)
def promote_to_admin(Client, message):
    chatid = message.chat.id
    if len(message.text.split()) < 1:
        app.send_message(chatid, "/Admin <**nome utente**>")
    else:

        try:
            app.promote_chat_member(chatid, message.text.split()[1], False, True, True, True, True, True, True, False)
            user = message.text.split()[1]
            app.send_message(chatid, f"**UserBot** >> Ho promosso ad Admin {user}")
        except UserNotParticipant:
            print("L'utente non fa parte della chat")
        except UsernameInvalid:
            app.send_message(chatid, "Nome Utente Invalido")
        except UserAdminInvalid:
            print("Non hai i permessi necessari")
        except IndexError:
            app.send_message(chatid, "/Admin <**nome utente**>")

@app.on_message(filters.command(["RemovePermissions"]) & filters.outgoing)
def remove_permissions(Client, message):
    chatid = message.chat.id
    if len(message.text.split()) < 1:
        app.send_message(chatid, "/RemovePermissions <**nome utente**>")
    else:
        try:
            if app.get_chat_member(chatid, message.text.split()[1]).can_edit_messages:
                try:
                    app.promote_chat_member(chatid, message.text.split()[1], False, False, False, False, False, False, False, False)
                    message.delete()
                    user = message.text.split()[1]
                    app.send_message(chatid, f"**UserBot** >> Ho rimosso i permessi a **{user}**")
                except UserNotParticipant:
                    print("L'utente non fa parte della chat")
                except UsernameInvalid:
                    app.send_message(chatid, "Nome Utente Invalido")
                except UserAdminInvalid:
                    print("Non hai i permessi necessari")
                except IndexError:
                    app.send_message(chatid, "/RemovePermissions <**nome utente**>")
        except IndexError:
            app.send_message(chatid, "/RemovePermissions <**nome utente**>")
        else:
            try:
                user = message.text.split()[1]
                app.send_message(chatid, f"L'**UserBot** >> L'utente {user} non è un amministratore")
            except IndexError:
                app.send_message(chatid, f"L'**UserBot** >> L'utente {user} non è un amministratore")

@app.on_message(filters.command(["MessagesCount"]) & filters.outgoing)
def count_messages(Client, message):
    chatid = message.chat.id
    mess_count = app.get_history_count(chat_id=chatid)
    app.send_message(chat_id=chatid, text=f"**UserBot** >> Numero Totale Di Messaggi: **{mess_count}**")

@app.on_message(filters.command(["Spam"]) & filters.outgoing)
def spam(Client, message):
    chatid = message.chat.id
    message_array = message.text.split()
    stopped = False
    counter = 0
    times_to_repeat = 0
    if len(message.text.split()) < 4:
        message.delete()
        message.reply("""
            /spam start <**delay**>  <**numero di volte da ripetere**>  <**messaggio**>
            
        """)
    else:
        if message_array[1] == "start":
            if message_array[2].isnumeric():
                delay = int(message_array[2])
                if message_array[3].isnumeric():
                    if int(message_array[3]) > 20:
                        times_to_repeat = 20
                    else:
                        times_to_repeat = int(message_array[3])
                    if message_array[4] is not None:
                        message.delete()
                        messagei = message_array[4]
                        bad_chars = [',', '[', ']', '\'', '_']
                        for i in bad_chars:
                            messagei = messagei.replace(i, ' ')

                        while not stopped:
                            while counter != times_to_repeat:
                                try:
                                    app.send_message(chatid, f"**UserBotSpam** >> {messagei}")
                                    counter = counter + 1
                                    time.sleep(delay)
                                except ChatWriteForbidden:
                                    get_chat_username = message.chat.username
                                    app.send_message("me", f"Non hai i permessi di scrivere nella chat {get_chat_username}")
                                    stopped = True
                            else:
                                stopped = True


@app.on_message(filters.command(["SpamPhoto"]) & filters.outgoing)
def spam(Client, message):
    chatid = message.chat.id
    message_array = message.text.split()
    stopped = False
    counter = 0
    times_to_repeat = 0
    if len(message.text.split()) < 4:
        message.delete()
        message.reply("""
            /spamphoto start <**delay**>  <**numero di volte da ripetere**>  <**messaggio**>

        """)
    else:
        if message_array[1] == "start":
            if message_array[2].isnumeric():
                delay = int(message_array[2])
                if message_array[3].isnumeric():
                    if int(message_array[3]) > 10:
                        times_to_repeat = 10
                    else:
                        times_to_repeat = int(message_array[3])
                    if message_array[4] is not None:
                        message.delete()
                        messagei = message_array[4]
                        bad_chars = [',', '[', ']', '\'', '_']
                        for i in bad_chars:
                            messagei = messagei.replace(i, ' ')

                        while not stopped:
                            while counter != times_to_repeat:
                                try:
                                    app.send_photo(chatid, message.text.split()[4])
                                    counter = counter + 1
                                    time.sleep(delay)
                                except ChatWriteForbidden:
                                    stopped = True
                                except ValueError:
                                    stopped = True
                                    break
                            else:
                                stopped = True

@app.on_message(filters.command(["SpamGif"]) & filters.outgoing)
def spam(Client, message):
    chatid = message.chat.id
    message_array = message.text.split()
    stopped = False
    counter = 0
    times_to_repeat = 0
    if len(message.text.split()) < 4:
        message.delete()
        message.reply("""
            /spamphoto start <**delay**>  <**numero di volte da ripetere**>  <**messaggio**>

        """)
    else:
        if message_array[1] == "start":
            if message_array[2].isnumeric():
                delay = int(message_array[2])
                if message_array[3].isnumeric():
                    if int(message_array[3]) > 10:
                        times_to_repeat = 10
                    else:
                        times_to_repeat = int(message_array[3])
                    if message_array[4] is not None:
                        message.delete()
                        messagei = message_array[4]
                        bad_chars = [',', '[', ']', '\'', '_']
                        for i in bad_chars:
                            messagei = messagei.replace(i, ' ')

                        while not stopped:
                            while counter != times_to_repeat:
                                try:
                                    app.send_animation(chatid, message.text.split()[4])
                                    counter = counter + 1
                                    time.sleep(delay)
                                except ChatWriteForbidden:
                                    stopped = True
                                except ValueError:
                                    stopped = True
                                    break
                            else:
                                stopped = True

@app.on_message(filters.command(["Godo"]) & filters.outgoing)
def godo(Client, message):
    chatid = message.chat.id
    a = app.send_message(chatid, "__**La goduria sta crescendo**__")
    b = a.message_id
    message_id = int(a.message_id)
    try:
        app.send(
            message.delete(),
            a,
            app.edit_message_text(chatid, b, text="__**La goduria sta crescendo.**__"),
            time.sleep(0.5),
            app.edit_message_text(chatid, b, text="__**La goduria sta crescendo..**__"),
            time.sleep(0.5),
            app.edit_message_text(chatid, b, text="__**La goduria sta crescendo...**__"),
            time.sleep(2),
            app.edit_message_text(chatid, message_id, text="**DONUT STA GODENDO MADONNA DE DIO**")
        )
    except AttributeError:
        pass
    except TypeError:
        pass

@app.on_message(filters.command(["GetStatus"]) & filters.outgoing)
def get_status(Client, message):
    chatid = message.chat.id
    arguments = len(message.text.split())

    if len(message.text.split()) < 1:
        message.delete()
        message.reply("/GetStatus <**nome utente**>")
    else:
        try:
            status = app.get_users(message.text.split()[1]).status
            nick = message.text.split()[1]
            app.send_message(chatid, f"**UserBot** >> Status Di @{nick}: **{status}**")
        except UsernameInvalid:
            message.reply("Nome Utente Invalido")
        except UsernameNotOccupied:
            message.reply("Utente Non Trovato")
        except IndexError:
            message.reply("/GetStatus <**nome utente**>")

@app.on_message(filters.command(["CheckVoip"]) & filters.outgoing)
def check_voip(Client, message):
    chatid = message.chat.id
    if len(message.text.split()) < 1:
        pass
    else:
        try:
            dc = app.get_users(message.text.split()[1]).dc_id
            user = message.text.split()[1]
            print(dc)
        except UsernameInvalid:
            message.reply("Nome Utente Invalido")
        except UsernameNotOccupied:
            message.reply("Utente Non Trovato")
        except IndexError:
            message.delete()
            message.reply("/CheckVoip <**nome utente**>")

        try:
            if dc == 1 or dc == 3:
                app.send_message(chatid, f"{user} appartiene al dc numero {dc}, potrebbe essere un voip")
            else:
                if dc == None:
                    message.reply("L'utente non ha una foto profilo")

                else:
                    message.reply("L'utente non appartiene al DC 1 o 3, potrebbe non essere voip")
        except UnboundLocalError:
            pass


@app.on_message(filters.command(["HelpBot"]) & filters.outgoing)
def helpCommand(Client, message):
    chatid = message.chat.id
    app.send_message(chatid, """
    **USERBOT COMMANDS**
/adduser (Aggiungi un utente)

/removeuser (Rimuovi un utente)

/CoFounder (Promuovi un utente a CoFounder)

/Admin (Promuovi un utente ad Admin)

/RemovePermissions (Rimuovi i permessi da amministratore)

/GetStatus (Status di un utente)

/CheckVoip (Check DC di un utente)

/MessagesCount (Conta i messaggi inviati nella chat)

/spam start (Floodda un messaggio)

/spamphoto start (Floodda una foto)

/spamgif start (Floodda una gif)

/godo (Letteralmente Godo)
    
    
    """)

app.run()


