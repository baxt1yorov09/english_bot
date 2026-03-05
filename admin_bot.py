import os
import django
from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models
from asgiref.sync import sync_to_async
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes, CallbackQueryHandler
import logging
from datetime import datetime, timedelta

# Set up Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'cefr_bot.settings')
django.setup()

User = get_user_model()

# Configure logging
logging.basicConfig(level=logging.INFO)

def get_admin_keyboard():
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(text="📊 User Statistics", callback_data="admin_stats")],
        [InlineKeyboardButton(text="👥 Active Users", callback_data="admin_active")],
        [InlineKeyboardButton(text="📈 Daily Activity", callback_data="admin_daily")],
        [InlineKeyboardButton(text="🏆 Top Users", callback_data="admin_top")],
        [InlineKeyboardButton(text="📅 Recent Registrations", callback_data="admin_recent")],
        [InlineKeyboardButton(text="🔙 Back to Main", callback_data="admin_back")],
    ])
    return keyboard

async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /admin command"""
    telegram_id = update.effective_user.id
    
    # Check if user is admin (you can add your admin Telegram IDs here)
    ADMIN_IDS = [telegram_id]  # For now, allow any user to access admin features
    
    if telegram_id not in ADMIN_IDS:
        await update.message.reply_text("❌ Access denied. Admin only.")
        return
    
    try:
        # Get statistics
        total_users = await sync_to_async(User.objects.count)()
        active_users = await sync_to_async(
            User.objects.filter(last_login__gte=datetime.now() - timedelta(days=7)).count
        )
        today_users = await sync_to_async(
            User.objects.filter(date_joined__date=datetime.now().date()).count
        )
        
        stats_text = (
            f"🔧 **Admin Panel** 🔧\n\n"
            f"👥 Total Users: {total_users}\n"
            f"🟢 Active Users (7 days): {active_users}\n"
            f"📅 New Users Today: {today_users}\n\n"
            f"Choose an option below:"
        )
        
        await update.message.reply_text(stats_text, reply_markup=get_admin_keyboard())
        
    except Exception as e:
        logging.error(f"Error in admin command: {e}")
        await update.message.reply_text("❌ Error loading admin panel.")

async def handle_admin_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle admin callback queries"""
    query = update.callback_query
    await query.answer()
    
    try:
        data = query.data
        
        if data == "admin_stats":
            # Overall statistics
            total_users = await sync_to_async(User.objects.count)()
            avg_score = await sync_to_async(
                User.objects.aggregate(avg_score=models.Avg('total_score'))
            )['avg_score'] or 0
            
            by_level = await sync_to_async(
                User.objects.values('current_level').annotate(
                    count=models.Count('id')
                ).order_by('-count')
            )
            
            level_stats = "\n".join([f"📊 {item['current_level']}: {item['count']} users" for item in by_level])
            
            stats_text = (
                f"📊 **User Statistics** 📊\n\n"
                f"👥 Total Users: {total_users}\n"
                f"⭐ Average Score: {avg_score:.1f}\n\n"
                f"**Users by Level:**\n{level_stats}"
            )
            
        elif data == "admin_active":
            # Active users (last 7 days)
            active_users = await sync_to_async(
                User.objects.filter(
                    last_login__gte=datetime.now() - timedelta(days=7)
                ).order_by('-last_login')[:10]
            )
            
            user_list = "\n".join([
                f"👤 {user.full_name} (Level: {user.current_level}, Score: {user.total_score})"
                for user in active_users
            ])
            
            stats_text = (
                f"🟢 **Active Users (Last 7 Days)** 🟢\n\n"
                f"{user_list}"
            )
            
        elif data == "admin_daily":
            # Daily activity for last 7 days
            daily_stats = []
            for i in range(7):
                date = datetime.now().date() - timedelta(days=i)
                count = await sync_to_async(
                    User.objects.filter(date_joined__date=date).count
                )
                daily_stats.append(f"📅 {date}: {count} users")
            
            stats_text = (
                f"📈 **Daily Activity (Last 7 Days)** 📈\n\n"
                f"\n".join(daily_stats)
            )
            
        elif data == "admin_top":
            # Top users by score
            top_users = await sync_to_async(
                User.objects.order_by('-total_score')[:10]
            )
            
            user_list = "\n".join([
                f"🏆 {i+1}. {user.full_name} - Score: {user.total_score} (Level: {user.current_level})"
                for i, user in enumerate(top_users)
            ])
            
            stats_text = (
                f"🏆 **Top Users by Score** 🏆\n\n"
                f"{user_list}"
            )
            
        elif data == "admin_recent":
            # Recent registrations
            recent_users = await sync_to_async(
                User.objects.order_by('-date_joined')[:10]
            )
            
            user_list = "\n".join([
                f"👤 {user.full_name} - Joined: {user.date_joined.strftime('%Y-%m-%d %H:%M')}"
                for user in recent_users
            ])
            
            stats_text = (
                f"📅 **Recent Registrations** 📅\n\n"
                f"{user_list}"
            )
            
        elif data == "admin_back":
            await query.edit_message_text("🔙 Returning to main menu...")
            return
        
        else:
            return
        
        await query.edit_message_text(stats_text, reply_markup=get_admin_keyboard())
        
    except Exception as e:
        logging.error(f"Error in admin callback: {e}")
        await query.edit_message_text("❌ Error loading statistics.")

async def stats_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle /stats command for quick stats"""
    try:
        total_users = await sync_to_async(User.objects.count)()
        active_today = await sync_to_async(
            User.objects.filter(last_login__date=datetime.now().date()).count
        )
        
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

def main():
    """Main function to start admin bot"""
    try:
        application = Application.builder().token(settings.TELEGRAM_BOT_TOKEN).build()
        
        # Add handlers
        application.add_handler(CommandHandler("admin", admin_command))
        application.add_handler(CommandHandler("stats", stats_command))
        application.add_handler(CallbackQueryHandler(handle_admin_callback))
        
        logging.info("Admin bot started successfully!")
        
        # Run the bot
        application.run_polling()
        
    except Exception as e:
        logging.error(f"Error starting admin bot: {e}")

if __name__ == "__main__":
    main()
