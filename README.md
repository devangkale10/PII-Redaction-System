# PII Redaction System

Finds and blacks out sensitive information in text files, such as names, dates, phone numbers, addresses and emails. It uses spaCy's transformer model (`en_core_web_trf`) together with regular expressions.

## Setup

```bash
pipenv install
pipenv shell
```

## Usage

```bash
python censoror.py --input 'docs/*.txt' \
  --names --dates --phones --address --email \
  --output 'censored/' \
  --stats stdout
```

| Flag | What it does |
|------|--------------|
| `--input` | Files to process (glob patterns work; repeat the flag for more) |
| `--names` | Redact names, organizations, places, etc. |
| `--dates` | Redact dates |
| `--phones` | Redact phone numbers |
| `--address` | Redact addresses |
| `--email` | Redact email addresses (optional) |
| `--output` | Folder for the results (must already exist). Files are saved with a `.censored` extension |
| `--stats` | Where to write a summary: `stdout`, `stderr`, or a filename |

## What gets redacted

- Names of people, organizations, places, groups and products
- Emails and phone numbers, including extensions
- Addresses, dates and times
- Money amounts, percentages and other numbers

Whitespace between redacted words is also blacked out, so nobody can guess the hidden text from its length.

## Example stats output

```
Filename: 2.txt
Censored Content Stats:
{'Dates': 9, 'Email IDs': 4, 'Persons': 9, 'Phone Numbers': 0, ...}
```

## Testing

```bash
pytest
```

All tests are in `tests/test_all.py`, so the spaCy model only has to load once.

## Limitations

- Supports English only
- Might miss some sensitive information
- Can be slow on large files

## Author

Devang Kale
