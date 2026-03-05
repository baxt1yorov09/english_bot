# Admin Panel Configuration

## How to Set Up Admin Access

### Method 1: Add Admin IDs Directly in Code

1. Open `bot.py` file
2. Find the `admin_command` function (around line 59)
3. Look for this section:
```python
ADMIN_IDS = [
    # Replace with actual admin Telegram IDs
    # For example: 123456789, 987654321
    # For now, we'll use the first user who registers as admin
]
```

4. Replace with your actual Telegram IDs:
```python
ADMIN_IDS = [
    123456789,  # Replace with your Telegram ID
    987654321,  # Replace with another admin's Telegram ID
]
```

### Method 2: Get Your Telegram ID

1. Start the bot: `/start`
2. Send any message to the bot
3. Check the bot logs or database for your user ID
4. Add your ID to the ADMIN_IDS list

### Method 3: First User Becomes Admin (Current Setup)

Currently, the bot is configured to automatically make the **first registered user** an admin. This is for testing purposes.

### Admin Commands Available

Once you have admin access, you can use:

- `/admin` - Show admin panel with statistics
- `/stats` - Quick statistics overview
- `/users` - List of recent users (last 20)
- `/active` - Active users in last 7 days (last 15)
- `/top` - Top users by score (top 15)

### Security Recommendation

For production use, it's recommended to:
1. Add specific Telegram IDs to ADMIN_IDS list
2. Remove the automatic admin assignment code
3. Keep admin IDs secure and limited

### Example Configuration

```python
ADMIN_IDS = [
    123456789,  # Main admin
    987654321,  # Secondary admin
    555666777,  # Moderator
]
```

Replace the numbers with actual Telegram user IDs.
