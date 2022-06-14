import wikipedia
import re

from Bestie_Robot.modules.helper_funcs.decorators import bestie_cmd
from telegram.error import BadRequest
from telegram.ext import CallbackContext
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup

from telegram.constants import ParseMode


@bestie_cmd(command='wiki', can_disable=True)
async def wiki(update: Update, context: CallbackContext):
    kueri = re.split(pattern="wiki", string = update.effective_message.text)
    message = update.effective_message
    wikipedia.set_lang("en")
    if not str(kueri[1]):
        await update.effective_message.reply_text("Enter keywords!")
    else:
        try:
            pertama = await update.effective_message.reply_text("🔄 Loading...")
            keyboard = InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            text="🔧 More Info...", url=wikipedia.page(kueri).url
                        )
                    ]
                ]
            )
            context.bot.editMessageText(
                chat_id=update.effective_chat.id,
                message_id=pertama.message_id,
                text=wikipedia.summary(kueri, sentences=10),
                reply_markup=keyboard,
            )
        except wikipedia.PageError as e:
            await message.reply_text(f"⚠ Error: {e}")
        except BadRequest as et:
            await message.reply_text(f"⚠ Error: {et}")
        except wikipedia.exceptions.DisambiguationError as eet:
            await message.reply_text(
                f"⚠ Error\n There are too many query! Express it more!\nPossible query result:\n{eet}"
            )
            """
