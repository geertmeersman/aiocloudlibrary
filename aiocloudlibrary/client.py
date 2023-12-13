"""Cloud Library Client using aiohttp for interacting with the Cloud Library API.

This module provides a client class, CloudLibraryClient, to communicate with the Cloud Library API.
It allows fetching current patron items, borrowing history, holds, saved items, and featured items.

Usage:
- Initialize the CloudLibraryClient with barcode, pin, and library details.
- Use client.current(), client.history(), client.holds(), client.saved(), and client.featured() to fetch data.

Requirements:
- aiohttp library (installed via pip)

Example:
-------
    client = CloudLibraryClient(
        barcode="xxxxxx@mail.com",  # Replace with actual barcode/email
        pin="xxxxxxxx",  # Replace with actual PIN/password
        library="xxxxx"  # Replace with actual library ID
    )
    current = await client.current()
    print(f"Current Patron Items: {current}")

    # Similarly fetch other data using client.history(), client.holds(), client.saved(), client.featured()

"""

import logging
from urllib.parse import urlencode

import aiohttp

from .const import BASE_URL, HEADERS

_LOGGER = logging.getLogger(__name__)


class CloudLibraryClient:
    """Class to communicate with the Cloud Library API."""

    def __init__(self, barcode, pin, library, custom_headers=None):
        """Initialize the CloudLibraryClient."""
        self.barcode = barcode
        self.pin = pin
        self.library = library
        self.session = None
        self.custom_headers = custom_headers or {}

    async def start_session(self):
        """Start a session with the Cloud Library API."""
        if self.session is None:
            self.session = aiohttp.ClientSession(
                headers={**HEADERS, **self.custom_headers}
            )
            await self.login()

    async def close_session(self):
        """Close the session with the Cloud Library API."""
        if self.session:
            await self.session.close()
            self.session = None

    async def login(self):
        """Log in to the Cloud Library API."""
        data = {
            "action": "login",
            "barcode": self.barcode,
            "pin": self.pin,
            "library": self.library,
        }
        for expected_status in [204, 200]:
            await self.request(
                "POST",
                "?_data=root",
                data,
                return_json=False,
                expected_status=expected_status,
                start_session=True,
            )

    async def request(
        self,
        method,
        path,
        data=None,
        return_json=True,
        expected_status=200,
        start_session=False,
    ):
        """Send a request to the Cloud Library API.

        Args:
        ----
            method (str): HTTP method (POST, GET, etc.).
            path (str): Endpoint path.
            data (dict): Request payload.
            return_json (bool): Flag to return JSON response (default: True).
            expected_status (int): Expected HTTP status code.
            start_session (bool): Flag to indicate session start.

        Returns:
        -------
            dict or None: Response payload as JSON or None if return_json is False.
        """
        if self.session is None and not start_session:
            await self.start_session()

        endpoint_path = f"{BASE_URL}/{path}"

        if method.lower() == "get":
            async with self.session.get(
                endpoint_path, headers={**HEADERS, **self.custom_headers}
            ) as response:
                if response.status == expected_status:
                    if return_json:
                        return await response.json()
                    else:
                        return
                else:
                    raise Exception(
                        f"Request to {endpoint_path} failed with status code {response.status}"
                    )
        else:  # For other methods like POST
            async with self.session.post(
                endpoint_path,
                headers={**HEADERS, **self.custom_headers},
                data=urlencode(data).replace("%27", "%22"),
            ) as response:
                if response.status == expected_status:
                    if return_json:
                        return await response.json()
                    else:
                        return
                else:
                    raise Exception(
                        f"Request to {endpoint_path} failed with status code {response.status}"
                    )

    def get_path(self, route=None):
        """Generate the path for a specific route.

        Args:
        ----
            route (str): Route identifier.

        Returns:
        -------
            str: Path for the specified route.
        """
        return f"library/{self.library}/mybooks/{route}?_data=routes/library.$name.mybooks.{route}"

    async def current(self):
        """Retrieve current patron items from the Cloud Library API.

        Returns
        -------
            dict: Response payload for current patron items as JSON.
        """
        path = self.get_path("current")
        data = {
            "format": "",
            "sort": "BorrowedDateDescending",
        }
        return await self.request("POST", path, data)

    async def holds(self):
        """Retrieve the patron's holds from the Cloud Library API.

        Returns
        -------
            dict: Response payload for patron's holds as JSON.
        """
        path = self.get_path("holds")
        data = {
            "format": "",
        }
        return await self.request("POST", path, data)

    async def history(self):
        """Retrieve the patron's borrowing history from the Cloud Library API.

        Returns
        -------
            dict: Response payload for patron's borrowing history as JSON.
        """
        path = self.get_path("history")
        data = {"format": "", "sort": "BorrowedDateDescending", "status": ""}
        return await self.request("POST", path, data)

    async def saved(self):
        """Retrieve the patron's saved items from the Cloud Library API.

        Returns
        -------
            dict: Response payload for patron's saved items as JSON.
        """
        path = self.get_path("saved")
        data = {
            "sort": "TitleAscending",
        }
        return await self.request("POST", path, data)

    async def email(self):
        """Retrieve the patron's email settings from the Cloud Library API.

        Returns
        -------
            dict: Response payload for patron's email settings as JSON.
        """
        path = f"library/{self.library}/email?_data=routes%2Flibrary.%24name.email"
        return await self.request("GET", path)

    async def featured(self):
        """Retrieve the patron's featured items from the Cloud Library API.

        Returns
        -------
            dict: Response payload for patron's featured items as JSON.
        """
        path = f"library/{self.library}/featured?_data=root"
        return await self.request("GET", path)

    async def notifications(self, unread="true", notification_id_to_archive=[]):
        """Retrieve the patron's notifications from the Cloud Library API.

        Returns
        -------
            dict: Response payload for patron's notifications as JSON.
        """
        path = f"library/{self.library}/notifications?_data=routes%2Flibrary.%24name.notifications"
        if len(notification_id_to_archive) > 0:
            data = {
                "onlyUnread": unread,
                "action": "markArchived",
                "notificationIds": notification_id_to_archive,
            }
        else:
            data = {
                "onlyUnread": unread,
            }
        return await self.request("POST", path, data)
