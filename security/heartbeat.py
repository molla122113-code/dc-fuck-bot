from discord.ext import tasks

from license_checker import (
    check_license
)


def setup_heartbeat(bot):

    @tasks.loop(minutes=1)
    async def heartbeat():

        valid, _ = check_license()

        bot.license_valid = valid

        print(
            "LICENSE:",
            "ACTIVE" if valid else "EXPIRED"
        )

    heartbeat.start()
