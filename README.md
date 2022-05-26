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

It will ask you to choose the source group from will users have to be scraped.
Then it collects all the extracted members within the file `members.csv`.

## Move

Run the mover

```bash
python move.py 
```
The default source file it will use to add users is `members.csv`, but you can also specify a different file:
```bash
python move.py members.csv
```

Follow the istruction and the script will start moving users using the accounts you provided.

The account in charge to add users to the group will be rotated each 20 users, in order to avoid flooding error in Telegram API.
You can also change this default number within the file `preferences.py`

Extraction:
```
# This configuration variable specifies how many users
# an account can add before it is switched to the next
# one in the list
MAX_USERS_MOVED = 20
```


## Limitations

1. You need to be admin of the destination PUBLIC group (the one where users will be added)

2. Due to a bug within Telethon scraping groups bigger than 5000 members can
lead to internal errors.

3. Only accounts with a defined username can be moved

4. An error message will be printed if a user has a policy preference which prevents him/her to be added to 
a group
