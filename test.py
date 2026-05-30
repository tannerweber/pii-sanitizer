import os

inputs_file = open('test_inputs.txt')
inputs = inputs_file.readlines()

for i in inputs:
    os.system('python3 main.py ' + i)
