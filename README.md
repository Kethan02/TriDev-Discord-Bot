# The Discord Digest Codebase

This project consists of a discord bot that scans messages in a guild and sends you a newsletter every morning with important information on what you missed. The project is written in python and uses discord.py to communicate with discord and MongoDB Altas for the backend.

## Setup

### Cloning the repository

Clone the github repo

```bash
git clone https://github.com/chrisjiang1/TriDev-Discord-Bot.git
```

cd into the repository

```bash
cd TriDev-Discord-Bot
```

Switch to database branch

```bash
git checkout database
```

### Managing Dependencies

Install pipenv

```bash
pip install --user pipenv
```

Install required dependencies with pipenv

```bash
pipenv install
```

## Usage

Run this command

```bash
pipenv run python bot.py
```

## Developer Instructions

To add a package to pipenv run this

```bash
pipenv install [package_name]
```

For debugging and testing the database code, open db.py and scroll down to the bottom of the file. There should be a main method commented out. Uncomment it and run this

```bash
pipenv run python db.py
```
