"""/추첨 프로그램"""
"""개발자: https://github.com/Crispylux"""



from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Dict, List, Optional

import discord
from discord import app_commands
from discord.ext import commands

from utils.ladder_render import run_ladder

JOIN_EMOJI = "🙋"


@dataclass
class Recruitment:
    host_id: int
    title: str
    description: Optional[str]
    mode: str  # "ladder" | "draw"
    win_count: int  # ladder: 당첨 인원 수 / draw: 뽑을 인원 수
    capacity: Optional[int]
    guild_id: int
    channel_id: int
    message_id: int = 0
    participants: Dict[int, str] = field(default_factory=dict)
    closed: bool = False


class CloseRecruitView(discord.ui.View):
    def __init__(self, cog: "RecruitCog", message_id: int):
        super().__init__(timeout=None)
        self.cog = cog
        self.message_id = message_id

    @discord.ui.button(label="마감하고 진행", style=discord.ButtonStyle.danger, emoji="🔒")
    async def close_button(self, interaction: discord.Interaction, button: discord.ui.Button):
        await self.cog.handle_close(interaction, self.message_id, self)


class RecruitCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.recruitments: Dict[int, Recruitment] = {}

    @app_commands.command(name="모집시작", description="이모지 반응으로 참가자를 모은 뒤 사다리타기/추첨을 진행합니다.")
    @app_commands.describe(
        제목="모집 제목 (예: 오늘 점심 내기)",
        방식="마감 시 어떤 방식으로 결과를 정할지",
        인원="'사다리타기'는 당첨 인원 수, '추첨'은 뽑을 인원 수 (기본 1명)",
        정원="최대 참가 인원 (비워두면 제한 없음)",
        설명="모집 설명 (선택)",
    )
    @app_commands.choices(
        방식=[
            app_commands.Choice(name="사다리타기", value="ladder"),
            app_commands.Choice(name="추첨", value="draw"),
        ]
    )
    async def start_recruit(
        self,
        interaction: discord.Interaction,
        제목: str,
        방식: app_commands.Choice[str],
        인원: Optional[int] = 1,
        정원: Optional[int] = None,
        설명: Optional[str] = None,
    ):
        if interaction.guild_id is None:
            await interaction.response.send_message("⚠️ 이 명령어는 서버 채널에서만 사용할 수 있습니다...", ephemeral=True)
            return

        rec = Recruitment(
            host_id=interaction.user.id,
            title=제목,
            description=설명,
            mode=방식.value,
            win_count=max(1, 인원 or 1),
            capacity=정원,
            guild_id=interaction.guild_id,
            channel_id=interaction.channel_id,
        )

        embed = self._build_embed(rec)
        view = CloseRecruitView(self, message_id=0)  # message_id는 전송 후 채워줌

        await interaction.response.send_message(embed=embed, view=view)
        sent = await interaction.original_response()

        rec.message_id = sent.id
        view.message_id = sent.id
        self.recruitments[sent.id] = rec

        try:
            await sent.add_reaction(JOIN_EMOJI)
        except discord.HTTPException:
            pass

    def _build_embed(self, rec: Recruitment) -> discord.Embed:
        mode_label = "🪜 사다리타기" if rec.mode == "ladder" else "🎲 추첨"
        color = discord.Color.blurple() if rec.mode == "ladder" else discord.Color.gold()

        embed = discord.Embed(title=f"📋 모집: {rec.title}", color=color)
        if rec.description:
            embed.description = rec.description

        cap_text = f" / 정원 {rec.capacity}명" if rec.capacity else ""
        names = list(rec.participants.values())
        participant_text = "\n".join(f"{i+1}. {n}" for i, n in enumerate(names)) if names else "아직 없습니다. 첫 번째 참가자가 되어보세요!"

        embed.add_field(
            name=f"참가 방법",
            value=f"이 메시지에 {JOIN_EMOJI} 반응을 눌러주세요!",
            inline=False,
        )
        embed.add_field(name=f"진행 방식", value=f"{mode_label} (당첨/추첨 {rec.win_count}명)", inline=True)
        embed.add_field(name=f"현재 참가자 ({len(names)}명{cap_text})", value=participant_text, inline=False)

        if rec.closed:
            embed.set_footer(text="🔒 마감되었습니다")
        else:
            embed.set_footer(text="주최자만 '마감하고 진행' 버튼을 누를 수 있습니다.")

        return embed

    async def _refresh_message(self, rec: Recruitment):
        try:
            channel = self.bot.get_channel(rec.channel_id) or await self.bot.fetch_channel(rec.channel_id)
            message = await channel.fetch_message(rec.message_id)
            await message.edit(embed=self._build_embed(rec))
        except (discord.NotFound, discord.HTTPException):
            pass

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: discord.RawReactionActionEvent):
        rec = self.recruitments.get(payload.message_id)
        if rec is None or rec.closed:
            return
        if str(payload.emoji) != JOIN_EMOJI:
            return
        if payload.user_id == self.bot.user.id:
            return

        name = payload.member.display_name if payload.member else f"user-{payload.user_id}"
        rec.participants[payload.user_id] = name
        await self._refresh_message(rec)

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload: discord.RawReactionActionEvent):
        rec = self.recruitments.get(payload.message_id)
        if rec is None or rec.closed:
            return
        if str(payload.emoji) != JOIN_EMOJI:
            return
        if payload.user_id in rec.participants:
            del rec.participants[payload.user_id]
            await self._refresh_message(rec)

    async def handle_close(self, interaction: discord.Interaction, message_id: int, view: CloseRecruitView):
        rec = self.recruitments.get(message_id)
        if rec is None:
            await interaction.response.send_message("⚠️ 모집 정보를 찾을 수 없습니다. (봇이 재시작됐을 수 있음)", ephemeral=True)
            return
        if rec.closed:
            await interaction.response.send_message("이미 마감된 모집입니다.", ephemeral=True)
            return

        is_host = interaction.user.id == rec.host_id
        is_manager = isinstance(interaction.user, discord.Member) and interaction.user.guild_permissions.manage_guild
        if not (is_host or is_manager):
            await interaction.response.send_message("⚠️ 주최자 또는 서버 관리자만 마감할 수 있습니다.", ephemeral=True)
            return

        names = list(rec.participants.values())
        if len(names) < 2:
            await interaction.response.send_message(
                f"⚠️ 참가자가 최소 2명은 있어야 진행할 수 있습니다. (현재: {len(names)}명)", ephemeral=True
            )
            return

        rec.closed = True
        for child in view.children:
            child.disabled = True

        await interaction.response.edit_message(embed=self._build_embed(rec), view=view)
        await self._refresh_message(rec)

        win = min(rec.win_count, len(names))

        if rec.mode == "draw":
            winners = random.sample(names, win)
            lines = "\n".join(f"{i+1}등 {w}" for i, w in enumerate(winners))
            message = (
                f"🎉 **[{rec.title}] 추첨 결과**\n{lines}\n"
                f"(전체 {len(names)}명 중 {win}명 추첨 · 마감: {interaction.user.display_name})"
            )
            await interaction.followup.send(message)
        else:
            results = ["🎉당첨"] * win + ["꽝"] * (len(names) - win)
            random.shuffle(results)
            ladder_result = run_ladder(names, results)
            lines = "\n".join(f"{p} → {r}" for p, r in ladder_result.pairs())
            message = f"🪜 **[{rec.title}] 사다리타기 결과**\n{lines}\n(마감: {interaction.user.display_name})"
            await interaction.followup.send(message)

        del self.recruitments[message_id]


async def setup(bot: commands.Bot):
    await bot.add_cog(RecruitCog(bot))
