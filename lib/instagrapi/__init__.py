import logging
from urllib.parse import urlparse

from .mixins.account import AccountMixin
from .mixins.album import DownloadAlbumMixin, UploadAlbumMixin
from .mixins.auth import LoginMixin
from .mixins.bloks import BloksMixin
from .mixins.challenge import ChallengeResolveMixin
from .mixins.clip import DownloadClipMixin, UploadClipMixin
from .mixins.collection import CollectionMixin
from .mixins.comment import CommentMixin
from .mixins.direct import DirectMixin
from .mixins.hashtag import HashtagMixin
from .mixins.igtv import DownloadIGTVMixin, UploadIGTVMixin
from .mixins.insights import InsightsMixin
from .mixins.location import LocationMixin
from .mixins.media import MediaMixin
from .mixins.password import PasswordMixin
from .mixins.photo import DownloadPhotoMixin, UploadPhotoMixin
from .mixins.private import PrivateRequestMixin
from .mixins.public import (
    ProfilePublicMixin,
    PublicRequestMixin,
    TopSearchesPublicMixin,
)
from .mixins.story import StoryMixin
from .mixins.timeline import ReelsMixin
from .mixins.totp import TOTPMixin
from .mixins.user import UserMixin
from .mixins.video import DownloadVideoMixin, UploadVideoMixin


class Client(
    PublicRequestMixin,
    ChallengeResolveMixin,
    PrivateRequestMixin,
    TopSearchesPublicMixin,
    ProfilePublicMixin,
    LoginMixin,
    DownloadPhotoMixin,
    UploadPhotoMixin,
    DownloadVideoMixin,
    UploadVideoMixin,
    DownloadAlbumMixin,
    UploadAlbumMixin,
    DownloadIGTVMixin,
    UploadIGTVMixin,
    MediaMixin,
    UserMixin,
    InsightsMixin,
    CollectionMixin,
    AccountMixin,
    DirectMixin,
    LocationMixin,
    HashtagMixin,
    CommentMixin,
    StoryMixin,
    PasswordMixin,
    DownloadClipMixin,
    UploadClipMixin,
    ReelsMixin,
    BloksMixin,
    TOTPMixin,
):
    proxy = None
    logger = logging.getLogger("instagrapi")

    def __init__(self, settings: dict = {}, proxy: str = None, **kwargs):
        super().__init__(**kwargs)
        self.settings = settings
        self.set_proxy(proxy)
        self.init()

    def set_proxy(self, dsn: str):
        if dsn:
            assert isinstance(
                dsn, str
            ), f'Proxy must been string (URL), but now "{dsn}" ({type(dsn)})'
            self.proxy = dsn
            proxy_href = "{scheme}{href}".format(
                scheme="http://" if not urlparse(self.proxy).scheme else "",
                href=self.proxy,
            )
            self.public.proxies = self.private.proxies = {
                "http": proxy_href,
                "https": proxy_href,
            }
            return True
        self.public.proxies = self.private.proxies = {}
        return False
