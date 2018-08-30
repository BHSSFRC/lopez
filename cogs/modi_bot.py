import discord
from discord.ext import commands


class modi():
    def __init__(self, bot: commands.Bot, special_cogs: list):
        self.bot = bot
        self.special_cogs = special_cogs

    @commands.group(description="Base command for module tinkering.\nMust be invoked with a subcommand. Can only be invoked by the bot's creator.")
    @commands.is_owner()
    async def mod(self, ctx):
        '''Base command for all module tinkering.'''
        if (ctx.invoked_subcommand is None):
            await ctx.send("This command must be invoked with a subcommand (`unload`, `load`, or `reload`)!")

    @mod.command(description="Load a module.")
    async def load(self, ctx, module: str):
        '''Load a module.'''
        if (module not in self.special_cogs):
            self.bot.load_extension(module)
            await ctx.send("Loaded `{}`".format(module))

    @mod.command(description="Unloads a module.")
    async def unload(self, ctx, module: str):
        '''Unload a module.'''
        if (module not in self.special_cogs):
            self.bot.unload_extension(module)
            await ctx.send("Unloaded `{}`".format(module))

    @mod.command(description='Reload a module. Technically, just calls the unload and load commands.')
    async def reload(self, ctx, module: str):
        '''Reload a module.'''
        await ctx.invoke(self.unload, module)
        await ctx.invoke(self.load, module)


def setup(bot: commands.Bot):
    bot.add_cog(modi(bot, ["main", "modi_bot"]))
