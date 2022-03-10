# Telegram Scraper

Python script to scrape telegram users from a group and move them to another.

## Setup

Install the required dependencies

```bash
python setup.py -i
```

Configure the Telegram accounts you want the script to use

```bash
python setup.py -c
```

A file `.config` will be generated with the info you provided.
You can edit your accounts data directly from there if you want.

## Scrape

Run the scraper

```bash
python scraper.py
```

Chose a group from which extract the members by writing the corresponding number, when prompted.

After that a file `members.csv` will be created.

## Move

Run the mover

```bash
python move.py members.csv
```

Follow the istruction and the script will start moving users using the accounts you provided.
The accounts will rotate to avoid flooding error in Telegram API.
