import aiohttp
import requests


class UUID_NotFoundException(Exception):
    pass


async def get_face(username: str) -> str:
    """
    Minecraftで使用されている名称（mcid)で顔アイコンを検索し、URLを返します。\n
    UUID_NotFoundException 見つからない場合にスローします。
    """
    async with aiohttp.ClientSession() as session:
        async with session.get(f"https://api.mojang.com/users/profiles/minecraft/{username}") as resp:
            try:
                data = await resp.json()
                return f"https://crafatar.com/avatars/{data['id']}"
            except aiohttp.ContentTypeError:
                raise UUID_NotFoundException(f"{username}のUUIDが見つからないよ")


async def save_face_icon(username: str, path="./mcicon/") -> str:
    """
    Minecraftで使用されている名称（mcid)で顔アイコンを検索し、アイコンをサーバーに保存します。\n
    アイコンをサーバーに保存が成功した場合は保存先のPathを返します。 \n
    UUID_NotFoundException 見つからない場合にスローします。
    """
    crafatar = requests.get(await get_face(username=username), stream=True)
    path += username + ".png"
    with open(path, "wb") as f:
        f.write(crafatar.content)
    return path
