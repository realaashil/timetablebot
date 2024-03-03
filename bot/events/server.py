import paramiko
from aiogram import Router
from aiogram.filters import IS_MEMBER, IS_NOT_MEMBER, ChatMemberUpdatedFilter
from aiogram.types import ChatMemberUpdated

from config import bot, host, password, username

events_router = Router()


def ssh_fun(host):
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(hostname=host, username=username, password=password)
    return ssh


@events_router.chat_member(ChatMemberUpdatedFilter(IS_MEMBER >> IS_NOT_MEMBER))
async def on_user_leave(event: ChatMemberUpdated):
    if str(event.chat.id) != "-1001848451237":
        return
    user = event.new_chat_member.user.username
    ssh = ssh_fun(host)

    stdin, stdout, stderr = ssh.exec_command(
        f"sudo pkill -KILL -u {user}; sudo userdel -r {user}"
    )
    await bot.send_message(
        "aashil", f"A new user has been deleted to the {host} {user}"
    )


@events_router.chat_member(ChatMemberUpdatedFilter(IS_NOT_MEMBER >> IS_MEMBER))
async def on_user_join(event: ChatMemberUpdated):
    if str(event.chat.id) != "-1001848451237":
        return
