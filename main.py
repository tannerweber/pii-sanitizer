from presidio_anonymizer import AnonymizerEngine
from presidio_anonymizer.entities import RecognizerResult, OperatorConfig
from presidio_analyzer import AnalyzerEngine
import sys

# Checks for prepositions relating to fixed times and adds one where needed to maintain grammatical correctness
def get_time_augment(result, text):

    if result.start == 0:
        return "At "
    elif result.start < 3:
        return "at "
    elif text[result.start - 2] == '.':
        return "At "
    elif result.start == 3 and text[result.start - 3:result.start - 1].strip().lower() in ("in", "on", "at", "of", "by"):
        return ""
    elif result.start < 4:
        return "at "
    elif text[result.start - 4:result.start - 1].strip().lower() in ("in", "on", "at", "of", "by"):
        return ""
    elif result.start < 6:
        return "at "
    elif result.start == 6 and text[result.start - 6:result.start - 1].strip().lower() == "after":
        return ""
    elif result.start < 7:
        return "at "
    elif text[result.start - 7:result.start - 1].strip().lower() == "after":
        return ""
    elif result.start == 7 and text[result.start - 7:result.start - 1].strip().lower() in ("after", "before", "during"):
        return ""
    elif result.start < 8:
        return "at "
    elif text[result.start - 8:result.start - 1].strip().lower() in ("before", "during"):
        return ""
    else:
        return "at "

if len(sys.argv) != 2:
    print("Error: Exactly one argument is required.", file=sys.stderr)
    print("Usage: " + sys.argv[0] + " 'text to anonymize'", file=sys.stderr)
    sys.exit(1)

# Prompt text to be anonymized
prompt_text = sys.argv[1]

# Anonymizer and Analyzer engine initialization
analyzer = AnalyzerEngine()
anonymizer = AnonymizerEngine()

# Call to analyzer to determine indecies of PII
# entities list must include all types of PII to be identified
recognizer_results = analyzer.analyze(text=prompt_text,
                                      entities=["PERSON",
                                                "DATE_TIME",
                                                "US_SSN",
                                                "PHONE_NUMBER",
                                                "LOCATION",
                                                "EMAIL_ADDRESS",
                                                "IP_ADDRESS"],
                                      score_threshold=.8,
                                      language='en')

# Dictionaries of unmasked PII to their ID
name_IDs     = {}
date_IDs     = {}
ssn_IDs      = {}
phone_IDs    = {}
location_IDs = {}
email_IDs    = {}
ip_IDs       = {}

# Indices starting at A for each category of PII
name_index     = ord('A')
date_index     = ord('A')
ssn_index      = ord('A')
phone_index    = ord('A')
location_index = ord('A')
email_index    = ord('A')
ip_index       = ord('A')

# Assigns a unique ID to all instances of each unique identifier
# then creates a custom anonymizer operator for ID
operators = {}
for result in recognizer_results:

    match result.entity_type:
        case "PERSON":
            name = prompt_text[result.start:result.end]
            result.entity_type = name
            if name not in name_IDs:
                name_IDs[name]  = name_index
                name_index     += 1
                operators[name] = OperatorConfig(operator_name="replace",
                                                 params={"new_value": f"Person {chr(name_IDs[name])}"})

        case "DATE_TIME":
            date = prompt_text[result.start:result.end]
            result.entity_type = date
            if date not in date_IDs:
                date_IDs[date]  = date_index
                date_index     += 1
                augment = get_time_augment(result, prompt_text)
                operators[date] = OperatorConfig(operator_name="replace",
                                                 params={"new_value": f"{augment}Date {chr(date_IDs[date])}"})

        case "US_SSN":
            ssn = prompt_text[result.start:result.end]
            result.entity_type = ssn
            if ssn not in ssn_IDs:
                ssn_IDs[ssn]   = ssn_index
                ssn_index     += 1
                operators[ssn] = OperatorConfig(operator_name="replace",
                                                params={"new_value": f"SSN {chr(ssn_IDs[ssn])}"})

        case "PHONE_NUMBER":
            phone = prompt_text[result.start:result.end]
            result.entity_type = phone
            if phone not in phone_IDs:
                phone_IDs[phone] = phone_index
                phone_index     += 1
                operators[phone] = OperatorConfig(operator_name="replace",
                                                  params={"new_value": f"Phone Number {chr(phone_IDs[phone])}"})

        case "LOCATION":
            location = prompt_text[result.start:result.end]
            result.entity_type = location
            if location not in location_IDs:
                location_IDs[location] = location_index
                location_index        += 1
                operators[location] = OperatorConfig(operator_name="replace",
                                                 params={"new_value": f"Location {chr(location_IDs[location])}"})

        case "EMAIL_ADDRESS":
            email = prompt_text[result.start:result.end]
            result.entity_type = email
            if email not in email_IDs:
                email_IDs[email] = email_index
                email_index     += 1
                operators[email] = OperatorConfig(operator_name="replace",
                                                  params={"new_value": f"Email Address {chr(email_IDs[email])}"})

        case "IP_ADDRESS":
            ip = prompt_text[result.start:result.end]
            result.entity_type = ip
            if ip not in ip_IDs:
                ip_IDs[ip]    = ip_index
                ip_index     += 1
                operators[ip] = OperatorConfig(operator_name="replace",
                                               params={"new_value": f"IP Address {chr(ip_IDs[ip])}"})

# Anonymize the passed prompt using the results from recognizer and custom operators
results = anonymizer.anonymize(text=prompt_text,
                              analyzer_results=recognizer_results,
                              operators=operators)

# Output just anonymized text to console
print(results.text)