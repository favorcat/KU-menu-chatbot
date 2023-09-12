import telegram, asyncio

telgm_token = '봇 HTTP API 키'
CHAT_ID = '채널 ID'
bot = telegram.Bot(token = telgm_token)
async def send_text(bot, text):
  await bot.send_message(CHAT_ID, text)

asyncio.run(send_text(bot, "메세지"))