from json.decoder import JSONDecodeError
from pathlib import Path
from typing import Dict

import requests

from ..exceptions import ClientError, ClientLoginRequired
from ..extractors import extract_account, extract_user_short
from ..types import Account, UserShort
from ..utils import dumps, gen_token


class AccountMixin:
    """
    Helper class to manage your account
    """

    def reset_password(self, username: str) -> Dict:
        """
        Reset your password

        Returns
        -------
        Dict
            Jsonified response from Instagram
        """
        response = requests.post(
            "https://www.instagram.com/accounts/account_recovery_send_ajax/",
            data={"email_or_username": username, "recaptcha_challenge_field": ""},
            headers={
                "x-requested-with": "XMLHttpRequest",
                "x-csrftoken": gen_token(),
                "Connection": "Keep-Alive",
                "Accept": "*/*",
                "Accept-Encoding": "gzip,deflate",
                "Accept-Language": "en-US",
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_6) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/11.1.2 Safari/605.1.15",
            },
            proxies=self.public.proxies,
        )
        try:
            return response.json()
        except JSONDecodeError as e:
            if "/login/" in response.url:
                raise ClientLoginRequired(e, response=response)
            raise ClientError(e, response=response)

    def account_info(self) -> Account:
        """
        Fetch your account info

        Returns
        -------
        Account
            An object of Account class
        """
        result = self.private_request("accounts/current_user/?edit=true")
        return extract_account(result["user"])

    def account_security_info(self) -> dict:
        """
        Fetch your account security info

        Returns
        -------
        dict
            Contains useful information on security settings: {
            "is_phone_confirmed": true,
            "is_two_factor_enabled": false,
            "is_totp_two_factor_enabled": true,
            "is_trusted_notifications_enabled": true,
            "is_eligible_for_whatsapp_two_factor": true,
            "is_whatsapp_two_factor_enabled": false,
            "backup_codes": [...],
            "trusted_devices": [],
            "has_reachable_email": true,
            "eligible_for_trusted_notifications": true,
            "is_eligible_for_multiple_totp": false,
            "totp_seeds": [],
            "can_add_additional_totp_seed": false
            }
        """
        return self.private_request("accounts/account_security_info/", self.with_default_data({}))

    def account_edit(self, **data: Dict) -> Account:
        """
        Edit your profile (authorized account)

        Parameters
        ----------
        data: Dict
            Fields you want to edit in your account as key and value pairs

        Returns
        -------
        Account
            An object of Account class
        """
        fields = (
            "external_url",
            "phone_number",
            "username",
            "full_name",
            "biography",
            "email",
        )
        data = {key: val for key, val in data.items() if key in fields}
        if "email" not in data and "phone_number" not in data:
            # Instagram Error: You need an email or confirmed phone number.
            user_data = self.account_info().dict()
            user_data = {field: user_data[field] for field in fields}
            data = dict(user_data, **data)
        # Instagram original field-name for full user name is "first_name"
        data["first_name"] = data.pop("full_name")
        # Biography with entities (markup)
        result = self.private_request("accounts/edit_profile/", self.with_default_data(data))
        biography = data.get("biography")
        if biography:
            self.account_set_biography(biography)
        return extract_account(result["user"])

    def account_set_biography(self, biography: str) -> bool:
        """
        Set biography with entities (markup)

        Parameters
        ----------
        biography: str
            Biography raw text

        Returns
        -------
        bool
            A boolean value
        """
        data = {
            "logged_in_uids": dumps([str(self.user_id)]),
            "raw_text": biography
        }
        result = self.private_request("accounts/set_biography/", self.with_default_data(data))
        return result["status"] == "ok"

    def account_change_picture(self, path: Path) -> UserShort:
        """
        Change photo for your profile (authorized account)

        Parameters
        ----------
        path: Path
            Path to the image you want to update as your profile picture

        Returns
        -------
        UserShort
            An object of UserShort class
        """
        upload_id, _, _ = self.photo_rupload(Path(path))
        result = self.private_request(
            "accounts/change_profile_picture/",
            self.with_default_data({"use_fbuploader": True, "upload_id": upload_id}),
        )
        return extract_user_short(result["user"])

    def news_inbox_v1(self, mark_as_seen: bool = False) -> dict:
        """
        Get old and new stories as is

        Parameters
        ----------
        mark_as_seen: bool
            Mark as seen or not

        Returns
        -------
        dict
        """
        return self.private_request(
            "news/inbox/",
            params={'mark_as_seen': mark_as_seen}
        )