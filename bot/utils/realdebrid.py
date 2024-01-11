import asyncio
import re

import requests
from aiogram.types import Message

from config import bot


class RD:
    def __init__(self, apitoken: str) -> None:
        self.rd_apitoken = apitoken
        self.base_url = "https://api.real-debrid.com/rest/1.0"
        self.header = {"Authorization": "Bearer " + self.rd_apitoken}

    def add_magnet(self, magnet: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/torrents/addMagnet",
            headers=self.header,
            data={"magnet": magnet},
        )

    def add_file(self, file_path: str) -> requests.Response:
        with open(file_path, "rb") as file:
            return requests.put(
                f"{self.base_url}/torrents/addTorrent",
                headers=self.header,
                data=file,
            )

    def info(self, torrent_id: str) -> requests.Response:
        return requests.get(
            f"{self.base_url}/torrents/info/" + str(torrent_id),
            headers=self.header,
        )

    def torrents(self) -> requests.Response:
        return requests.get(
            f"{self.base_url}/torrents",
            headers=self.header,
        )

    def available_hosts(self) -> requests.Response:
        return requests.get(
            f"{self.base_url}/torrents/availableHosts",
            headers=self.header,
        )

    def unrestrict(self, link: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/unrestrict/link",
            headers=self.header,
            data={"link": link},
        )

    def select_files(self, torrent_id: str, files: str) -> requests.Response:
        return requests.post(
            f"{self.base_url}/torrents/selectFiles/" + str(torrent_id),
            headers=self.header,
            data={"files": files},
        )


rd = RD("VWWEB5YIEXJYEFMDTLROBTAHZG75PQBLUMTFDZJM6PIATZWCUYSQ")


def extract_link(message_text):
    match = re.search(r"magnet:\?xt=urn:btih:[a-zA-Z0-9]+", message_text)
    if match:
        return match.group(0)
    return None


async def rb_mirror(message: Message, t_id):
    rd.select_files(t_id, "all")
    progress_message = await bot.send_message(message.chat.id, "Progress: 0%")
    progress = rd.info(t_id).json()["progress"]
    while progress < 100:
        info = rd.info(t_id).json()
        progress = info["progress"]
        speed = info["speed"] or "0"
        await bot.edit_message_text(
            f"Progress {progress}% - Speed: {speed}",
            message.chat.id,
            progress_message.message_id,
        )
        await asyncio.sleep(10)
    link = rd.info(t_id).json()["links"][0]
    unrestrict = rd.unrestrict(link=link).json()
    await bot.edit_message_text(
        f"Link: {unrestrict['download']}", message.chat.id, progress_message.message_id
    )


async def mirror_id(message: Message, file_path=None, torrent_link=None):
    if torrent_link is not None:
        t_id = rd.add_magnet(torrent_link).json()["id"]
        await rb_mirror(message, t_id)
    if file_path is not None:
        t_id = rd.add_file(file_path).json()["id"]
        await rb_mirror(message, t_id)
