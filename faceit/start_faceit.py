import random
from typing import List
import discord
from discord.ui import View, Select
import asyncio

faceitGameId = 0

async def get_maps(channel : discord.TextChannel):

    maps = ['zone7', 'sandstone', 'sakura', 'rust', 'province', 'breeze', 'dune']
    emodjis = [e for e in channel.guild.emojis if e.name in maps]

    embed = discord.Embed(
        title = 'Выберите карту. 10 cек',
        color = discord.Color.green()
    )

    msg = await channel.send(embed = embed)
    await asyncio.gather(*(msg.add_reaction(e) for e in emodjis))
    
    await asyncio.sleep(10)

    msg : discord.Message = [m async for m in channel.history(limit = 1)][0]

    counts = {}

    for reactions in msg.reactions:
        if reactions.emoji.name in maps:
            counts[reactions.emoji] = reactions.count
        
    res : discord.Emoji = max(counts, key=counts.get)

    print(str(res))

    await msg.delete()

    return str(res)

async def get_rounds(channel : discord.TextChannel):

    rounds = ['1️⃣', '2️⃣', '3️⃣']

    embed = discord.Embed(
        title = 'Выберите кол-во раундов. 10 cек',
        color = discord.Color.blue()
    )

    embed.add_field(
        name='1️⃣ - 10 раундов'
    )

    embed.add_field(
        name='2️⃣ - 13 раундов'
    )

    embed.add_field(
        name='3️⃣ - 16 раундов'
    )

    msg = await channel.send(embed = embed)
    await asyncio.gather(*(msg.add_reaction(e) for e in rounds))
    
    await asyncio.sleep(10)

    msg : discord.Message = [m async for m in channel.history(limit = 1)][0]

    counts = {}

    for reactions in msg.reactions:
        if reactions.emoji in rounds:
            counts[reactions.emoji] = reactions.count
        
    res = max(counts, key=counts.get)

    print(str(res))

    await msg.delete()

    return res

async def start_faceit_game(members: List[discord.Member], channel: discord.TextChannel):

    global faceitGameId

    cap1 = random.choice(members)
    cap2 = random.choice([m for m in members if m != cap1])

    cap1Players = []
    cap2Players = []

    available_players = [m for m in members if m != cap1 and m != cap2]

    turn_order = [
        (cap1, 1),
        (cap2, 2),
        (cap1, 2),
        (cap2, 1),
        (cap1, 1),
        (cap2, 1)
    ]

    turn_index = 0
    picks_remaining = turn_order[turn_index][1]

    embed = discord.Embed(title=f"Faceit ranked game #{faceitGameId}")

    def update_embed():
        embed.set_field_at(0, name='CT', value=f'{cap1.mention}\n' + "\n".join(p.mention for p in cap1Players), inline=False)
        embed.set_field_at(1, name='T', value=f'{cap2.mention}\n' + "\n".join(p.mention for p in cap2Players), inline=False)

    embed.add_field(name='CT', value=f'{cap1.mention}', inline=False)
    embed.add_field(name='T', value=f'{cap2.mention}', inline=False)

    view = View()

    def create_select(for_captain: discord.Member):
        options = [discord.SelectOption(label=p.display_name, value=str(p.id)) for p in available_players]
        select = Select(
            placeholder=f'{for_captain.display_name}, выберите игрока',
            options=options,
            max_values=1,
            min_values=1
        )

        async def select_callback(interaction: discord.Interaction):
            nonlocal picks_remaining, turn_index, available_players, cap1Players, cap2Players

            if interaction.user.id != for_captain.id:
                await interaction.response.send_message(f"Сейчас выбирает {for_captain.mention}!")
                return

            selected_id = int(select.values[0])
            selected_player = discord.utils.get(available_players, id=selected_id)

            if selected_player is None:
                await interaction.response.send_message("Игрок не найден или уже выбран")
                return
    
            if for_captain == cap1:
                cap1Players.append(selected_player)
            else:
                cap2Players.append(selected_player)

            available_players.remove(selected_player)

            picks_remaining -= 1

            update_embed()

            if picks_remaining == 0:
                turn_index += 1
                if turn_index >= len(turn_order):
            
                    await interaction.message.edit(embed=embed, view=None)
                    await interaction.response.send_message("check!")
                    map : discord.Emoji = await get_maps(channel)
                    rounds = await get_rounds(channel)
                    return
                else:
                    picks_remaining = turn_order[turn_index][1]

    
            next_captain = turn_order[turn_index][0]

    
            new_view = View()
            if available_players:
                new_view.add_item(create_select(next_captain))
                await interaction.message.edit(embed=embed, view=new_view)

            await interaction.response.defer()

        select.callback = select_callback
        return select

    view.add_item(create_select(turn_order[turn_index][0]))

    await channel.send(embed=embed, view=view)
