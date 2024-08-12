from pyrogram import Client , filters
from datetime import datetime, timedelta
import time , asyncio

n = 0
timer_id = []
timer_confing = {
    'text': 's' ,
    'on' : True ,
    'off' : False ,
    'time' : 2, 
    'stop' : False,
}

config = {
    'name' : "session", # OPTINAL
    'api_id' : API-ID, # NEED A EDIT
    'api_hash' : 'API-HASH', # NEED A EDIT
    'admin' : 000, # NEED A EDIT
    }

app = Client(config['name'],config['api_id'],config['api_hash'])

@app.on_message(filters.me , group = 1)
async def ping(_,message):
    if message.text == "ping":
        await message.reply("online.")

@app.on_message(filters.user(config['admin']) & filters.command("timer"),group=6)
async def timer_online_offline(_,message):
    text = message.text.split()[1]
    if text == "on":
        timer_confing['on'] = True
        timer_confing['off'] = False
        texts = "timer online."
    if text == "off":
        timer_confing['on'] = False
        timer_confing['off'] = True
        texts = "timer offlin."
    await message.reply(texts)

@app.on_message(filters.user(config['admin']) & filters.command("timertext"),group=5)
async def timer_text(client,message):
    if timer_confing['on'] == True:  
        timer_confing['text'] = message.text.replace('/timertext ' , '')
        await message.reply("text saved")
    if timer_confing['off'] == True:
        return
    
@app.on_message(filters.user(config['admin']) & filters.command("settimer"),group=4)
async def timer_time(client,message):
    if timer_confing['on'] == True: 
        time = message.text.split()[1]
        timer_confing['time'] = int(time)
        await message.reply("time seted")
    if timer_confing['off'] == True:
        return
    
@app.on_message(filters.user(config['admin']) & filters.command("start"),group=3)
async def start_time(client,message):
    global timer_id , n 
    chat = message.text.split()[1]
    if timer_confing['on'] == True:  
        timer_confing['stop'] = False
        timer_id.append(1)
        await message.reply("started..!")
        timetimer = timer_confing['time'] 
        current_time = datetime.now()
        timex = int(timetimer)
        sleepX = timex * 60
        n = 0
        for n in range(100):
                scheduled_time = current_time + timedelta(minutes=timex)
                timex += int(timetimer)
                await client.send_message(
                    chat_id=chat,
                    text=timer_confing['text'],  
                    schedule_date=datetime.fromtimestamp(scheduled_time.timestamp()))
                time.sleep(0.5)
                n=+1
    if timer_confing['off'] == True:
        return


                    
@app.on_message(filters.user(config['admin']) & filters.command("ping"),group=2)
async def ping_timer(client,message):
    await message.reply("timer is okay.")


@app.on_message(filters.user(config['admin']) & filters.command("stop"),group=11)
async def stop(client,message):
    global timer_id , n 
    n = 0
    timer_id.append(None) 
    await message.reply("stoped..!")

@app.on_message(filters.user(config['admin']) & filters.command("help"),group=10)
async def help(client,message):
    x = f'/start [id]\n/stop\n/ping\n/settimer (number)\n/timertext (text)'
    await message.reply(x)

@app.on_message(filters.user(config['admin']) & filters.command("restart"),group=12)
async def restart_timer(_,message):
    timer_confing['stop'] = True
    timer_confing['time'] = None
    timer_confing['text'] = None
    
app.run()