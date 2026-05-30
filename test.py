import subprocess
import spacy

nlp = spacy.load("en_core_web_md")

with open("test_inputs.txt", "r", encoding="utf-8") as input_files:
    inputs = input_files.readlines()

for original_text in inputs:
    original_text = original_text.strip()

    result = subprocess.run(
        ["python", "main.py", original_text],
        capture_output=True,
        text=True
    )

    anonymized_text = result.stdout.strip()

    orginal_doc = nlp(original_text)
    anonymized_doc = nlp(anonymized_text)
    sim_scores = []
    sim_scores.append(orginal_doc.similarity(anonymized_doc))

    print(f"Original: {original_text}")
    print(f"Anonymized: {anonymized_text}")
    print(f"Similarity Score: {(orginal_doc.similarity(anonymized_doc)):.3f} \n")

print(f"Average Similarity Score: {(sum(sim_scores) / len(sim_scores)):.3f}")