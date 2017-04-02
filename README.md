# Mailstat.py


## Description
This script is a wrapper which parse emails stored in plain text in folders specified.
It exports a CSV file with : `the score, isSpam (bool)` for each email.


## Config
You can express the folders to scan and if they contain spam or ham with a conf file like that :


```
path/to/spam/folder,1
path/to/ham/folder,0
```

## Usage

`mailstat.py [-c CONFIG FILE] [-o OUTPUT FILE]`

