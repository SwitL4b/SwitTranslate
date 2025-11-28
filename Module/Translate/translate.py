# MIT License
# Copyright (c) 2025 kenftr


import discord
import io
import os
import asyncio
from datetime import datetime

from discord import app_commands
from discord.ext import commands

from Module import Model
from Module.Translate.Utils import EmbedJson
from Module.Translate.Utils import Config
from Module.cooldown import CoolDown
class TranslateCommand(commands.Cog):
    def __init__(self,app):
        self.app = app
    @app_commands.command(name=Config.TranslateCommand.Name(),
                          description=Config.TranslateCommand.Description())
    @app_commands.describe(translate_to=Config.TranslateCommand.Describe.Translate_to_description(),config_file=Config.TranslateCommand.Describe.Config_file_description())

    async def Translate(self,interaction: discord.Interaction,translate_to:str,config_file: discord.Attachment) -> None:
        await interaction.response.defer(thinking=True,ephemeral=True)

        print(f'[Translate] [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {interaction.user.id} has used the command.')

        if Config.TranslateCommand.Enabled() == False:
            await interaction.followup.send("This command is disabled.",ephemeral=True)
            print(f'[Translate] [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {interaction.user.id} has been rejected.')
            return

        allowed_roles = Config.TranslateCommand.RolesAllowed()
        if "@everyone" not in allowed_roles:
            user_roles = {role.id for role in interaction.user.roles}
            if not any(int(r) in user_roles for r in allowed_roles):
                await interaction.followup.send("You don't have permission to use this command.", ephemeral=True)
                print(f'[Translate] [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {interaction.user.id} rejected (missing role).')
                return

        allowed_users = Config.TranslateCommand.UsersAllowed()
        if len(allowed_users) > 0:
            if allowed_users is not None and interaction.user.id not in allowed_users:
                await interaction.followup.send("You are not allowed to use this command.", ephemeral=True)
                print(f'[Translate] [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {interaction.user.id} rejected (not allowed).')
                return

        cooldown = CoolDown.check(interaction.user.id)

        if cooldown == 1:
            await interaction.followup.send("Please wait a moment before using the command again.", ephemeral=True)
            return

        if cooldown == 2:
            CoolDown.remove(interaction.user.id)
            CoolDown.add(interaction.user.id)

        if cooldown == 0:
            CoolDown.add(interaction.user.id)


        config_file_name, config_file_ext = os.path.splitext(config_file.filename)
        if config_file_ext not in ['.json','.yaml','.yml']:
            print(f'[Translate] [{datetime.now().strftime("%Y-%m-%d %H:%M:%S")}] {interaction.user.id} has been rejected.')
            await interaction.followup.send("Please only use ``.yml`` and ``.json``")
            return

        config_file = await config_file.read()

        config_file_data = config_file.decode('utf-8')

        # Before start translate embed

        before_embed_data = EmbedJson.get('before_start_translate')
        before_embed = discord.Embed(
            title=before_embed_data['title'],
            description=before_embed_data['description'],
            color=discord.Color.from_str(before_embed_data['color'])
        )
        msg = await interaction.followup.send(embed=before_embed)


        # After start translate embed

        model = Model(target=translate_to, config_data=config_file_data)

        start_embed_data = EmbedJson.get('after_start_translate')
        start_embed = discord.Embed(
            title=start_embed_data['title'],
            description=start_embed_data['description'],
            color=discord.Color.from_str(start_embed_data['color'])
        )
        await msg.edit(embed=start_embed)

        #Because waiting for the result takes around 20 seconds, it causes a heartbeat block, so I added this :3
        for i in range(3):
            prog = discord.Embed(
                title=start_embed_data['title'],
                description=start_embed_data['description'] + "." * i,
                color=discord.Color.from_str(start_embed_data['color'])
            )
            await msg.edit(embed=prog)
            await asyncio.sleep(4)

        result = model.StartTranslate()
        output_filename = f"{config_file_name}-translate{config_file_ext}"

        output_file = discord.File(io.BytesIO(result.encode('utf-8')), filename=output_filename)

        # After Translate embed

        done_embed_data = EmbedJson.get('after_translate')
        done_embed = discord.Embed(
            title=done_embed_data['title'],
            description=done_embed_data['description'],
            color=discord.Color.from_str(done_embed_data['color'])
        )

        await msg.edit(embed=done_embed)
        await interaction.followup.send(file=output_file,ephemeral=True)



