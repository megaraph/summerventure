import requests
import uuid

from pathlib import Path
from django.conf import settings

STATICFILES_ROOT = settings.STATICFILES_DIRS[0]
LOCAL_MEDIA = Path.joinpath(Path.cwd(), "users", "media")

AVATAR_FILE_SUFFIX = "svg"
DEFAULT_AVATAR_STATIC_LOCATION = "base/images/icons/"
DEFAULT_AVATAR_NAME = "default-avatar"
DEFAULT_AVATAR_FILE = Path.joinpath(
    Path(STATICFILES_ROOT),
    DEFAULT_AVATAR_STATIC_LOCATION,
    f"{DEFAULT_AVATAR_NAME}.{AVATAR_FILE_SUFFIX}",
)


def get_avatar(username) -> tuple[bool, bytes, str]:
    url = f"https://avatars.dicebear.com/api/adventurer-neutral/{username}.{AVATAR_FILE_SUFFIX}"
    res = requests.get(url=url, stream=True)

    new_file_prefix = str(uuid.uuid1())
    new_file_name = f"{new_file_prefix}.{AVATAR_FILE_SUFFIX}"

    try:
        if res.ok:
            extracted_img = res.content
        else:
            with open(DEFAULT_AVATAR_FILE, "rb") as f:
                extracted_img = f.read()
    except:
        return (False, None)

    return (True, extracted_img, new_file_name)
