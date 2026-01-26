import requests
from bs4 import BeautifulSoup
import json

FACULTY_URLS = {
    "Faculty": "https://www.daiict.ac.in/faculty",
    "Adjunct Faculty": "https://www.daiict.ac.in/adjunct-faculty",
    "Distinguished Professor": "https://www.daiict.ac.in/distinguished-professor",
    "Professor of Practice": "https://www.daiict.ac.in/professor-practice",
    "Adjunct faculty international": "https://www.daiict.ac.in/adjunct-faculty-international"
}

OUTPUT_FILE = "daiict_all_faculty_raw.json"


def scrape_faculty_page(url, faculty_type):
    response = requests.get(url, timeout=10)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    faculty_records = []

    outer_div = soup.find("div", class_="facultyInformation")
    if not outer_div:
        print(f"No faculty container found for {faculty_type}")
        return faculty_records

    faculty_cards = outer_div.find_all("div", class_="facultyDetails")

    for card in faculty_cards:

        personal_div = (card.find("div", class_="personalDetails") or card.find("div", class_="personalDetail") or card.find("div", class_="personalsDetails"))
        name_tag = personal_div.find("h3") if personal_div else None
        name = name_tag.get_text(strip=True) if name_tag else None

        edu_div = card.find("div", class_="facultyEducation")
        education = edu_div.get_text(" ", strip=True) if edu_div else None

        contact_div = card.find("div", class_="contactDetails")

        phone = address = email = None
        if contact_div:
            phone_tag = contact_div.find("span", class_="facultyNumber")
            address_tag = contact_div.find("span", class_="facultyAddress")
            email_tag = contact_div.find("span", class_="facultyemail")

            phone = phone_tag.get_text(strip=True) if phone_tag else None
            address = address_tag.get_text(" ", strip=True) if address_tag else None
            email = email_tag.get_text(strip=True) if email_tag else None

        area_div = card.find("div", class_="areaSpecialization")
        specialization = area_div.get_text(" ", strip=True) if area_div else None

        faculty_records.append({
            "name": name,
            "education": education,
            "phone": phone,
            "address": address,
            "email": email,
            "specialization": specialization,
            "faculty_type": faculty_type
        })

    return faculty_records


def main():
    all_faculty_data = []

    for faculty_type, url in FACULTY_URLS.items():
        print(f"\nScraping {faculty_type}...")
        records = scrape_faculty_page(url, faculty_type)
        print(f"Records scraped from {faculty_type}: {len(records)}")
        all_faculty_data.extend(records)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(all_faculty_data, f, indent=2, ensure_ascii=False)

 
    print("\n Scraping completed successfully")
    print(f" Output file: {OUTPUT_FILE}")
    print(f"TOTAL faculty records scraped: {len(all_faculty_data)}")


if __name__ == "__main__":
    main()
