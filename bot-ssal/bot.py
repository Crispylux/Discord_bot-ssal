"""
사다리타기 / 추첨 디스코드 봇 - 메인 실행 파일

- 특정 서버(길드)에 종속되지 않는 "범용 봇"으로 설계되어 있습니다.
  즉, 봇 초대 링크만 있으면 어떤 디스코드 서버에 초대하더라도 바로
  동작합니다. (서버 ID를 코드에 하드코딩하지 않음)
- 슬래시(/) 커맨드로 동작하며, Discord의 "Message Content Intent" 같은
  민감(Privileged) 인텐트가 전혀 필요하지 않습니다. 개발자 포털에서
  별도 설정을 켜지 않아도 됩니다.
"""
"""개발자: https://github.com/Crispylux"""




import asyncio
import logging
import os

import discord
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    raise SystemExit(
        "DISCORD_TOKEN 환경변수가 설정되어 있지 않습니다. "
        ".env 파일을 만들고 DISCORD_TOKEN=발급받은토큰 형식으로 넣어주세요."
    )

# 개발 중에만 특정 서버에 즉시 반영하고 싶다면 .env에 TEST_GUILD_ID를 넣으세요.
# (범용 배포 시에는 비워두면 됩니다 - 전역 슬래시 커맨드로 동작)
TEST_GUILD_ID = os.getenv("TEST_GUILD_ID")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s] %(levelname)s %(name)s: %(message)s",
)
log = logging.getLogger("ladder-draw-bot")

# 민감하지 않은 기본 인텐트만 사용합니다. (guilds, guild_reactions 포함)
intents = discord.Intents.default()


class LadderDrawBot(commands.Bot):
    def __init__(self):
        super().__init__(command_prefix="!미사용!", intents=intents, help_command=None)

    async def setup_hook(self):
        extensions = ["cogs.ladder", "cogs.draw", "cogs.recruit"]
        for ext in extensions:
            await self.load_extension(ext)
            log.info(f"확장 로드 완료: {ext}")

        if TEST_GUILD_ID:
            guild = discord.Object(id=int(TEST_GUILD_ID))
            self.tree.copy_global_to(guild=guild)
            synced = await self.tree.sync(guild=guild)
            log.info(f"테스트 서버({TEST_GUILD_ID})에 커맨드 {len(synced)}개 동기화 완료")
        else:
            synced = await self.tree.sync()
            log.info(f"전역 슬래시 커맨드 {len(synced)}개 동기화 완료 (모든 서버 반영까지 최대 1시간 소요될 수 있음)")

    async def on_ready(self):
        log.info(f"로그인 완료: {self.user} (id={self.user.id})")
        log.info(f"현재 {len(self.guilds)}개 서버에서 사용 중입니다.")
        await self.change_presence(
            activity=discord.Activity(type=discord.ActivityType.watching, name="/사다리타기 · /추첨")
        )


bot = LadderDrawBot()


async def main():
    async with bot:
        await bot.start(TOKEN)


if __name__ == "__main__":
    asyncio.run(main())
