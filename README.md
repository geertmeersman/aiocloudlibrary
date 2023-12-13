# aiocloudlibrary

Asynchronous library to communicate with the Cloud Library API

[![maintainer](https://img.shields.io/badge/maintainer-Geert%20Meersman-green?style=for-the-badge&logo=github)](https://github.com/geertmeersman)
[![buyme_coffee](https://img.shields.io/badge/Buy%20me%20a%20Duvel-donate-yellow?style=for-the-badge&logo=buymeacoffee)](https://www.buymeacoffee.com/geertmeersman)
[![discord](https://img.shields.io/discord/1094198226493636638?style=for-the-badge&logo=discord)](https://discord.gg/QhvcnzjYzA)

[![MIT License](https://img.shields.io/github/license/geertmeersman/aiocloudlibrary?style=flat-square)](https://github.com/geertmeersman/aiocloudlibrary/blob/master/LICENSE)

[![GitHub issues](https://img.shields.io/github/issues/geertmeersman/aiocloudlibrary)](https://github.com/geertmeersman/aiocloudlibrary/issues)
[![Average time to resolve an issue](http://isitmaintained.com/badge/resolution/geertmeersman/aiocloudlibrary.svg)](http://isitmaintained.com/project/geertmeersman/aiocloudlibrary)
[![Percentage of issues still open](http://isitmaintained.com/badge/open/geertmeersman/aiocloudlibrary.svg)](http://isitmaintained.com/project/geertmeersman/aiocloudlibrary)
[![PRs Welcome](https://img.shields.io/badge/PRs-Welcome-brightgreen.svg)](https://github.com/geertmeersman/aiocloudlibrary/pulls)

[![Python](https://img.shields.io/badge/Python-FFD43B?logo=python)](https://github.com/geertmeersman/aiocloudlibrary/search?l=python)

[![github release](https://img.shields.io/github/v/release/geertmeersman/aiocloudlibrary?logo=github)](https://github.com/geertmeersman/aiocloudlibrary/releases)
[![github release date](https://img.shields.io/github/release-date/geertmeersman/aiocloudlibrary)](https://github.com/geertmeersman/aiocloudlibrary/releases)
[![github last-commit](https://img.shields.io/github/last-commit/geertmeersman/aiocloudlibrary)](https://github.com/geertmeersman/aiocloudlibrary/commits)
[![github contributors](https://img.shields.io/github/contributors/geertmeersman/aiocloudlibrary)](https://github.com/geertmeersman/aiocloudlibrary/graphs/contributors)
[![github commit activity](https://img.shields.io/github/commit-activity/y/geertmeersman/aiocloudlibrary?logo=github)](https://github.com/geertmeersman/aiocloudlibrary/commits/main)

## Cloud Library API Example Script

This example script demonstrates how to utilize the `CloudLibraryClient` class from the `aiocloudlibrary` module to interact with the Cloud Library API. It showcases various functionalities available within the client class to retrieve different types of data from the API.

### Usage

1. **Installation:** Ensure the `aiocloudlibrary` module is installed. If not, install it using `pip install aiocloudlibrary`.

2. **Configuration:** Replace the placeholder details (barcode/email, PIN/password, library ID) within the script with actual values.

3. **Functionality Displayed:**

   - `current()`: Fetches the current patron items.
   - `history()`: Retrieves the patron's borrowing history.
   - `holds()`: Retrieves the patron's holds.
   - `saved()`: Retrieves the patron's saved items.
   - `featured()`: Retrieves the patron's featured items.
   - `email()`: Retrieves the patron's email settings.
   - `notifications()`: Retrieves patron notifications (unread or archived).

4. **Execution:** Run the script, and it will sequentially call these functions, displaying the retrieved data for each function.

### Important Notes

- Replace placeholder values (barcode, PIN, library ID) with your actual Cloud Library account details.
- The `notifications()` function demonstrates both fetching unread notifications and archiving specific notifications.
- Make sure you have appropriate access rights and permissions for the Cloud Library API endpoints being accessed.

Feel free to modify the script as needed, adding error handling, logging, or additional functionalities based on your requirements and the Cloud Library API's capabilities.

```python
"""
Example Script: Accessing Cloud Library API with aiocloudlibrary

This script demonstrates fetching current patron items, borrowing history, holds, and saved items
from the Cloud Library API using the aiocloudlibrary library.

Make sure to replace 'xxxxxx@mail.com', 'xxxxxxxx', and 'xxxxx' with actual credentials and library details.

Requirements:
- aiocloudlibrary library (installed via pip)

Usage:
Run the script and observe the output displaying various data from the Cloud Library API.
"""

from aiocloudlibrary import CloudLibraryClient
import asyncio
import json

async def main():
    client = CloudLibraryClient(
        barcode="xxxxxx@mail.com",  # Replace with actual barcode/email
        pin="xxxxxxxx",  # Replace with actual PIN/password
        library="xxxxx"  # Replace with actual library ID
    )

    try:
        current = await client.current()
        print(f"Current Patron Items: {json.dumps(current, indent=2)}")

        history = await client.history()
        print(f"Patron's Borrowing History: {json.dumps(history, indent=2)}")

        holds = await client.holds()
        print(f"Patron's Holds: {json.dumps(holds, indent=2)}")

        saved_items = await client.saved()
        print(f"Patron's Saved Items: {json.dumps(saved_items, indent=2)}")

        featured_items = await client.featured()
        print(f"Patron's Featured Items: {json.dumps(featured_items, indent=2)}")

        email_settings = await client.email()
        print(f"Patron's Email Settings: {json.dumps(email_settings, indent=2)}")

        unread_notifications = await client.notifications()
        print(f"Unread Notifications: {json.dumps(unread_notifications, indent=2)}")

        notification_ids = ["notification_id_1", "notification_id_2"]  # Replace with actual notification IDs
        archived_notifications = await client.notifications(
            unread="false", notification_id_to_archive=notification_ids
        )
        print(f"Archived Notifications: {json.dumps(archived_notifications, indent=2)}")

    finally:
        await client.close_session()

asyncio.run(main())
```
