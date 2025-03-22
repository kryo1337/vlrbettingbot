# VLR Betting Bot

A betting bot system for Valorant esports matches, built with Python. The system consists of multiple components working together to scrape match data, process betting information, and execute betting strategies.

(Not finished yet)

## Project Structure

- `bot/` - Main betting bot component
- `scraper/` - Data scraping service for Valorant matches
- `db/` - Database initialization and migrations
- `docker-compose.yml` - Container orchestration configuration

## Setup

1. Clone the repository:

```bash
git clone https://github.com/kryo1337/vlrbettingbot.git
cd vlrbettingbot
```

2. Create a `.env` file in the root directory with your configuration:

```bash
cp .env.example .env
# Edit .env with your settings
```

3. Start the services using Docker Compose:

```bash
docker-compose up -d
```

This will start:

- PostgreSQL database (internal port 5432, mapped to host port 5433)
- Redis on port 6379
- Scraper service on port 8000
- Betting bot service

## Environment Variables

Create a `.env` file in the root directory with the following variables:

```env
DISCORD_TOKEN=
DISCORD_GUILD_ID=

DB_NAME=
DB_USER=
DB_PASSWORD=
DB_HOST=db
DB_PORT=5432
```

Make sure to replace empty spaces

## Commands

The bot provides the following Discord slash commands:

| Command        | Description                                          | Usage                                              |
| -------------- | ---------------------------------------------------- | -------------------------------------------------- |
| `/ping`        | Check bot responsiveness                             | `/ping`                                            |
| `/events`      | Display events available to bet                      | `/events`                                          |
| `/leaderboard` | Display top users with most points for a given event | `/leaderboard <event_name>`                        |
| `/bet`         | Place a bet on a match                               | `/bet <event> <match> <team> <score> <top_killer>` |
| `/bets`        | View your active bets                                | `/bets`                                            |
| `/available`   | View available matches to bet on                     | `/available`                                       |
| `/create`      | Create a new betting event                           | `/create <event_name>`                             |
| `/end`         | End event and display top5                           | `yet to be implemented`                            |
| `/history`     | Display history of user bets                         | `yet to be implemented`                            |
| `/check`       | Manually checks result of matches in event           | `yet to be implemented`                            |
