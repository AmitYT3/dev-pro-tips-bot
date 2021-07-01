import discord
from discord.ext import commands
from .reaction_handler import ReactionHandler
import config

class ReactionRolesCog(commands.Cog, name="Reaction Roles"):
    """Give and remove roles based on reactions"""

    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.reaction_handler = ReactionHandler(bot)

    @commands.Cog.listener()
    async def on_ready(self):
        guild = self.bot.get_guild(config.GUILD_ID)
        self.member_role = guild.get_role(config.MEMBER_ROLE_ID)
        self.unassigned_role = guild.get_role(config.UNASSIGNED_ROLE_ID)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        """Gives a role based on a reaction emoji"""
        role_assignment = self.reaction_handler.validate_reaction(payload)
        if role_assignment is not None:
            await role_assignment.member.add_roles(role_assignment.role)
            # add member role
            await role_assignment.member.add_roles(self.member_role)
            # remove unassigned role
            await role_assignment.member.remove_roles(self.unassigned_role)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        """Removes a role based on a reaction emoji"""
        role_assignment = self.reaction_handler.validate_reaction(payload)
        if role_assignment is not None:
            await role_assignment.member.remove_roles(role_assignment.role)
        

# setup functions for bot
def setup(bot):
    bot.add_cog(ReactionRolesCog(bot))