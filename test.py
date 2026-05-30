import subprocess
import sys
import spacy

#Input file specfied as CLI-argument
if len(sys.argv) != 2:
    print("Error: Exactly one argument is required.", file=sys.stderr)
    print("Usage: " + sys.argv[0] + " 'input file to test'", file=sys.stderr)
    sys.exit(1)
#Spacy Language Package used for NLP
nlp = spacy.load("en_core_web_lg") 
#Read all test cases from input file
with open(sys.argv[1], "r", encoding="utf-8") as input_files:
    inputs = input_files.readlines()

sim_scores = []

for original_text in inputs:
    original_text = original_text.strip()
    #run main file on each line of test input
    result = subprocess.run(
        ["python", "main.py", original_text],
        capture_output=True,
        text=True
    )
    anonymized_text = result.stdout.strip()
    orginal_doc = nlp(original_text)
    anonymized_doc = nlp(anonymized_text)
    
    #calculate similarity between input and sanitizated result
    sim_scores.append(orginal_doc.similarity(anonymized_doc))

    #display result for each input
    print(f"Original: {original_text}")
    print(f"Anonymized: {anonymized_text}")
    print(f"Similarity Score: {(orginal_doc.similarity(anonymized_doc)):.3f} \n")

#output similarity score for all test cases
print(f"Average Similarity Score: {(sum(sim_scores) / len(sim_scores)):.3f}")