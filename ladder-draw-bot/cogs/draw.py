"""/추첨 프로그램"""
"""개발자: https://github.com/Crispylux"""


from __future__ import annotations

import asyncio
import random

import discord
from discord import app_commands
from discord.ext import commands

from utils.parsing import split_list, validate_participants


class DrawCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="추첨", description="참가자 목록 중에서 무작위로 N명을 추첨합니다.")
    @app_commands.describe(
        참가자="쉼표(,)로 구분한 참가자 목록. 예: 쌀1, 쌀2, 쌀3, 쌀4",
        인원="몇 명을 뽑을지 (기본 1명)",
        중복허용="같은 사람이 여러 번 뽑힐 수 있게 할지 (기본 false)",
    )
    async def draw(
        self,
        interaction: discord.Interaction,
        참가자: str,
        인원: int = 1,
        중복허용: bool = False,
    ):
        participants = split_list(참가자)
        err = validate_participants(participants)
        if err:
            await interaction.response.send_message(f"⚠️ {err}", ephemeral=True)
            return

        if 인원 < 1:
            await interaction.response.send_message("⚠️ 뽑을 인원은 1명 이상이어야 합니다.", ephemeral=True)
            return

        if not 중복허용 and 인원 > len(participants):
            await interaction.response.send_message(
                f"⚠️ 중복 허용을 켜지 않으면 최대 {len(participants)}명까지만 뽑을 수 있습니다.",
                ephemeral=True,
            )
            return

        await interaction.response.send_message(
            embed=discord.Embed(description="🎲 추첨 중...", color=discord.Color.gold())
        )

        # 약간의 긴장감을 위한 연출
        await asyncio.sleep(1.0)

        if 중복허용:
            winners = [random.choice(participants) for _ in range(인원)]
        else:
            winners = random.sample(participants, 인원)

        embed = discord.Embed(
            title="🎉 추첨 결과",
            description="\n".join(f"**{i+1}등** {w}" for i, w in enumerate(winners)),
            color=discord.Color.gold(),
        )
        embed.set_footer(text=f"전체 {len(participants)}명 중 {인원}명 추첨 · 요청: {interaction.user.display_name}")

        await interaction.edit_original_response(embed=embed)


async def setup(bot: commands.Bot):
    await bot.add_cog(DrawCog(bot))
