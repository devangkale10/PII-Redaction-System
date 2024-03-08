import spacy
import re


def censor_content(content, nlp, label_mapping):

    # Since the model does not have a built-in entity for phone numbers and email IDs
    # We will use a regex pattern to find them
    mobile_pattern = (
        r"(?:\+1\s)?(?:\(\d{3}\)\s?|\d{3}-)\d{3}-\d{4}"  # US phone number pattern
    )
    email_pattern = (
        r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"  # Email ID pattern
    )
    names_pattern1 = r"\\[A-Za-z]+_[A-Za-z]+_?[A-Za-z0-9]*\\"  # Find names using regex pattern corresponding to X_Folder
    names_pattern2 = r"\b[A-Za-z]+-[A-Z]\b"  # Find names using regex pattern corresponding to X_Origin

    # Find names using regex pattern corresponding to X_Folder and X_Origin
    names1 = re.findall(names_pattern1, content)
    names2 = re.findall(names_pattern2, content)

    # Replace names with "█" characters
    for name in names1:
        content = content.replace(name, "█" * len(name))
    for name in names2:
        content = content.replace(name, "█" * len(name))

    names_count = len(names1) + len(names2)

    # Parse the content using the model
    doc = nlp(content)
    # Create a dictionary to store the counts of each entity that will be hidden
    entity_counts = {}

    # Count the number of each entity and store it in the entity_counts dictionary
    for ent in doc.ents:
        if ent.label_ not in entity_counts:
            entity_counts[ent.label_] = 1
        else:
            entity_counts[ent.label_] += 1

    # Replace content with █ using entity text information
    entities_sorted = sorted(doc.ents, key=lambda ent: ent.start_char, reverse=True)
    # Loop through each entity, replacing it with the appropriate number of "█" characters
    for ent in entities_sorted:
        # Calculate the length of the entity text
        blackout_length = len(ent.text)
        # Create a string of "█" characters of the same length as the entity text
        blackout_text = "█" * blackout_length
        # Replace the entity text in the content with the blackout text
        content = content[: ent.start_char] + blackout_text + content[ent.end_char :]

    # Find phone numbers and email IDs using regex pattern
    phone_nums = re.findall(mobile_pattern, content)
    for phone in phone_nums:
        content = content.replace(phone, "█" * len(phone))
    email_IDs = re.findall(email_pattern, content)
    for email in email_IDs:
        content = content.replace(email, "█" * len(email))

    # Update entity counts with phone numbers and email IDs
    entity_counts["PHONE"] = len(phone_nums)
    entity_counts["EMAIL"] = len(email_IDs)

    # Add names_count to PERSON key in entity_counts
    # Check if PERSON key exists in entity_counts first
    # We do this because even spacy recognizes names as PERSON entities
    # and we want to add our regex found names to the PERSON count
    if "PERSON" in entity_counts:
        entity_counts["PERSON"] += names_count
    else:
        entity_counts["PERSON"] = names_count

    # Replacing some key names in the entity_counts dictionary
    # Some keynames like NORP, GPE, LOC are not very intuitive
    # and we will replace them with more intuitive names
    intuitive_entity_counts = {
        label_mapping.get(key, "Unknown"): value for key, value in entity_counts.items()
    }

    # print(intuitive_entity_counts)

    return content, intuitive_entity_counts
