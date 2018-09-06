import boiler
import discord
from discord.ext import commands
import math
import random

scores = ["STR", "DEX", "CON", "INT", "WIS", "CHR"]


def ndn(amount: str) -> list:
    '''Converts a string in ndn format into a two item list of the form [number to roll, size of dice].'''
    d = amount.split('d')
    num_roll = roller.to_int(d[0])
    die_size = roller.to_int(d[1])
    return [num_roll, die_size]


class roller():
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @staticmethod
    def to_int(number: str) -> int:
        '''Really bad str -> int function not to be used outside this file.'''
        try:
            return int(number)
        except ValueError:
            return 1

    @staticmethod
    def mod_from_score(score: int) -> int:
        '''Returns a skill modifier given a DnD ability score.'''
        return math.floor((score - 10) / 2)

    @staticmethod
    def roll_ndn(dice: list) -> list:
        '''Rolls x many n sided dice, where x is dice[0] and n is dice[1].'''
        rolls = []
        for _ in range(dice[0]):
            rolls.append(random.randint(1, dice[1]))
        return rolls

    @commands.command()
    async def roll(self, ctx: commands.Context, dice: ndn):
        '''\"Straight\" rolls a die (no ability scores applied.)'''
        rolls = roller.roll_ndn(dice)
        message = "**Your rolls:**\n"
        for i in range(len(rolls)):
            roll = rolls[i]
            message += "{} + ".format(roll) if i is not len(rolls) - \
                1 else "{} = ".format(roll)
        message += "**{0!s}**".format(sum(rolls))
        await ctx.send(message)

    @commands.command()
    async def skill_check(self, ctx: commands.Context, bonus: int, dc: int = None):
        '''Rolls an ability check.'''
        message = "**You rolled:**\n"
        roll = roller.roll_ndn([1, 20])
        total = sum(roll) + bonus
        message += "{0} {3} {1} = **{2}**\n".format(
            sum(roll), abs(bonus), total, "+" if bonus >= 0 else "-")
        if dc is not None:
            message += "{} {} {}: {}".format(total, "passes DC" if total >=
                                             dc else "fails DC", dc, "Success!" if total >= dc else "You fail!")
        await ctx.send(message)

    @commands.group(description='Base character creation/modification command.\nCurrently, NO DATA is stored and these commands are for testing only.')
    async def character(self, ctx: commands.Context):
        '''Base character creation/modification command.'''
        if (ctx.invoked_subcommand is None):
            await ctx.send("You need to invoke this command with a subcommand. To see available subcommands, try `[] help character`.")

    @character.command(description="Creates a character with all six stats defined in a single command.\nStats MUST be in the following order: strength, dexterity, constitution, intelligence, wisdom, charisma.\nAs this is a very long command, other options will be available.")
    async def create_onecall(self, ctx: commands.Context, name: str, *stats):
        '''Creates a character (long form.)'''
        s = {}
        for i in range(len(scores)):
            stat = scores[i]
            s[stat] = roller.to_int(stats[i])
        em = boiler.embed_template()
        em.title = name
        statblock = ""
        for stat, score in s.items():
            modstring = "+ {}".format(roller.mod_from_score(
                score)) if score > 9 else "- {}".format(abs(roller.mod_from_score(score)))
            statblock += "**{0}:** {1!s} ({2})\n".format(stat,
                                                         score, modstring)
        em.add_field(name="Stats", value=statblock)
        await ctx.send(None, embed=em)


def setup(bot: commands.Bot):
    bot.add_cog(roller(bot))
