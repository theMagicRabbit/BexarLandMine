# Bexar Land Mine

A webscraper to datamine the Bexar County Tax records.

## Prerequisites

1. Python 3.13 installed in your $PATH (this may work on earlier versions of
   python3, but it has only been tested against 3.13)
2. An understanding of python virtual environments is helpful.
3. An understanding of git and/or github.
4. Willingness to use a CLI.
5. [SQLite3](https://sqlite.org/)

This has only been used on x86_64 Arch Linux. It should run anywhere that
python3 runs, but this has not been validated by me.

## Install

These instructions assume you are using a Unix-like shell, such as bash. On
Windows, you would need to modify these commands for PowerShell. They should
be fairly close.

1. Clone the repo (or download the latest archive and unpack.)
   `git clone git@github.com:theMagicRabbit/BexarLandMine.git`
2. Open the repo directory with a terminal.
    `cd BexarLandMine`
3. Create a python virtual environment.
    `python3 -m venv venv`
4. Activate the virtual environment.
    `source ./venv/bin/activate`
5. Install pip requrements to the virtual environment.
    `python3 -m pip install -r requrements.txt`

Commands as one block to copy and paste all in one go if you prefer:

```bash
git clone git@github.com:theMagicRabbit/BexarLandMine.git
cd BexarLandMine
python3 -m venv venv
source ./venv/bin/activate
python3 -m pip install -r requrements.txt
```

## Running

The config can be modified if you wish to control where the SQLite database
or the log file is stored. You can also adjust the wait between queries. By
default, this program waits 1-5 seconds between queries to reduce the load on
the Bexar County website and to avoid being blocked. This may not be enough to
avoid being blocked and you are taking on any risks by using this software. The
most likely risk is your IP address being restricted from accessing the Public
records website. This and any other consequences are risks you take on by running
this software. Datamining a government website, or any website, can have legal
reprecusions and you should educate youself on those risks before using this
software.

By default, the scraper will only scrape the first 1,000 account numbers. There
are far more than 1,000 properties in Bexar county and this number will need to be
adjusted in the config to suit your needs. Unfortunatly, the account numbers are
not sequential and are 12 digits long, which is to say, there are 1 trillion
possible account numbers. This application would take well over 31,000 years
to check every possible account number. Any practical use of this application
would require running multiple instances at the same time. At that point, you
start running the risk of DDoSing a government website. **You** are responsible
for the consequences of **your** use of this software.


1. Open a terminal to the repo directory you cloned during the install.
2. Activate your virtual environment (same as step 4 in the install.)
3. Run the module.
    `python -m BexarLandMine`

Output will be to the SQLite database file configured in the config.toml file.
The collected data can then be used from the database or transfered somewhere
else, as you see fit.

