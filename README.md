# Project Name

### The Censorer
Censor sensitive information from text.  
This project uses spaCy's Transformer-based models and regular expressions to identify and replace sensitive information in text.


# Developed By
Name: Devang Kale  
UFID: 3340 9661  
Email: devangkale@ufl.edu  


## Table of Contents

- [Installation and Usage](#installation-and-usage)
- [Flag Information](#flag-information)
- [Function Descriptions](#function-descriptions)
- [Logic Behind the Code](#logic-behind-the-code)
- [Bugs and Assumptions](#bugs-and-assumptions)
- [Testing](#testing)
- [Resources](#resources)

## Installation and Usage

First use 
```bash
pipenv install 
```
to install all the dependencies. 

Then use 
```bash
pipenv shell 
```
to activate the virtual environment.  
  
Then, run the censorer.py file using 
```bash
pipenv run python censoror.py --input '[folder_path]/*.txt' 
--names --dates --phones --address --email[Optional] 
--output '[folder_path]/' 
--stats [stderr, stdout, filename]
```

## Flag Information

- `--input` : The input file path. You can use glob to check multiple file types. For example, `--input 'folder/*.txt'` will check all the .txt files in the folder.  
            And `--input 'folder/*.txt'` `--input 'folder/*.md'` will check all the .txt and .md files in the folder.
- `--names` : Flag to check for names in the text[Required].
- `--dates` : Flag to check for dates in the text.[Required].
- `--phones` : Flag to check for phone numbers in the text.[Required].
- `--address` : Flag to check for addresses in the text.[Required].
- `--email` : Flag to check for email addresses in the text.[Optional].
- `--output` : The output file path. Example usage will be `--output 'folder/'`. Files will be written to this folder with a `.censored` extension.
- `--stats` : The output file path. Output is written either to `stderr`, `stdout` or `filename`.  
            Example usage will be `--stats stderr` or `--stats stdout` or `--stats [filename]`.


## Function Descriptions
`argsparser` : This function is used to parse the command line arguments.
  
`fileprocessor` : Input: `args` from the argsparser. It processes the files. It uses the `censor_content` function to censor the content of the file. It also writes the censored content to the output file. It also writes the statistics to the output file or stderr or stdout.    
  
`censor_content` : Input: `content` of the file, `nlp` model loaded which is `en_core_web_trf`, `label_mapping` to generate intiutive labels for the stats file. It uses the `spaCy` library to identify the sensitive information in the text. It also uses the `re` library to find out EMAIL and PHONE NUMBER. It returns the censored content of the file. It also returns the statistics of the what sensitive information was found and the counts of it.  
  

`censoror` : This is the main function which is used to run the program. It uses the `argsparser` to parse the command line arguments. It uses the `fileprocessor` to process the files.

## Logic Behind the Code
In developing the `censor_content` function, I have accounted for the following logic:
- I have used the `spaCy` library to identify the sensitive information in the text. I have used the `en_core_web_trf` model to identify the sensitive information. I have used the `re` library to find out EMAIL and PHONE NUMBER, since some phone numbers were not being identified by the `spaCy` library.
- The email files contain sections called `X_Folder`, `X_Origin` which contain names of the people who have sent the email. I have used the `re` library to find out the names of the people who have sent the email, since the `spaCy` library was not able to identify this particular type of sensitive information.
- I have also censored whitespaces between the sensitive information. This is because I want to maximize privacy protection. Leaving whitespaces unaccounted for would allow for the possibility of reconstructing the sensitive information, based on the number of characters and the context of the text.

- The format of the statistics file is as such:
    - The filename is printed first.
    - Then the sensitive information found in the file is printed along with the counts of it.
```bash
Filename: 2.txt
Censored Content Stats: 
{'Cardinal Numbers': 4,
 'Dates': 9,
 'Email IDs': 4,
 'Monetary Values': 6,
 'Persons': 9,
 'Phone Numbers': 0,
 'Times': 1}

Filename: 11.txt
Censored Content Stats: 
{'Cardinal Numbers': 40,
 'Dates': 40,
 'Email IDs': 4,
 'Facilities': 1,
 'Geopolitical Entities': 2,
 'Monetary Values': 2,
 'Nationalities or Religious or Political Groups': 1,
 'Ordinal Numbers': 13,
 'Organizations': 39,
 'Percentages': 1,
 'Persons': 48,
 'Phone Numbers': 1,
 'Quantities': 2,
 'Times': 1}
```
- The sensitive information I have chosen to hide is
    - Names : All sorts of proper nouns. They have been grouped further into "Nationalities or Religious or Political Groups", "Geopolitical Entities", "Facilities", "Organizations", "Persons", "Locations", "Products", "Events", "Art Works", "Laws", "Languages"
    - Email addresses : All sorts of email addresses
    - Phone numbers :Phone numbers such as 123-456-7890, (123) 456-7890, +1 123-456-7890, +1 (123) 456-7890
    - Phone number extensions
    - Addresses
    - Dates
    - Times
    - Monetary amounts which include Ordinal and Cardinal Numbers, Percentages
      
I believe that all of these are highly sensitive information and should be censored from the text.

## Bugs and Assumptions
- Language Consideration: The code is tested for English language only. It may not work for other languages.
- Correct Flag Usage: Users are expected to use the correct flags. If the flags are not used correctly, the program will not work as expected.
- Censoring of Sensitive Information: The program may not be able to censor all the sensitive information. It may miss out on some sensitive information. This is because the `spaCy` library is not perfect and may not be able to identify all the sensitive information. Also, the `re` library may not be able to identify all the sensitive information.
- Performance Issues: The program may not work as expected for large files. This is because the `spaCy` library is not optimized for large files. It may take a long time to process large files.
- Output Directory: The specified output directory should exist. If it does not exist, the program will not work as expected.
- Other Important Considerations: I have developed all the tests in a single test file using `@pytest.mark.parametrize`. This is because the nlp model `en_core_web_trf` model takes a considerable time to load, so loading it in every test file would consume a lot of time.

## Testing
`test_all.py` : This file contains all the tests for the program. It uses the `pytest` library to run the tests. It uses `@pytest.mark.parametrize` to run the tests for all types of sensitive information we come across. It uses the `censor_content` function to test the program. 


## Resources
- [spaCy](https://spacy.io/)
- [re](https://docs.python.org/3/library/re.html)
- [argparse](https://docs.python.org/3/library/argparse.html)
- [glob](https://docs.python.org/3/library/glob.html)
- [os](https://docs.python.org/3/library/os.html)
- [pytest](https://docs.pytest.org/en/7.1.x/contents.html)
- [pipenv](https://pypi.org/project/pipenv/)
- [Python](https://www.python.org/)
- [Stack Overflow](https://stackoverflow.com/)
