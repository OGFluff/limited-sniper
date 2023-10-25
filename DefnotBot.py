# DefnotBot By defnotstevo
import json
import subprocess
import os
import asyncio
import requests
import re
import time
from datetime import datetime, timedelta
try:
    import discord
    from discord.ext import commands
except:
    os.system("pip install discord.py")
try:
    from rgbprint import gradient_print, Color, rgbprint
except:
    os.system("pip install rgbprint")
try:
    import pyautogui
except:
    os.system("pip install pyautogui")
    os.system("pip install Pillow")

os.system("cls")
with open("config.json") as file:
    config = json.load(file)

token = "" # Discord Bot Token Goes Here
prefix = "!"
pfile = 'main.py'
intents = discord.Intents.all()
bot = commands.Bot(command_prefix=f'{prefix}', intents=intents, help_command=None)

start_time = None
process = False

title = """
████████▄     ▄████████    ▄████████ ███▄▄▄▄    ▄██████▄      ███     ▀█████████▄   ▄██████▄      ███     
███   ▀███   ███    ███   ███    ███ ███▀▀▀██▄ ███    ███ ▀█████████▄   ███    ███ ███    ███ ▀█████████▄ 
███    ███   ███    █▀    ███    █▀  ███   ███ ███    ███    ▀███▀▀██   ███    ███ ███    ███    ▀███▀▀██ 
███    ███  ▄███▄▄▄      ▄███▄▄▄     ███   ███ ███    ███     ███   ▀  ▄███▄▄▄██▀  ███    ███     ███   ▀ 
███    ███ ▀▀███▀▀▀     ▀▀███▀▀▀     ███   ███ ███    ███     ███     ▀▀███▀▀▀██▄  ███    ███     ███     
███    ███   ███    █▄    ███        ███   ███ ███    ███     ███       ███    ██▄ ███    ███     ███     
███   ▄███   ███    ███   ███        ███   ███ ███    ███     ███       ███    ███ ███    ███     ███     
████████▀    ██████████   ███         ▀█   █▀   ▀██████▀     ▄████▀   ▄█████████▀   ▀██████▀     ▄████▀   
                                                                                                                        
"""

async def update_title():
    while True:
        gradient_print(title, start_color=Color(0x5215F0), end_color=Color(0x9A79F0))
        await asyncio.sleep(2)
        os.system("cls")

@bot.event
async def on_ready():
    bot.loop.create_task(update_title())
    os.system("cls")

@bot.command(name="run", aliases=["r"])
async def start(ctx):
    global process, start_time
    if process is not False:
        embed = discord.Embed(
            title='Info',
            description='❗ | The Sniper is already running.',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return

    try:
        if start_time is None:
            start_time = datetime.now()

        os.system(f"start /B start cmd.exe @cmd /k py {pfile}")
        process = True
        response = f'✅ | Sniper started!'
        embed = discord.Embed(
            title='Success',
            description=f'{response}',
            color=discord.Color.green()
        )
    except Exception as e:
        response = f'❌ | Error starting sniper: {e}'
        embed = discord.Embed(
            title='Error',
            description=f'{response}',
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

@bot.command(name="kill", aliases=['k'])
async def kill(ctx):
    global process, start_time
    if process is False:
        embed = discord.Embed(
            title='Info',
            description='❗ | The Sniper is not currently running.',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return

    try:
        current_pid = os.getpid()
        processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
        programs_to_kill = ['python.exe', 'cmd.exe']

        for proces in processes:
            for program in programs_to_kill:
                if program in proces:
                    pid = int(proces.split()[1])
                    if pid != current_pid:
                        os.system(f'taskkill /PID {pid} /F')
                        process = False
                        start_time = None
        response = f'✅ | Sniper stopped!'
        embed = discord.Embed(
            title='Success',
            description=f'{response}',
            color=discord.Color.green()
        )
    except Exception as e:
        response = f'❌ | Error stopping sniper: {e}'
        embed = discord.Embed(
            title='Error',
            description=f'{response}',
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

@bot.command(name="elapsed", aliases=['el'])
async def elapsed(ctx):
    global start_time
    if start_time is None:
        embed = discord.Embed(
            title='Info',
            description='❗ | The Sniper has not been started yet.',
            color=discord.Color.blue()
        )
    else:
        running_time = datetime.now() - start_time
        running_time = running_time - timedelta(microseconds=running_time.microseconds)
        embed = discord.Embed(
            title='Elapsed Time',
            description=f'The Sniper has been running for {running_time}',
            color=discord.Color.green()
        )

    await ctx.send(embed=embed)

@bot.command(name="restart", aliases=['re'])
async def restart(ctx):
    global process, start_time
    if process is False:
        embed = discord.Embed(
            title='Info',
            description='❗ | The Sniper is not currently running.',
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
        return

    try:
        current_pid = os.getpid()
        processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
        programs_to_kill = ['python.exe', 'cmd.exe']
        for proces in processes:
            for program in programs_to_kill:
                if program in proces:
                    pid = int(proces.split()[1])
                    if pid != current_pid:
                        os.system(f'taskkill /PID {pid} /F')
                        start_time = None
        os.system(f"start /B start cmd.exe @cmd /k py {pfile}")
        if start_time is None:
            start_time = datetime.now()
        response = f'✅ | Sniper restarted!'
        embed = discord.Embed(
            title='Success',
            description=f'{response}',
            color=discord.Color.green()
        )
    except Exception as e:
        response = f'❌ | Error restarting sniper: {e}'
        embed = discord.Embed(
            title='Error',
            description=f'{response}',
            color=discord.Color.red()
        )
    await ctx.send(embed=embed)

auto_restarta = False
@bot.command(name="autorestart", aliases=["ar"])
async def autorestart(ctx, toggle=None, interval=None):
    global process,auto_restarta
    if toggle is None and interval is None:
        embed = discord.Embed(
            title='Error',
            description=f':x: | Please specify on/off and the interval between each restart. ex: {prefix}ar on 10m',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    if toggle is None:
        embed = discord.Embed(
            title='Error',
            description=':x: | Please specify on or off',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return

    if toggle.lower() == "on":
        if interval is None:
            embed = discord.Embed(
                title='Error',
                description=':x: | Please specify the interval between each restart. ex: on 10m',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        try:
            intervalv, intervalu = parse_interval(interval)
            if intervalv <= 0:
                raise ValueError('Invalid interval value.')

            async def auto_restart():
                global process,auto_restarta
                while auto_restarta:
                    current_pid = os.getpid()
                    processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
                    programs_to_kill = ['python.exe', 'cmd.exe']
                    for proces in processes:
                        for program in programs_to_kill:
                            if program in proces:
                                pid = int(proces.split()[1])
                                if pid != current_pid:
                                    os.system(f'taskkill /PID {pid} /F')
                                    process = False

                    os.system(f"start /B start cmd.exe @cmd /k py {pfile}")
                    process = True
                    await asyncio.sleep(intervalv)

            auto_restarta = True
            bot.loop.create_task(auto_restart())
            response = f'✅ | Sniper will start auto restarting every {interval}.'
            embed = discord.Embed(
                title='Success',
                description=f'{response}',
                color=discord.Color.green()
            )
        except Exception as e:
            response = f'❌ | Error starting auto restart: {e}'
            embed = discord.Embed(
                title='Error',
                description=f'{response}',
                color=discord.Color.red()
            )

    elif toggle.lower() == "off":
        if auto_restarta:
            current_pid = os.getpid()
            processes = subprocess.run(['tasklist'], capture_output=True, text=True).stdout.split('\n')
            programs_to_kill = ['python.exe', 'cmd.exe']
            for proces in processes:
                for program in programs_to_kill:
                    if program in proces:
                        pid = int(proces.split()[1])
                        if pid != current_pid:
                            os.system(f'taskkill /PID {pid} /F')
                            process = False

            auto_restarta = False
            embed = discord.Embed(
                title='Success',
                description='✅ | Auto restart has been turned off. (*Sniper stopped*)',
                color=discord.Color.green()
            )
        else:
            embed = discord.Embed(
                title='Info',
                description='❗ | Auto restart is not currently active.',
                color=discord.Color.blue()
            )
    else:
        embed = discord.Embed(
            title='Error',
            description=':x: | Invalid toggle. Please use `on` or `off`.',
            color=discord.Color.red()
        )

    await ctx.send(embed=embed)

def parse_interval(interval):
    intervalv = int(interval[:-1])
    intervalu = interval[-1]
    if intervalu == 'm':
        intervalv *= 60
    elif intervalu == 'h':
        intervalv *= 3600
    elif intervalu == 'd':
        intervalv *= 86400
    else:
        raise ValueError('Invalid interval unit.')

    return intervalv, intervalu

@bot.command(name="ss")
async def screenshot(ctx):
    try:
        if not os.path.exists("screenshots"):
            os.makedirs("screenshots")

        waitmsg = await ctx.send("Please wait...")

        filename = "screenshot.png"
        filepath = os.path.join("screenshots", filename)
        pyautogui.screenshot(filepath)

        file = discord.File(filepath, filename=filename)
        embed = discord.Embed(
            title="Screenshot",
            description="Here is a screenshot of your PC:",
            color=discord.Color.blue()
        )
        embed.set_image(url=f"attachment://{filename}")

        await ctx.send(embed=embed, file=file)
        await waitmsg.delete()
    except Exception as e:
        response = f'❌ | Error taking a screenshot: {e}'
        embed = discord.Embed(
            title='Error',
            description=f'{response}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        await waitmsg.delete()

@bot.command(name="check", aliases=["c"])
async def check(ctx, id):
    try:
        id = int(id)
    except ValueError:
        embed = discord.Embed(
            title='Error',
            description='❌ | Please provide a valid ID.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        return
    
    if id is not None:
        try:
            waitmsg = await ctx.send("Please wait...")
            fcsrf = requests.post('https://auth.roblox.com/v1/usernames/validate')
            csrf = fcsrf.headers['x-csrf-token']
            fetch = 'https://catalog.roblox.com/v1/catalog/items/details'
            headers = {
                'X-Csrf-Token': f'{csrf}'
            }
            payload = {
                'items': [
                    {
                        'itemType': 1,
                        'id': id
                    }
                ]
            }
            response = requests.post(fetch, headers=headers, json=payload)
            
            if response.status_code == 200:
                data = response.json().get('data', [])
                if data:
                    item = data[0]
                    price = item.get('price')
                    status = item.get('priceStatus')
                    type_value = item.get('saleLocationType')
                    quantity = item.get('totalQuantity')
                    limit = item.get('quantityLimitPerUser')
                    description = item.get('description')
                    item_name = item.get('name')
                    item_id = item.get('id')
                    creator_name = item.get('creatorName')
                    
                    findimage = requests.get(f"https://thumbnails.roblox.com/v1/assets?assetIds={item_id}&returnPolicy=PlaceHolder&size=420x420&format=Png&isCircular=false").json()
                    images = findimage.get('data', [])
                    if images:
                        getimage = images[0].get('imageUrl')
                    else:
                        getimage = None
                    
                    embed_description = f"• __**Name:**__ {item_name}\n\n• __**Creator:**__ {creator_name}\n\n"
                    
                    if price is not None:
                        embed_description += f"• __**Price:**__ {price}\n\n"
                    if status is not None:
                        embed_description += f"• __**Status:**__ {status}\n\n"
                    if limit is not None:
                        embed_description += f"• __**Limit:**__ {limit}\n\n"
                    if quantity is not None:
                        embed_description += f"• __**Quantity:**__ {quantity}\n\n"
                    embed_description += f"• __**Type:**__ {type_value}\n\n"
                    embed_description += f"• __**Link:**__ https://roblox.com/catalog/{item_id}/Remotely\n\n"
                    if description is not None:
                        embed_description += f"• __**Description:**__ ```{description}```"
                    
                    embed = discord.Embed(
                        title='Info',
                        description=embed_description,
                        color=discord.Color.blue()
                    )
                    
                    if getimage is not None:
                        embed.set_thumbnail(url=getimage)
                    
                    await ctx.send(embed=embed)
                    await waitmsg.delete()
                else:
                    await ctx.send(f"❌ | No data found for the ID {id}.")
                    await waitmsg.delete()
            elif response.status_code == 429:
                embed = discord.Embed(
                    title='Rate Limit!',
                    description=f'❌ | Rate limit exceeded. Please wait 1m and try again!',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                await waitmsg.delete()
            else:
                embed = discord.Embed(
                    title='Weird..',
                    description=f'❌ | Something weird happened while fetching your ID.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                await waitmsg.delete()
        except Exception as e:
            embed = discord.Embed(
                title='Error',
                description=f'❌ | An error occurred: {e}',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            await waitmsg.delete()

@check.error
async def checkerr(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument) and error.param.name == 'id':
        embed = discord.Embed(
            title='Error',
            description='❌ | Please provide an ID.',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.command(name="status", aliases=["s"],)
async def status(ctx):
    global process
    if process:
        embed = discord.Embed(
            title='Info',
            description='✅ | That Sniper is running.',
            color=discord.Color.green()
        )
    else:
        embed = discord.Embed(
            title='Info',
            description='❗ | The Sniper is not running.',
            color=discord.Color.blue()
        )
    await ctx.send(embed=embed)


@bot.command(name="config", aliases=["cf"])
async def config_command(ctx):
    try:
        with open("config.json") as file:
            data = json.load(file)

        auto_restart = data.get("auto_restart", False)
        items_count = len(data.get("items", {}).get("list", {}))
        global_max_price = data.get("items", {}).get("global_max_price", 0)
        cookie = data.get("cookie", "")

        auto_restart_status = "Enabled" if auto_restart else "Disabled"

        config = f"**Auto restart:** {auto_restart_status}\n"
        config += f"**ID(s):** {items_count}\n"
        config += f"**Global max price:** {global_max_price}\n"
        config += f"**Cookie:** ||{cookie}||\n"

        embed = discord.Embed(
            title='Configuration Settings',
            description=config,
            color=discord.Color.blue()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)    


@bot.command(name="change", aliases=["ch"])
async def change(ctx, change=None, value=None):
    try:
        if change is None or value is None:
            embed = discord.Embed(
                title='Error',
                description=f'❌ | Please specify what you want to change and what you want to change it to. ex: `{prefix}change cookie "_|your_cookie_here|"`',
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        with open("config.json") as file:
            data = json.load(file)

        if change == "cookie":
            if not value.startswith("_|WARNING:-DO-NOT-SHARE-THIS.--Sharing-this-will-allow-someone-to-log-in-as-you-and-to-steal-your-ROBUX-and-items."):
                embed = discord.Embed(
                    title='Error',
                    description='❌ | Invalid cookie.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            data["cookie"] = value
            embed = discord.Embed(
                title='Success',
                description='✅ | Successfully changed your cookie',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        elif change == "waittime":
            if not value.isdigit():
                embed = discord.Embed(
                    title='Error',
                    description='❌ | Invalid wait time.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            data["wait_time"] = int(value)
            embed = discord.Embed(
                title='Success',
                description='✅ | Successfully changed wait time',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        elif change == "gmp" or change == "globalmaxprice":
            if not value.isdigit():
                embed = discord.Embed(
                    title='Error',
                    description='❌ | Invalid global max price.',
                    color=discord.Color.red()
                )
                await ctx.send(embed=embed)
                return
            data["global_max_price"] = int(value)
            embed = discord.Embed(
                title='Success',
                description='✅ | Successfully changed global max price',
                color=discord.Color.green()
            )
            await ctx.send(embed=embed)
        else:
            embed = discord.Embed(
                title='Error',
                description="❌ | Invalid configuration option. Specify 'cookie', 'waittime', or 'gmp'.",
                color=discord.Color.red()
            )
            await ctx.send(embed=embed)
            return

        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.command(name="resetids", aliases=["rid"])
async def delete_ids(ctx):
    try:
        with open("config.json") as file:
            data = json.load(file)

        if len(data["items"]) <= 1:
            embed = discord.Embed(
                title='Info',
                description='❗ | There is only 1 ID in the item list.',
                color=discord.Color.blue()
            )
            await ctx.send(embed=embed)
            return
        data["items"] = data["items"][:1]
        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)
        embed = discord.Embed(
            title='Success',
            description='✅ | Resetted all the IDs in the config file.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name="ids", description="Display the IDs in the item list.")
async def ids(ctx):
    try:
        with open("config.json") as file:
            data = json.load(file)

        item_list = data.get("items", {}).get("list", {})
        item_ids = ', '.join(item_id for item_id in item_list.keys())
        amount = len(item_list)

        embed = discord.Embed(
            title='IDs in the list',
            description=f'```{item_ids}```\nAmount: {amount}',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)

    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name="add_ids", aliases=["aid"])
async def add_ids(ctx, *, args):
    try:
        with open("config.json", "r") as file:
            data = json.load(file)

        entries = args.split(",")
        max_price = None

        # Check if the last entry is a valid max price (integer)
        last_entry = entries[-1].strip()
        if last_entry.isnumeric():
            max_price = int(entries.pop())

        item_data = data.get("items", {}).get("list", {})  # Get the 'list' dictionary within 'items'

        for entry in entries:
            item_id = int(entry.strip())
            if max_price is not None:
                item_data[str(item_id)] = {"max_price": max_price}
            else:
                item_data[str(item_id)] = {"max_price": 0}  # Default max price when not specified

        # Update the 'list' dictionary within 'items' in the data dictionary
        data["items"]["list"] = item_data

        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

        embed = discord.Embed(
            title='Success',
            description='✅ | Added the ID(s) and max prices to the config file.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        
@bot.command(name="remove_ids", aliases=["rmid"])
async def remove_ids(ctx, *, args):
    try:
        with open("config.json") as file:
            data = json.load(file)

        entries = args.split(", ")
        item_data = data.get("items", {}).get("list", {})  # Get the 'list' dictionary within 'items'

        for entry in entries:
            item_id = entry
            if item_id in item_data:
                del item_data[item_id]

        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

        embed = discord.Embed(
            title='Success',
            description='✅ | Removed the specified ID(s) and max prices from the config file.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)

@bot.command(name="clearids", aliases=["cid"])
async def clear_ids(ctx):
    try:
        with open("config.json", "r") as file:
            data = json.load(file)

        if "items" in data and "list" in data["items"]:
            data["items"]["list"] = {}

        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

        embed = discord.Embed(
            title='Success',
            description='✅ | Cleared all the IDs and max prices in the config file.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)
        
@bot.command(name="add_links", aliases=["al"])
async def add_links(ctx, *, args):
    try:
        with open("config.json") as file:
            data = json.load(file)

        entries = args.split(", ")
        item_links = [entry for entry in entries]

        data["items"].extend(item_links)

        with open("config.json", "w") as file:
            json.dump(data, file, indent=4)

        embed = discord.Embed(
            title='Success',
            description='✅ | Added the link(s) to the config file.',
            color=discord.Color.green()
        )
        await ctx.send(embed=embed)
    except Exception as e:
        embed = discord.Embed(
            title='Error',
            description=f'❌ | An error occurred: {e}',
            color=discord.Color.red()
        )
        await ctx.send(embed=embed)


@bot.command(name="help", aliases=['h'], description="Shows the help message.")
async def help_command(ctx):
    pages = [
        [
            {"name": f"{prefix}run   |   {prefix}r", "value": "Starts the Sniper."},
            {"name": f"{prefix}restart   |   {prefix}re", "value": "Restarts the Sniper."},
            {"name": f"{prefix}kill   |   {prefix}k", "value": "Stops the Sniper."},
            {"name": f"{prefix}ss", "value": "Takes a screenshot of your PC."},
            {"name": f"{prefix}check `<id>`   |   {prefix}c `<id>`", "value": "Checks information about a catalog item."},
            {"name": f"{prefix}help   |   {prefix}h", "value": "Shows this message."},
        ],
        [
            {"name": f'{prefix}status   |   {prefix}s', "value": 'Check if the Sniper is running.'},
            {"name": f'{prefix}config   |   {prefix}cf', "value": 'View the current configuration settings.'},
            {"name": f'{prefix}resetids `[option]`   |   {prefix}rid `[option]`', "value": 'Resets all the IDs in specified item list. Options: release/r, cheap/c'},
            {"name": f'{prefix}change `[option]` `[value]`   |   {prefix}ch `[option]` `[value]`', "value": 'Change configuration settings. Options: rooms, token, prefix, theme, cookie.'},
            {"name": f'{prefix}ids [option]', "value": 'Display the IDs in the specified list. Options: release/r, cheap/c'},
            {"name": f'{prefix}autorestart `[toggle]` `[interval]`   |   {prefix}ar `[toggle]` `[interval]`', "value": 'Automatically restarts your sniper every X amount of time. Toggle: on, off'},
            {"name": f'{prefix}add_ids `<id1>, <id2>, etc.. <type> <max price>`   |   {prefix}aid `<id1>, <id2>, etc.. <type> <max price>`', "value": 'Adds multiple IDs at once to config.json. Type: release/r, cheap/c. **IMPORTANT:** The commas and spaces are very important so make sure you put them.'},
            {"name": f'{prefix}cheap `[toggle]`', "value": 'Toggle cheap sniping on/off. Toggle: on, off'},
        ],
        [
            {"name": f'{prefix}add_links `<link1>, <link2>, etc.. <type> <max price>`   |   {prefix}al `<link1>, <link1>, etc.. <type> <max price>`', "value": 'Adds multiple IDs at once to config.json using roblox links. Type: release/r, cheap/c. **IMPORTANT:** The commas and spaces are very important so make sure you put them.'},
            {"name": f'{prefix}elapsed   |   {prefix}el', "value": 'View for how long the sniper has been running.'},
            {"name": f'{prefix}add_cookies `<cookie1>, <cookie2>, etc..`   |   {prefix}ac `<cookie1>, <cookie2>, etc..`', "value": 'Add multiple cookies at once to config.json'},
            {"name": f'{prefix}remove_ids `<id1>, <id2>, etc.. <type>`   |   {prefix}rmid `<id1>, <id2>, etc.. <type>`', "value": 'Remove multiple IDs at once from config.json. Type: release/r, cheap/c.'},
            {"name": f'{prefix}remove_cookies `<cookie1>, <cookie2>, etc..`   |   {prefix}rc `<cookie1>, <cookie2>, etc..`', "value": 'Remove multiple cookies at once from config.json.'},
            {"name": f'{prefix}checkup `<type>`   |   {prefix}cup `<type>`', "value": 'Checks all the IDs in the specified type to see which ones are on sale. Type: release/r, cheap/c.'},
        ]
    ]

    page = 0

    async def update_embed():
        embed.clear_fields()
        embed.title = f"• DefnotBot's Commands - Page {page + 1}"
        embed.description = "**THESE ARE THE COMMANDS YOU CAN USE - **"
        for command in pages[page]:
            embed.add_field(name=command['name'], value=command['value'], inline=False)
        await message.edit(embed=embed)

    embed = discord.Embed(
        title=f"• DefnotBot's Commands - Page {page + 1}",
        url="https://discord.gg/WR2ZkPfkHy",
        description="**THESE ARE THE COMMANDS YOU CAN USE - **",
        color=discord.Color.blue()
    )
    for command in pages[page]:
        embed.add_field(name=command['name'], value=command['value'], inline=False)
    embed.set_footer(text="DefNotBot - by DefnNotStevo)")

    message = await ctx.send(embed=embed)
    await message.add_reaction('◀')
    await message.add_reaction('▶')

    def check(reaction, user):
        return user == ctx.author and str(reaction.emoji) in ['◀', '▶']

    while True:
        try:
            reaction, user = await bot.wait_for('reaction_add', timeout=30.0, check=check)
        except asyncio.TimeoutError:
            break

        if str(reaction.emoji) == '◀' and page > 0:
            page -= 1
            await update_embed()
        elif str(reaction.emoji) == '▶' and page < len(pages) - 1:
            page += 1
            await update_embed()

    await message.clear_reactions()

loop = asyncio.get_event_loop()
loop.create_task(update_title())
bot.run(token)
