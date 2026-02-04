import pandas as pd
import json
import re

# 1. LOAD RAW JSON

INPUT_FILE = "daiict_all_faculty_raw.json"
OUTPUT_JSON = "daiict_faculty_transformed.json"
OUTPUT_CSV = "daiict_faculty_transformed.csv"

with open(INPUT_FILE, "r", encoding="utf-8") as f:
    data = json.load(f)

df = pd.DataFrame(data)

# 2. HANDLE MISSING VALUES

df.fillna("Not Available", inplace=True)

# 3. CLEAN EMAIL

def clean_email(email):
    if email == "Not Available":
        return email
    email = email.lower()
    email = email.replace("[at]", "@").replace("[dot]", ".")
    email = re.sub(r"\s+", "", email)
    return email

df["email"] = df["email"].apply(clean_email)

# 4. CLEAN PHONE

def clean_phone(phone):
    if phone == "Not Available":
        return phone
    return re.sub(r"[^\d]", "", phone)

df["phone"] = df["phone"].apply(clean_phone)

# 5. TOKENIZE SPECIALIZATION

def tokenize_specialization(text):
    if text == "Not Available":
        return []
    return [item.strip().lower() for item in text.split(",")]

df["specialization_list"] = df["specialization"].apply(tokenize_specialization)

# 6. CREATE RESEARCH TAGS

def create_research_tags(spec_list):
    tags = set()
    for item in spec_list:
        for word in item.split():
            if len(word) > 2:
                tags.add(word)
    return sorted(tags)

df["research_tags"] = df["specialization_list"].apply(create_research_tags)

# 7. CLEAN BIO

import re

def clean_text(text):
    if pd.isna(text) or text == "Not Available":
        return "Not Available"
    text = re.sub(r"\s+", " ", text)  # remove extra spaces
    text = text.strip()
    return text

df["bio"] = df["bio"].apply(clean_text)

def extract_keywords_from_bio(bio):
    if bio == "Not Available":
        return []
    
    keywords = []
    common_terms = [
        "machine learning", "deep learning", "data science", "computer vision",
        "natural language processing", "nlp", "artificial intelligence",
        "wireless networks", "cyber security", "iot", "blockchain",
        "robotics", "signal processing", "cloud computing",'ml','dl','ai'
    ]
    
    bio_lower = bio.lower()
    for term in common_terms:
        if term in bio_lower:
            keywords.append(term)
    
    return keywords

df["bio_tags"] = df["bio"].apply(extract_keywords_from_bio)

df["research_tags"] = df.apply(
    lambda row: list(set(row["research_tags"] + row["bio_tags"])),
    axis=1
)



# 8. CLEAN ADDRESS (UTF / ENCODING ONLY)

def clean_address(address):
    if address == "Not Available":
        return address

    # Remove broken UTF characters like â€, â€“ etc.
    address = re.sub(r"[â€™â€“â€”â€]", "", address)

    # Normalize multiple spaces
    address = re.sub(r"\s+", " ", address).strip()

    return address

df["address"] = df["address"].apply(clean_address)

# 9. CREATE COMBINED TEXT (CHATBOT READY)

def build_combined_text(row):
    parts = [
        f"Name: {row['name']}",
        f"Role: {row['faculty_type']}",
        f"Education: {row['education']}",
        f"Biography: {row['bio']}",
        f"Research Areas: {', '.join(row['specialization_list'])}",
        f"Research Keywords: {', '.join(row['research_tags'])}"
    ]
    return " | ".join([p for p in parts if p and p != "Not Available"])

df["combined_text"] = df.apply(build_combined_text, axis=1)


# 10. FINAL COLUMN ORDER

df_final = df[
    [
        "name",
        "faculty_type",
        "education",
        "bio",
        "specialization_list",
        "research_tags",
        "email",
        "phone",
        "address",
        "combined_text"
    ]
].copy()

# Add unique faculty ID
df_final.insert(0, "faculty_id", range(1, len(df_final) + 1))

# 11. SAVE OUTPUTS

df_final.to_json(
    OUTPUT_JSON,
    orient="records",
    indent=2,
    force_ascii=False
)

df_final.to_csv(
    OUTPUT_CSV,
    index=False,
    encoding="utf-8"
)

print("Faculty data cleaned and transformed successfully")
print(f"JSON Output: {OUTPUT_JSON}")
print(f"CSV Output: {OUTPUT_CSV}")
print(f"Total records: {len(df_final)}")
