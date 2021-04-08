# test-gitbot

## Installation

You must have Docker on your machine.

1. Clone this repo.
2. Add an `.env` file with contents like `TELEGRAM_BOT_TOKEN=<token>`
3. Build the image with `docker build -t gitbot .`
4. Run the image with `docker run --env-file .env gitbot`

## Usage

`/help` - returns help for the bot

`/repo owner/repository` - returns you the repository you requested as a zip archive.

## Can I try it?

I'll have the bot running for a few days on my cloud. You can find it under `@TestingGitbot` alias.

## TODO

It's clumsy, but it works. I've left a few todo comments in the code for what could be improved.

Makes sense to add a docker bind mount so `zip/` directory is presistent through container restarts.

Would also be great to check if the requested zip is actual instead of 
refreshing only the files which are older than a week, 
but it involves complications with git api auth, or at least scraping github.
