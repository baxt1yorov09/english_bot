import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import logging
import asyncio
import random
import webbrowser
from datetime import datetime, timedelta
from ai_services import ai_service
from channel_manager import add_required_channel, remove_required_channel, get_required_channels

User = get_user_model()

# Configure logging
logging.basicConfig(level=logging.INFO)

# CEFR Level keyboard
def get_cefr_keyboard():
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="A1 - Beginner", callback_data="level_A1")],
        [InlineKeyboardButton(text="A2 - Elementary", callback_data="level_A2")],
        [InlineKeyboardButton(text="B1 - Intermediate", callback_data="level_B1")],
        [InlineKeyboardButton(text="B2 - Upper Intermediate", callback_data="level_B2")],
        [InlineKeyboardButton(text="C1 - Advanced", callback_data="level_C1")],
        [InlineKeyboardButton(text="C2 - Proficient", callback_data="level_C2")],
    ])
    return keyboard

def get_main_keyboard():
    keyboard = ReplyKeyboardMarkup([
        [KeyboardButton(" Speaking Partner")],
        [KeyboardButton("📖 Reading")],
        [KeyboardButton("🎙 Listening")],
        [KeyboardButton("🔥 My Streak")],
        [KeyboardButton("📊 My Progress")],
        [KeyboardButton("🏆 Top Users")],
    ], resize_keyboard=True)
    return keyboard

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    telegram_id = update.effective_user.id
    
    # Add your admin Telegram IDs here
    ADMIN_IDS = [
        5475526744,
        5687217504
        # Replace with actual admin Telegram IDs
        # For example: 123456789, 987654321
        # For now, we'll use the first user who registers as admin
    ]
    
    # For demo purposes, make the first user admin
    if not ADMIN_IDS:
        # Get first user and make them admin
        first_user = await sync_to_async(User.objects.first)()
        if first_user and first_user.telegram_id == telegram_id:
            ADMIN_IDS.append(telegram_id)
    
    if telegram_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Access denied. Admin only.\n\nTo become admin, add your Telegram ID to the ADMIN_IDS list in bot.py")
        return
    
    try:
        # Get statistics
        total_users = await sync_to_async(User.objects.count)()
        active_users = await sync_to_async(
            lambda: User.objects.filter(last_login__gte=datetime.now() - timedelta(days=7)).count()
        )()
        today_users = await sync_to_async(
            lambda: User.objects.filter(date_joined__date=datetime.now().date()).count()
        )()
        
        stats_text = (
            f"🔧 **Admin Panel** 🔧\n\n"
            f"👥 Total Users: {total_users}\n"
            f"🟢 Active Users (7 days): {active_users}\n"
            f"📅 New Users Today: {today_users}\n\n"
            f"**Available Commands:**\n"
            f"/stats - Quick statistics\n"
            f"/users - All users list\n"
            f"/active - Active users (7 days)\n"
            f"/top - Top users by score\n"
            f"/channel - Manage required channels"
        )
        
        await update.message.reply_text(stats_text)
        
    except Exception as e:
        logging.error(f"Error in admin command: {e}")
        await update.message.reply_text("❌ Error loading admin panel.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command for quick stats"""
    try:
        total_users = await sync_to_async(User.objects.count)()
        active_today = await sync_to_async(
            lambda: User.objects.filter(last_login__date=datetime.now().date()).count()
        )()
        
        stats_text = (
            f"📊 **Quick Statistics** 📊\n\n"
            f"👥 Total Users: {total_users}\n"
            f"🟢 Active Today: {active_today}\n"
            f"🤖 Bot Status: ✅ Online"
        )
        
        await update.message.reply_text(stats_text)
        
    except Exception as e:
        logging.error(f"Error in stats command: {e}")
        await update.message.reply_text("❌ Error loading statistics.")

async def users_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /users command"""
    try:
        users = await sync_to_async(
            lambda: list(User.objects.all().order_by('-date_joined')[:20])
        )()
        
        user_list = "\n".join([
            f"👤 {user.full_name} - Level: {user.current_level} - Score: {user.total_score}"
            for user in users
        ])
        
        stats_text = (
            f"👥 **Recent Users** 👥\n\n"
            f"{user_list}\n\n"
            f"Showing last 20 users"
        )
        
        await update.message.reply_text(stats_text)
        
    except Exception as e:
        logging.error(f"Error in users command: {e}")
        await update.message.reply_text("❌ Error loading users list.")

async def active_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /active command"""
    try:
        active_users = await sync_to_async(
            lambda: list(User.objects.filter(
                last_login__gte=datetime.now() - timedelta(days=7)
            ).order_by('-last_login')[:15])
        )()
        
        user_list = "\n".join([
            f"🟢 {user.full_name} - Level: {user.current_level} - Score: {user.total_score}"
            for user in active_users
        ])
        
        stats_text = (
            f"🟢 **Active Users (Last 7 Days)** 🟢\n\n"
            f"{user_list}\n\n"
            f"Showing last 15 active users"
        )
        
        await update.message.reply_text(stats_text)
        
    except Exception as e:
        logging.error(f"Error in active command: {e}")
        await update.message.reply_text("❌ Error loading active users.")

async def progress_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /progress command"""
    telegram_id = update.effective_user.id
    
    try:
        user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
        
        # Calculate rank
        rank_count = await sync_to_async(
            lambda: User.objects.filter(total_score__gt=user.total_score).count()
        )()
        rank = rank_count + 1
        
        progress_text = (
            f"📊 **Your Progress** 📊\n\n"
            f"👤 **Name:** {user.full_name}\n"
            f"📈 **Current Level:** {user.current_level}\n"
            f"🎯 **Target Level:** {user.target_level}\n"
            f"⭐ **Total Score:** {user.total_score}\n"
            f"🔥 **Streak:** {user.streak} days\n"
            f"📅 **Member Since:** {user.date_joined.strftime('%Y-%m-%d')}\n\n"
            f"🏆 **Rank:** #{rank}\n\n"
            f"Keep practicing! 🚀"
        )
        
        await update.message.reply_text(progress_text, reply_markup=get_main_keyboard())
        
    except Exception as e:
        logging.error(f"Error in progress command: {e}")
        await update.message.reply_text("❌ Error loading progress data.")

async def top_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /top command"""
    try:
        top_users = await sync_to_async(
            lambda: list(User.objects.order_by('-total_score')[:15])
        )()
        
        user_list = "\n".join([
            f"🏆 {i+1}. {user.full_name} - Score: {user.total_score} - Level: {user.current_level}"
            for i, user in enumerate(top_users)
        ])
        
        stats_text = (
            f"🏆 **Top Users by Score** 🏆\n\n"
            f"{user_list}\n\n"
            f"Showing top 15 users"
        )
        
        await update.message.reply_text(stats_text)
        
    except Exception as e:
        logging.error(f"Error in top command: {e}")
        await update.message.reply_text("❌ Error loading top users.")

async def channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /channel command for managing required channels"""
    telegram_id = update.effective_user.id
    
    # Check if admin
    ADMIN_IDS = [5475526744, 5687217504]
    
    if telegram_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Access denied. Admin only.")
        return
    
    try:
        # For now, show channel management options
        await update.message.reply_text(
            "📢 **Channel Management** 📢\n\n"
            "Options:\n"
            "/addchannel @channel_name - Add required channel\n"
            "/removechannel @channel_name - Remove required channel\n"
            "/listchannels - List all required channels\n"
            "/checkchannel @channel_name - Check channel subscription\n\n"
            "Users will need to subscribe to these channels before using the bot.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="📋 List Current Channels", callback_data="list_channels")],
                [InlineKeyboardButton(text="➕ Add New Channel", callback_data="add_channel")],
                [InlineKeyboardButton(text="🔙 Back to Admin Panel", callback_data="admin_back")],
            ])
        )
        
    except Exception as e:
        logging.error(f"Error in channel command: {e}")
        await update.message.reply_text("❌ Error loading channel management.")

async def add_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /addchannel command"""
    telegram_id = update.effective_user.id
    
    # Check if admin
    ADMIN_IDS = [5475526744, 5687217504]
    
    if telegram_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Access denied. Admin only.")
        return
    
    try:
        # Get channel name from command
        if len(context.args) < 1:
            await update.message.reply_text(
                "❌ Please provide channel name.\n"
                "Usage: /addchannel @channel_name",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
            return
        
        channel_name = context.args[0]
        
        # Remove @ if present and add it back
        if not channel_name.startswith('@'):
            channel_name = '@' + channel_name
        
        # Add to channel manager
        if add_required_channel(channel_name):
            await update.message.reply_text(
                f"✅ **Channel Added Successfully** ✅\n\n"
                f"📢 Channel: {channel_name}\n"
                f"📝 Status: Active\n"
                f"👥 Users will need to subscribe to this channel\n\n"
                f"Use /listchannels to see all required channels.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="📋 List All Channels", callback_data="list_channels")],
                    [InlineKeyboardButton(text="➕ Add Another Channel", callback_data="add_channel")],
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
        else:
            await update.message.reply_text(
                f"⚠️ **Channel Already Exists** ⚠️\n\n"
                f"📢 Channel: {channel_name}\n"
                f"📝 Status: Already in required list\n\n"
                f"Use /listchannels to see all required channels.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="📋 List All Channels", callback_data="list_channels")],
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
        
    except Exception as e:
        logging.error(f"Error in add_channel_command: {e}")
        await update.message.reply_text("❌ Error adding channel.")

async def remove_channel_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /removechannel command"""
    telegram_id = update.effective_user.id
    
    # Check if admin
    ADMIN_IDS = [5475526744, 5687217504]
    
    if telegram_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Access denied. Admin only.")
        return
    
    try:
        # Get channel name from command
        if len(context.args) < 1:
            await update.message.reply_text(
                "❌ Please provide channel name.\n"
                "Usage: /removechannel @channel_name",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
            return
        
        channel_name = context.args[0]
        
        # Remove @ if present and add it back
        if not channel_name.startswith('@'):
            channel_name = '@' + channel_name
        
        # Remove from channel manager
        if remove_required_channel(channel_name):
            await update.message.reply_text(
                f"✅ **Channel Removed Successfully** ✅\n\n"
                f"📢 Channel: {channel_name}\n"
                f"📝 Status: Removed from required list\n"
                f"👥 Users no longer need to subscribe to this channel\n\n"
                f"Use /listchannels to see current required channels.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="📋 List All Channels", callback_data="list_channels")],
                    [InlineKeyboardButton(text="➕ Add Another Channel", callback_data="add_channel")],
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
        else:
            await update.message.reply_text(
                f"❌ **Channel Not Found** ❌\n\n"
                f"📢 Channel: {channel_name}\n"
                f"📝 Status: Not in required list\n\n"
                f"Use /listchannels to see all required channels.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="📋 List All Channels", callback_data="list_channels")],
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
        
    except Exception as e:
        logging.error(f"Error in remove_channel_command: {e}")
        await update.message.reply_text("❌ Error removing channel.")

async def list_channels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /listchannels command"""
    telegram_id = update.effective_user.id
    
    # Check if admin
    ADMIN_IDS = [5475526744, 5687217504]
    
    if telegram_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Access denied. Admin only.")
        return
    
    try:
        # Get channels from channel manager
        channels = get_required_channels()
        
        if not channels:
            await update.message.reply_text(
                "📋 **Required Channels** 📋\n\n"
                "❌ No channels configured.\n"
                "Use /addchannel @channel_name to add channels.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="➕ Add Channel", callback_data="add_channel")],
                    [InlineKeyboardButton(text="🔙 Back to Admin Panel", callback_data="admin_back")],
                ])
            )
            return
        
        channels_text = "\n".join([f"📢 {i+1}. {channel}" for i, channel in enumerate(channels)])
        
        await update.message.reply_text(
            f"📋 **Required Channels** 📋\n\n"
            f"{channels_text}\n\n"
            f"📊 Total: {len(channels)} channels\n"
            f"👥 Users must subscribe to all these channels\n\n"
            f"Use /addchannel to add more or /removechannel to remove.",
            reply_markup=InlineKeyboardMarkup([
                [InlineKeyboardButton(text="➕ Add Channel", callback_data="add_channel")],
                [InlineKeyboardButton(text="🗑️ Remove Channel", callback_data="remove_channel")],
                [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
            ])
        )
        
    except Exception as e:
        logging.error(f"Error in list_channels_command: {e}")
        await update.message.reply_text("❌ Error listing channels.")

async def streak_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Show user's current streak and statistics"""
    telegram_id = update.effective_user.id
    
    try:
        user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
        
        from datetime import date, timedelta
        today = date.today()
        
        # Calculate streak status
        streak_status = ""
        if user.last_practice_date == today:
            streak_status = "🔥 **Active today!**"
        elif user.last_practice_date == today - timedelta(days=1):
            streak_status = "⏰ **Practice today to keep your streak!**"
        else:
            streak_status = "❌ **Streak broken - start a new one!**"
        
        # Milestone badges
        badges = []
        if user.streak >= 30:
            badges.append("🏆 **Master Streaker** (30+ days)")
        elif user.streak >= 14:
            badges.append("🥈 **Dedicated Learner** (14+ days)")
        elif user.streak >= 7:
            badges.append("🥉 **Week Warrior** (7+ days)")
        elif user.streak >= 3:
            badges.append("⭐ **Rising Star** (3+ days)")
        elif user.streak >= 1:
            badges.append("🌟 **Beginner** (1+ days)")
        
        badge_text = "\n".join(badges) if badges else "📚 **No badges yet - start practicing!**"
        
        streak_text = (
            f"🔥 **Your Streak Statistics** 🔥\n\n"
            f"📅 **Current Streak:** {user.streak} days\n"
            f"📊 **Status:** {streak_status}\n"
            f"🗓️ **Last Practice:** {user.last_practice_date or 'Never'}\n\n"
            f"🏆 **Your Badges:**\n{badge_text}\n\n"
            f"💡 **Tips:**\n"
            f"• Practice daily to maintain your streak\n"
            f"• Earn bonus coins for longer streaks\n"
            f"• Unlock special achievements at milestones"
        )
        
        await update.message.reply_text(streak_text, reply_markup=get_main_keyboard())
        
    except Exception as e:
        logging.error(f"Error in streak_command: {e}")
        await update.message.reply_text("❌ Error loading streak data.")

async def check_channel_subscription(user_id, channel_username):
    """Check if user is subscribed to channel"""
    try:
        # Remove @ if present
        channel = channel_username.replace('@', '')
        
        # Check subscription using bot API
        chat_member = await context.bot.get_chat_member(
            chat_id=f"@{channel}",
            user_id=user_id
        )
        
        return chat_member.status in ['member', 'administrator', 'creator']
    except Exception as e:
        logging.error(f"Error checking channel subscription: {e}")
        return False

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /start command"""
    telegram_id = update.effective_user.id
    telegram_username = update.effective_user.username
    
    # Required channels (admin can manage these)
    REQUIRED_CHANNELS = [
          # Replace with actual channels
        "@SirojiddinovAcademy"
    ]
    
    # Check channel subscriptions
    unsubscribed_channels = []
    for channel in REQUIRED_CHANNELS:
        try:
            chat_member = await context.bot.get_chat_member(
                chat_id=channel,
                user_id=telegram_id
            )
            if chat_member.status not in ['member', 'administrator', 'creator']:
                unsubscribed_channels.append(channel)
        except Exception as e:
            # If bot is admin, it can check membership
            # If not admin, skip the check for this channel
            logging.warning(f"Could not check channel {channel}: {e}")
            # Don't add to unsubscribed if we can't check
            continue
    
    # If user is not subscribed to required channels
    if unsubscribed_channels:
        channel_buttons = []
        for channel in unsubscribed_channels:
            channel_buttons.append([InlineKeyboardButton(text=f"📢 {channel}", url=f"https://t.me/{channel.replace('@', '')}")])
        
        channel_buttons.append([InlineKeyboardButton(text="✅ I've Subscribed", callback_data="check_subscription")])
        
        await update.message.reply_text(
            "🔒 **Subscription Required** 🔒\n\n"
            "To use this bot, you need to subscribe to the following channels:\n\n"
            + "\n".join([f"📢 {channel}" for channel in unsubscribed_channels]) +
            "\n\nPlease subscribe to all channels and then click the button below:",
            reply_markup=InlineKeyboardMarkup(channel_buttons)
        )
        return
    
    try:
        user, created = await sync_to_async(User.objects.get_or_create)(
            telegram_id=telegram_id,
            defaults={
                'telegram_username': telegram_username,
                'username': f"tg_{telegram_id}",
                'email': f"{telegram_id}@telegram.bot"
            }
        )
        
        if not user.full_name:
            await update.message.reply_text(
                "👋 Welcome to CEFR English Exam Simulator! 🎉\n\n"
                "Let's complete your registration first.\n\n"
                "What's your full name?"
            )
            context.user_data['registration_step'] = 'full_name'
        else:
            # Check if user can get daily bonus
            from datetime import date
            today = date.today()
            daily_bonus_given = False
            
            if user.last_practice_date != today:
                # Give daily login bonus
                await sync_to_async(user.update_streak)()
                bonus_coins = 10 + (user.streak * 2)  # Bonus increases with streak
                bonus_xp = 5 + user.streak
                await sync_to_async(user.add_coins)(bonus_coins)
                await sync_to_async(user.add_xp)(bonus_xp)
                await sync_to_async(user.save)()
                daily_bonus_given = True
            
            welcome_msg = f"👋 Welcome back, {user.full_name}! 👋\n\n"
            
            if daily_bonus_given:
                welcome_msg += f"🎉 **Daily Login Bonus!** 🎉\n"
                welcome_msg += f"💰 +{bonus_coins} coins\n"
                welcome_msg += f"⚡ +{bonus_xp} XP\n"
                if user.streak == 1:
                    welcome_msg += f"🔥 **New streak started!**\n\n"
                elif user.streak % 7 == 0:
                    welcome_msg += f"🔥 **{user.streak} day streak! Amazing!** 🔥\n\n"
                else:
                    welcome_msg += f"� **Streak: {user.streak} days**\n\n"
            
            welcome_msg += f"� Current Level: {user.current_level}\n"
            welcome_msg += f"🎯 Target Level: {user.target_level}\n"
            welcome_msg += f"⭐ Total Score: {user.total_score}\n"
            welcome_msg += f"🔥 Streak: {user.streak} days\n"
            welcome_msg += f"💰 Coins: {user.coins}\n"
            welcome_msg += f"⚡ XP: {user.xp}\n\n"
            welcome_msg += "Choose what you want to practice:"
            
            await update.message.reply_text(welcome_msg, reply_markup=get_main_keyboard())
    except Exception as e:
        logging.error(f"Error in start_command: {e}")
        await update.message.reply_text("Sorry, there was an error. Please try again.")

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle text messages"""
    text = update.message.text
    user_id = update.effective_user.id
    
    try:
        # Handle registration
        if 'registration_step' in context.user_data:
            step = context.user_data['registration_step']
            
            if step == 'full_name':
                context.user_data['full_name'] = text
                await update.message.reply_text("Great! Now, how old are you? 📅")
                context.user_data['registration_step'] = 'age'
                
            elif step == 'age':
                try:
                    age = int(text)
                    if age < 10 or age > 100:
                        await update.message.reply_text("Please enter a valid age between 10 and 100:")
                        return
                    
                    context.user_data['age'] = age
                    await update.message.reply_text(
                        "What's your current English level? 📚",
                        reply_markup=get_cefr_keyboard()
                    )
                    context.user_data['registration_step'] = 'current_level'
                except ValueError:
                    await update.message.reply_text("Please enter a valid number:")
                    
            elif step == 'current_level':
                # Handle callback query for level selection
                return
        
        # Handle main menu
        elif text == "� My Streak":
            await streak_command(update, context)
            
        elif text == "� My Progress":
            await progress_command(update, context)
            
        elif text == "🏆 Top Users":
            await top_command(update, context)
            
        elif text == " Speaking Partner":
            await update.message.reply_text(
                "🎧 Speaking Partner\n\n"
                "Opening AI speaking partner in your browser...\n"
                "https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice#demo"
            )
            # Open website in browser
            webbrowser.open("https://www.sesame.com/research/crossing_the_uncanny_valley_of_voice#demo")
            
        elif text == "📖 Reading":
            await update.message.reply_text(
                "📖 Reading Practice\n\n"
                "Opening reading resources in your browser...\n"
                "https://jamesclear.com/articles"
            )
            # Open website in browser
            webbrowser.open("https://jamesclear.com/articles")
            
        elif text == "🎙 Listening":
            await update.message.reply_text(
                "🎙 Listening Practice\n\n"
                "Opening listening resources in your browser...\n"
                "https://www.podcastsinenglish.com/"
            )
            # Open website in browser
            webbrowser.open("https://www.podcastsinenglish.com/")
            
        elif text == "📊 My Progress":
            try:
                user = await sync_to_async(User.objects.get)(telegram_id=user_id)
                
                progress_text = (
                    f"📊 Your Progress 📈\n\n"
                    f"👤 {user.full_name}\n"
                    f"📈 Current Level: {user.current_level}\n"
                    f"🎯 Target Level: {user.target_level}\n"
                    f"⭐ Total Score: {user.total_score}\n"
                    f"🎤 Speaking Score: {user.speaking_score:.1f}/5.0\n"
                    f"✍️ Writing Score: {user.writing_score:.1f}/5.0\n"
                    f"🔥 Streak: {user.streak} days\n"
                    f"💰 Coins: {user.coins}\n"
                    f"⚡ XP: {user.xp}\n"
                    f"⏱️ Total Practice: {user.total_practice_time} min\n"
                    f"📅 Daily Goal: {user.daily_goal} min"
                )
                
                await update.message.reply_text(progress_text, reply_markup=get_main_keyboard())
            except Exception as e:
                await update.message.reply_text("Error loading progress. Please try again.")
                
    except Exception as e:
        logging.error(f"Error in handle_message: {e}")
        await update.message.reply_text("Sorry, there was an error. Please try again.")

async def handle_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle callback queries"""
    query = update.callback_query
    await query.answer()
    
    try:
        data = query.data
        
        if data.startswith("level_"):
            # Handle level selection
            level = data.split("_")[1]
            context.user_data['current_level'] = level
            
            # Check if this is current level or target level selection
            if context.user_data.get('registration_step') == 'current_level':
                await query.edit_message_text(
                    "Great! What's your target English level? 🎯",
                    reply_markup=get_cefr_keyboard()
                )
                context.user_data['registration_step'] = 'target_level'
            elif data.startswith("channel_management"):
            await query.edit_message_text(
                "📢 **Channel Management** 📢\n\n"
                "Options:\n"
                "/addchannel @channel_name - Add required channel\n"
                "/removechannel @channel_name - Remove required channel\n"
                "/listchannels - List all required channels\n"
                "/checkchannel @channel_name - Check channel subscription\n\n"
                "Users will need to subscribe to these channels before using the bot.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="📋 List Current Channels", callback_data="list_channels")],
                    [InlineKeyboardButton(text="➕ Add New Channel", callback_data="add_channel")],
                    [InlineKeyboardButton(text="🔙 Back to Admin Panel", callback_data="admin_back")],
                ])
            )
            
        elif data.startswith("add_channel"):
            await query.edit_message_text(
                "➕ **Add New Channel**\n\n"
                "Please send the channel name using the command:\n\n"
                "/addchannel @channel_name\n\n"
                "Example: /addchannel @mychannel",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
            
        elif data.startswith("remove_channel"):
            await query.edit_message_text(
                "🗑️ **Remove Channel**\n\n"
                "Please send the channel name using the command:\n\n"
                "/removechannel @channel_name\n\n"
                "Example: /removechannel @mychannel",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
            
        elif data.startswith("list_channels"):
            # For now, show hardcoded channels (you can fetch from database later)
            channels = ["@SirojiddinovAcademy"]
            
            if not channels:
                await query.edit_message_text(
                    "📋 **Required Channels** 📋\n\n"
                    "❌ No channels configured.\n"
                    "Use /addchannel @channel_name to add channels.",
                    reply_markup=InlineKeyboardMarkup([
                        [InlineKeyboardButton(text="➕ Add Channel", callback_data="add_channel")],
                        [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                    ])
                )
                return
            
            channels_text = "\n".join([f"📢 {i+1}. {channel}" for i, channel in enumerate(channels)])
            
            await query.edit_message_text(
                f"📋 **Required Channels** 📋\n\n"
                f"{channels_text}\n\n"
                f"📊 Total: {len(channels)} channels\n"
                f"👥 Users must subscribe to all these channels\n\n"
                f"Use /addchannel to add more or /removechannel to remove.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="➕ Add Channel", callback_data="add_channel")],
                    [InlineKeyboardButton(text="🗑️ Remove Channel", callback_data="remove_channel")],
                    [InlineKeyboardButton(text="🔙 Back to Channel Management", callback_data="channel_management")],
                ])
            )
            
        elif data.startswith("check_subscription"):
            # Re-check channel subscriptions
            telegram_id = update.effective_user.id
            from channel_manager import get_required_channels
            REQUIRED_CHANNELS = get_required_channels()
            
            unsubscribed_channels = []
            for channel in REQUIRED_CHANNELS:
                try:
                    chat_member = await context.bot.get_chat_member(
                        chat_id=channel,
                        user_id=telegram_id
            else:
                # Complete registration
                full_name = context.user_data.get('full_name', 'User')
                age = context.user_data.get('age', 0)
                current_level = context.user_data.get('current_level', 'A1')
                target_level = level
                
                # Update user in database
                telegram_id = update.effective_user.id
                user = await sync_to_async(User.objects.get)(telegram_id=telegram_id)
                user.full_name = full_name
                user.age = age
                user.current_level = current_level
                user.target_level = target_level
                user.daily_goal = 30  # Default daily goal
                await sync_to_async(user.save)()
                
                await query.edit_message_text(
                    " Registration completed!\n\n"
                    "Name: {full_name}\n"
                    "Level: {current_level} → {target_level}\n"
                    "Daily Goal: 30 minutes\n\n"
                    "You're all set! Choose what you want to practice:",
                    reply_markup=None
                )
                
                # Send new message with main keyboard
                await query.message.reply_text(
                    "Main Menu:",
                    reply_markup=get_main_keyboard()
                        [InlineKeyboardButton(text=" Back to Admin Panel", callback_data="admin_back")],
                    ])
                )
                return
            
            channels_text = "\n".join([f" {i+1}. {channel}" for i, channel in enumerate(channels)])
            
            await query.edit_message_text(
                f" **Required Channels** \n\n"
                f"{channels_text}\n\n"
                f" Total: {len(channels)} channels\n"
                f" Users must subscribe to all these channels\n\n"
                f"Admin can manage these channels using /channel command.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=" Add Channel", callback_data="add_channel")],
                    [InlineKeyboardButton(text=" Remove Channel", callback_data="remove_channel")],
                    [InlineKeyboardButton(text=" Back to Admin Panel", callback_data="admin_back")],
                ])
            )
            
        elif data.startswith("add_channel"):
            await query.edit_message_text(
                " **Add Channel** \n\n"
                "To add a new required channel, use:\n"
                "/addchannel @channel_name\n\n"
                "The bot will require users to subscribe to this channel.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text=" Back to Channel Management", callback_data="back_to_channel")],
                    [InlineKeyboardButton(text=" Back to Admin Panel", callback_data="admin_back")]
                ])
            )
            
        elif data.startswith("back_to_channel"):
            await query.edit_message_text(
                " **Channel Management** \n\n"
                "Options:\n"
                "/addchannel @channel_name - Add required channel\n"
                "/removechannel @channel_name - Remove required channel\n"
                "/listchannels - List all required channels\n"
                "/checkchannel @channel_name - Check channel subscription\n\n"
                "Users will need to subscribe to these channels before using the bot.",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton(text="📋 List Current Channels", callback_data="list_channels")],
                    [InlineKeyboardButton(text="➕ Add New Channel", callback_data="add_channel")],
                    [InlineKeyboardButton(text="🔙 Back to Admin Panel", callback_data="admin_back")],
                ])
            )
            
        elif data.startswith("admin_back"):
            await query.edit_message_text(
                "🔙 **Admin Panel** 🔙\n\n"
                "Use /admin to return to the admin panel.",
                reply_markup=None
            )
            
    except Exception as e:
        logging.error(f"Error in handle_callback: {e}")
        try:
            await query.edit_message_text("Sorry, there was an error. Please try again.")
        except:
            # If we can't edit the message, just answer the callback
            pass

def main():
    """Main function to start bot"""
    try:
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("start", start_command))
        application.add_handler(CommandHandler("admin", admin_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(CommandHandler("users", users_command))
        application.add_handler(CommandHandler("active", active_command))
        application.add_handler(CommandHandler("top", top_command))
        application.add_handler(CommandHandler("progress", progress_command))
        application.add_handler(CommandHandler("streak", streak_command))
        application.add_handler(CommandHandler("channel", channel_command))
        application.add_handler(CommandHandler("addchannel", add_channel_command))
        application.add_handler(CommandHandler("removechannel", remove_channel_command))
        application.add_handler(CommandHandler("listchannels", list_channels_command))
        application.add_handler(CallbackQueryHandler(handle_callback))
        application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
        
        logging.info("Bot started successfully!")
        
        # Run the bot
        application.run_polling()
        
    except Exception as e:
        logging.error(f"Error starting bot: {e}")

if __name__ == "__main__":
    main()
