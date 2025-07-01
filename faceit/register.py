from discord.ext import commands
from database import registerUser, CheckIfUserExists
from discord.ui import Button, View, Modal, TextInput
import discord

class RegisterModal(Modal):
    def __init__(self):
        super().__init__(title = 'Окно регистрации')

        self.nickname = TextInput(label = 'ваш Ник', placeholder="Введите свой ник в игре")
        self.gameId = TextInput(label = 'ваш ID', placeholder="Введите свой ID в игре")
        self.device = TextInput(label = 'Ваш девайс', placeholder='Введите модель своего дейвайса')
        self.serial_number = TextInput(label = 'Ваш серийный номер', placeholder='Введите серийный номер своего дейвайса')

        self.add_item(self.nickname)
        self.add_item(self.gameId)
        self.add_item(self.device)
        self.add_item(self.serial_number)
    
    async def on_submit(self, interaction : discord.Interaction):
        await registerUser(interaction.user.id, self.nickname.value, self.gameId.value, self.device.value, self.serial_number.value)
        await interaction.response.send_message("Вы успешно зарегистрированы!")

class RegisterCog(commands.Cog):
    def __init__(self, bot : commands.Bot):
        self.bot = bot

    async def button_callback(self, interaction: discord.Interaction):

        response = await CheckIfUserExists(interaction.user.id)

        if response:
            await interaction.response.send_message("Вы регистрированы!")
            return

        await interaction.response.send_modal(RegisterModal())

    @commands.Cog.listener()
    async def on_ready(self):
        print("\033[34mLogged without any issues\033[0m")

        channel = discord.utils.get(self.bot.get_guild(1383163443636338830).text_channels, name = 'register-user')

        registerBtn = Button(label = 'Регистрация', style = discord.ButtonStyle.green)
        registerBtn.callback = self.button_callback

        view = View()
        view.add_item(registerBtn)

        await channel.send(view = view)

    @commands.command()
    async def ping(self, ctx : commands.Context):
        await ctx.channel.send("Pong!")
    
async def setup(bot):
    await bot.add_cog(RegisterCog(bot)) 