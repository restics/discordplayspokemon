
from discord.ui import View, Select
import discord
import os

from player import instance

class RomsDropdown(View):
    def __init__(self, roms):
        super().__init__()
        self.add_item(RomsSelect(roms))

class RomsSelect(Select):
    def __init__(self, roms):
        options = [discord.SelectOption(label=rom) for rom in roms]
        super().__init__(placeholder="Choose a ROM...", min_values=1, max_values=1, options=options)

    async def callback(self, interaction: discord.Interaction):
        await interaction.response.send_message(f"You selected: {self.values[0]}", ephemeral=True)
        await instance.load_rom(self.values[0])

class DummyButton(discord.ui.Button):
    def __init__(self, row, col):
        super().__init__(label="\u200b", style=discord.ButtonStyle.secondary, disabled=True, row=row)
    async def callback(self, interaction: discord.Interaction):
        pass

class GameboyPad(View):
    def __init__(self):
        super().__init__(timeout=None)
        """
        3 rows x 5 columns grid
        .^...
        <.>ab
        .v.sS
        
        """
        # Row 0
        self.add_item(DummyButton(row=0, col=0))
        self.add_item(GameboyButton('up', row=0, col=1))
        self.add_item(DummyButton(row=0, col=2))
        self.add_item(DummyButton(row=0, col=3))
        self.add_item(DummyButton(row=0, col=4))
        # Row 1
        self.add_item(GameboyButton('left', row=1, col=0))
        self.add_item(DummyButton(row=1, col=1))
        self.add_item(GameboyButton('right', row=1, col=2))
        self.add_item(GameboyButton('a', row=1, col=3))
        self.add_item(GameboyButton('b', row=1, col=4))
        # Row 2
        
        self.add_item(DummyButton(row=2, col=0))
        self.add_item(GameboyButton('down', row=2, col=1))
        self.add_item(DummyButton(row=2, col=2))
        self.add_item(GameboyButton('start', row=2, col=3))
        self.add_item(GameboyButton('select', row=2, col=4))


class GameboyButton(discord.ui.Button):
    def __init__(self, label, row, col):
        super().__init__(label=label.upper(), style=discord.ButtonStyle.primary, row=row)
        self.input_label = label

    async def callback(self, interaction: discord.Interaction):
        if not instance.is_playing:
            await interaction.response.send_message("No rom loaded!")
            return
        embed, image = play_game_screen()
        reply = instance.send_input(interaction.user.id, self.input_label)
        if image:
            await interaction.response.send_message(reply, embed=embed, file=image, view=GameboyPad(), ephemeral=True)
        else:
            await interaction.response.send_message(reply, embed=embed, view=GameboyPad(), ephemeral=True)


def play_game_screen():
    embed = discord.Embed(title="Gameboy Emulator")
    frame_dir = 'temp'
    frame_filename = 'curr_frame.png'
    frame_path = os.path.join(frame_dir, frame_filename)
    if os.path.exists(frame_path):
        imagefile = discord.File(frame_path, filename=frame_filename)
        embed.set_image(url=f'attachment://{frame_filename}')
        return embed, imagefile
    else:
        return embed, None
