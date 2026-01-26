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

# 7. CREATE BIO

def create_bio(row):
    bio = f"{row['name']} is a {row['faculty_type']} at DA-IICT. "
    bio += f"Educational background: {row['education']}."
    if row["specialization"] != "Not Available":
        bio += f" Research interests include {row['specialization']}."
    return bio

df["bio"] = df.apply(create_bio, axis=1)

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

df["combined_text"] = (
    df["name"] + " " +
    df["faculty_type"] + " " +
    df["bio"] + " " +
    df["specialization_list"].apply(lambda x: " ".join(x))
)

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
