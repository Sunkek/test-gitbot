"""
Just for the resting purposes, I pasted this 
echobot example for aiogram docs
"""

import logging
import os
import pathlib
from datetime import datetime, timedelta

import zipfile
import git
from aiogram import Bot, Dispatcher, executor, types

import helpers

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
GITHUB = "https://github.com/"

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    logging.info(f"{message.from_user.id} - cmd: /help")
    await message.reply(
        "Hello!\nAvailable commands:\n`/repo owner/repository` - returns the repository as a zip.",
        parse_mode="Markdown",
    )

@dp.message_handler()
async def ziprepo(message: types.Message):
    if not message.text.startswith("/repo "):
        return
    logging.info(f"{message.from_user.id} - cmd: {message.text}")
    # TODO Check user input before trying to get the repo from GitHub
    repo = message.text[6:]
    repo_path = repo.split("/")
    temp_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "tmp", *repo_path
    )
    # TODO Create zip directory just in case
    zip_path = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), "zip", " ".join(repo_path)
    )

    archive = pathlib.Path(f"{zip_path}.zip")
    edited_at = datetime.now()
    if archive.exists():
        edited_at = datetime.fromtimestamp(archive.stat().st_mtime)

    if not archive.exists() or edited_at + timedelta(days=7) < datetime.now():
        # TODO Handle different git errors
        # TODO Clone the repo in parallel to avoid blocking
        try:
            git.Repo.clone_from(
                f"{GITHUB}{repo}", temp_path, branch="master"
            )
            logging.info(f"Cloned {repo}")
        except git.exc.GitCommandError as e:
            logging.error(f"Failed to clone {repo}: {e}")
            return await message.reply(
                f"There is no `{repo}` repo on GitHub!",
                parse_mode="Markdown",
            )

        # TODO Pack the archive in parallel to avoid blocking
        zipf = zipfile.ZipFile(f"{zip_path}.zip", "w", zipfile.ZIP_DEFLATED)
        helpers.zipdir(temp_path, zipf)
        zipf.close()
        logging.info(f"Created archive for {repo}")
        
        helpers.rmdir(temp_path)
        logging.info(f"Deleted repository of {repo}")

        edited_at = datetime.fromtimestamp(archive.stat().st_mtime)

    edited_at = edited_at.strftime("%Y-%m-%d %H:%M:%S")
    with open(f"{zip_path}.zip", "rb") as f:
        await message.reply_document(
            document=f, 
            caption=f"`{repo}` as you wanted!\nDownloaded at: {edited_at}",
            parse_mode="Markdown",
        )

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)