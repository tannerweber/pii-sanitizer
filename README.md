# PII Sanitizer

This program uses [Presidio](https://microsoft.github.io/presidio/) to primitively sanitize inputted text using pseudonymization.

Before
```
'Draft a memo regarding the acquisition of CloudStream Inc. for $450M. The lead negotiator is Sarah Jenkins from our Austin office, and we need to finalize this by Friday, the 14th.'
```
After
```
'Draft a memo regarding the acquisition of CloudStream Inc. for $450M. The lead negotiator is Person A from our Location A office, and we need to finalize this by Date A.'
```

## Authors

* Tanner Weber
* Ben Mortiz
* Xavier Izard

## Setup

Dependencies can be found in `requirements.txt`.
Perform
``` bash
pip install -r requirements.txt
```

## Usage

`main.py` accepts a single argument that is a string containing the text input
to be sanitized. The sanitized version will be printed out.

``` bash
python3 main.py 'My phone number is 555-555-5555'
```

`test.py` is a testing utility used to evaluate the effectiveness of the test anonymizaiton process implemented in main.py. The script reads a list of test inputs from the text file specified as an arguement. A similarity score comparing the original input with the results of the anonymizaiton process are provided for each line of input as well as a average for all inputs in a file.

``` bash
python3 test.py test_input.txt
```
