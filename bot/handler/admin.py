from aiogram import Router
from aiogram.filters.command import Command, CommandStart
from aiogram.types import Message

from bot.utils.filters import IsAdmin
from bot.utils.realdebrid import extract_link, mirror_id
from config import bot

admin_router = Router()
admin_router.message.filter(IsAdmin())


@admin_router.message(CommandStart())
async def start(message: Message):
    await message.answer("Hello You are a admin!")


@admin_router.message(Command("mirror"))
async def mirror(message: Message):
    msg_reply = message.reply_to_message
    if (
        msg_reply
        and msg_reply.document
        and msg_reply.document.mime_type == "application/x-bittorrent"
    ):
        # Download the torrent file
        file_path = f"./downloads/{msg_reply.document.file_name}.torrent"
        await bot.download(
            msg_reply.document.file_id,
            destination=file_path,
        )
        await mirror_id(message, file_path=file_path)
        return
    if msg_reply and msg_reply.text:
        torrent_link = extract_link(msg_reply.text)
        await mirror_id(message, torrent_link=torrent_link)
        return

    torrent_link = extract_link(message.text)
    await mirror_id(message, torrent_link=torrent_link)
    return
