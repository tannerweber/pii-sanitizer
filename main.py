from presidio_analyzer import AnalyzerEngine
from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import OperatorConfig
import sys

if len(sys.argv) != 2:
    print("Error: Exactly one argument is required.", file=sys.stderr)
    print("Usage: " + sys.argv[0] + " 'text to anonymize'", file=sys.stderr)
    sys.exit(1)

text = sys.argv[1]

# Set up the engine, loads the NLP module (spaCy model by default)
# and other PII recognizers
analyzer = AnalyzerEngine()

# Call analyzer to get results
recognizer_results = analyzer.analyze(
    text=text,
    entities=[
        "PERSON",
        "DATE_TIME",
        "US_SSN",
        "PHONE_NUMBER",
        "LOCATION",
        "EMAIL_ADDRESS",
        "IP_ADDRESS"
    ],
    language='en'
)

# print(recognizer_results)

# Analyzer results are passed to the AnonymizerEngine for anonymization
anonymizer = AnonymizerEngine()
anonymized_text = anonymizer.anonymize(
    text=text,
    analyzer_results=recognizer_results,
    operators={
        "PERSON": OperatorConfig("replace", {"new_value": "👻"}),
        "DATE_TIME": OperatorConfig("replace", {"new_value": "👻"}),
        "US_SSN": OperatorConfig("replace", {"new_value": "👻"}),
        "PHONE_NUMBER": OperatorConfig("replace", {"new_value": "👻"}),
        "LOCATION": OperatorConfig("replace", {"new_value": "👻"}),
        "EMAIL_ADDRESS": OperatorConfig("replace", {"new_value": "👻"}),
        "IP_ADDRESS": OperatorConfig("replace", {"new_value": "👻"}),
    }
)

print(anonymized_text.text)
