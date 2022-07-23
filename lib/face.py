import requests


class UUID_NotFoundException(Exception):
    pass


def get_face(username):
    mojang = requests.get(
        f"https://api.mojang.com/users/profiles/minecraft/{username}").json()
    isvalid = mojang.get("id", None)
    if isvalid is None:
        raise UUID_NotFoundException(f"{username}のUUIDが見つからないよ")
    else:
        return f"https://crafatar.com/avatars/{mojang['id']}"
