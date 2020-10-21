# The Discord Digest Codebase

This branch of the repository is dedicated to developing the database back end of the project. It uses MongoDB Atlas to host all of the data and pymongo to communicate with the database.

NOTE: To get access to the database, your IP address must be whitelisted. DM me your public IP so I can add it to the whitelist.

## Setup

### Cloning the repository

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
pipenv run python db.py
```
