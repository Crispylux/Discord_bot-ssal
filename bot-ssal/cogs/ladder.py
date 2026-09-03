"""/사다리타기 프로그램"""
"""개발자: https://github.com/Crispylux"""


from __future__ import annotations

import random
from typing import Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.ladder_render import run_ladder
from utils.parsing import split_list, validate_participants


class LadderCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @app_commands.command(name="사다리타기", description="참가자들과 결과를 입력하면 사다리타기를 진행합니다.")
    @app_commands.describe(
        참가자="쉼표(,)로 구분한 참가자 목록. 예: 쌀1,쌀2,쌀3",
        결과="쉼표(,)로 구분한 결과 목록 (참가자 수와 같아야 함). 비워두면 '당첨/꽝'으로 자동 설정됩니다. 예: 탱,딜,힐",
        인원="결과를 비워뒀을 때, 몇 명을 '당첨'으로 할지 (기본 1명)",
    )
    async def ladder(
        self,
        interaction: discord.Interaction,
        참가자: str,
        결과: Optional[str] = None,
        인원: Optional[int] = 1,
    ):
        participants = split_list(참가자)
        err = validate_participants(participants)
        if err:
            await interaction.response.send_message(f"⚠️ {err}", ephemeral=True)
            return

        n = len(participants)

        if 결과:
            results = split_list(결과)
            if len(results) != n:
                await interaction.response.send_message(
                    f"⚠️ 결과 개수({len(results)}개)가 참가자 수({n}명)와 다릅니다. 둘의 개수가 같아야 합니다.",
                    ephemeral=True,
                )
                return
        else:
            win = max(1, min(인원 or 1, n))
            results = ["🎉당첨"] * win + ["꽝"] * (n - win)
            # 어느 자리에 당첨이 몰려있는지 티가 나지 않도록 섞어준다
            random.shuffle(results)

        ladder_result = run_ladder(participants, results)

        pairs_text = "\n".join(f"{p} → {r}" for p, r in ladder_result.pairs())
        message = f"🪜 **사다리타기 결과** (요청: {interaction.user.display_name})\n{pairs_text}"

        await interaction.response.send_message(message)


async def setup(bot: commands.Bot):
    await bot.add_cog(LadderCog(bot))
