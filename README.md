# PII Sanitizer

This program uses [Presidio](https://microsoft.github.io/presidio/) to primitively sanitize inputted text using pseudonymization.

## Authors

* Tanner Weber
* Ben Mortiz
* Xavier Izard

## Usage

`main.py` accepts a single argument that is a string containing the text input
to be sanitized. The sanitized version will be printed out.

``` bash
python3 main.py "My phone number is 555-555-5555"
```

`test.py` will run through all the examples in `test_inputs.txt`.

``` bash
python3 test.py
```
