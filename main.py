import os
import discord

from discord import app_commands
from discord.ext import commands

from license_checker import (
    check_license
)

from security.heartbeat import (
    setup_heartbeat
)


MY_DISCORD_ID = 1028589017861718076


class TicketLauncher(discord.ui.View):

    def __init__(self):

        super().__init__(timeout=None)

    @discord.ui.button(
        label="Submit YouTube Proof",
        style=discord.ButtonStyle.primary,
        custom_id="open_ticket_final_eng",
        emoji="📸"
    )

    async def open_ticket(
        self,
        interaction: discord.Interaction,
        button: discord.ui.Button
    ):

        if not interaction.client.license_valid:

            return await interaction.response.send_message(
                "❌ Subscription Expired",
                ephemeral=True
            )

        guild = interaction.guild

        user = interaction.user

        ticket_channel_name = (
            f"ticket-{user.name.lower()}"
        ).replace(" ", "-")

        existing_channel = discord.utils.get(
            guild.text_channels,
            name=ticket_channel_name
        )

        if existing_channel:

            return await interaction.response.send_message(
                f"You already have an open ticket: {existing_channel.mention}",
                ephemeral=True
            )

        await interaction.response.defer(ephemeral=True)

        overwrites = {

            guild.default_role:
            discord.PermissionOverwrite(
                view_channel=False
            ),

            user:
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                read_message_history=True,
                attach_files=True
            ),

            guild.me:
            discord.PermissionOverwrite(
                view_channel=True,
                send_messages=True,
                manage_channels=True
            )
        }

        ticket_channel = await guild.create_text_channel(

            name=ticket_channel_name,

            overwrites=overwrites,

            topic=f"Private Ticket for {user.name}"
        )

        embed = discord.Embed(

            title="🛡️ UID Whitelist",

            description=(

                f"Hello {user.mention},\n\n"

                "1. Upload your YouTube subscription screenshot.\n"

                "2. Send your UID.\n\n"

                f"Admin <@{MY_DISCORD_ID}> will review shortly."
            ),

            color=discord.Color.blue()
        )

        embed.set_footer(
            text="CODEVERSE Security"
        )

        await ticket_channel.send(

            content=f"<@{MY_DISCORD_ID}>",

            embed=embed
        )

        await interaction.followup.send(

            f"✅ Ticket Created: {ticket_channel.mention}",

            ephemeral=True
        )


class CODEVERSE(commands.Bot):

    def __init__(self):

        super().__init__(
            command_prefix="!",
            intents=discord.Intents.all()
        )

        self.license_valid = True

    async def setup_hook(self):

        self.add_view(
            TicketLauncher()
        )

        setup_heartbeat(self)

        await self.tree.sync()

        print(
            f"Logged in as {self.user}"
        )


bot = CODEVERSE()




@bot.event
async def on_message(message):

    if message.author.bot:
        return

    if not bot.license_valid:
        return

    await bot.process_commands(message)




@bot.tree.interaction_check
async def interaction_check(
    interaction: discord.Interaction
):

    if not bot.license_valid:

        await interaction.response.send_message(
            "❌ Subscription Expired",
            ephemeral=True
        )

        return False

    return True




@bot.tree.command(
    name="spawn_ticket",
    description="Create whitelist panel"
)

@app_commands.checks.has_permissions(
    administrator=True
)

async def spawn_ticket(
    interaction: discord.Interaction
):

    embed = discord.Embed(

        title="🛡️ UID Whitelist",

        description=(

            "To access our software:\n\n"

            "• Subscribe to our YouTube channel\n"

            "• Click the button below\n"

            "• Upload proof screenshot\n"

            "• Send your UID"
        ),

        color=discord.Color.blue()
    )

    await interaction.channel.send(

        embed=embed,

        view=TicketLauncher()
    )

    await interaction.response.send_message(

        "✅ Whitelist Panel Spawned!",

        ephemeral=True
    )




@bot.tree.command(
    name="about",
    description="Bot information"
)

async def about(
    interaction: discord.Interaction
):

    valid, data = check_license()

    status = (
        "ACTIVE"
        if valid
        else "EXPIRED"
    )

    last_payment = data.get(
        "last_payment",
        "Unknown"
    )

    expires = data.get(
        "expires",
        "Unknown"
    )

    await interaction.response.send_message(

        f"""

🦋 CODEVERSE v1.0

License Status:
{status}

Last Payment:
{last_payment}

Expires:
{expires}

        """,

        ephemeral=True
    )




bot.run(
    os.getenv("TOKEN")
)
