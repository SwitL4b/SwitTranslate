# MIT License
# Copyright (c) 2025 kenftr


import discord
from discord.ext import commands
from Module.Translate.translate import TranslateCommand
from Module.Translate.Utils import Config
from Module.Check import check
app = commands.Bot(command_prefix="!",intents=discord.Intents.default())


@app.event
async def on_ready() -> None:
    await app.add_cog(TranslateCommand(app=app))
    await app.tree.sync()
    print('Bot is ready')

def main() -> None:
    if check() == False:
        for i in range(10):
            print('⚠️ Please check your config.yml. Make sure both the API key and bot token are set correctly.')
        return
    app.run(Config.Discord.Token())

if __name__ == '__main__':
    main()