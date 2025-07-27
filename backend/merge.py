import os
import re

# Example page lists (replace with actual import or definitions if used elsewhere)
pages = {
    "about": "https://www.snuchennai.edu.in/about-us/",
    "academics": "https://www.snuchennai.edu.in/academics/",
    "ug_admissions": "https://www.snuchennai.edu.in/ug-admissions/",
    "pg_admissions": "https://www.snuchennai.edu.in/pg-admissions/",
    "law_admissions": "https://law.snuchennai.edu.in/admissions/",
    "phd_admissions": "https://www.snuchennai.edu.in/phd-admissions/",
    "placements": "https://www.snuchennai.edu.in/placements/",
    "careers": "https://www.snuchennai.edu.in/careers/",
    "faculty": "https://www.snuchennai.edu.in/faculty/",
    "campus_life": "https://www.snuchennai.edu.in/campus-life/",
    "scholarships": "https://www.snuchennai.edu.in/scholarship/"
}

programs = [
    ("btech_ai_ds", "https://www.snuchennai.edu.in/b-tech-ai-data-science/"),
    ("btech_iot", "https://www.snuchennai.edu.in/b-tech-computer-science-and-engineering-with-specialisation-in-iot/"),
    ("btech_cs", "https://www.snuchennai.edu.in/b-tech-computer-science-engineering-cyber-security/"),
    ("bcom", "https://www.snuchennai.edu.in/b-com/"),
    ("bcom_pa", "https://www.snuchennai.edu.in/b-com-professional-accounting/"),
    ("bsc_eco", "https://www.snuchennai.edu.in/b-sc-economics/"),
    ("ba_llb", "https://law.snuchennai.edu.in/academics/")
]


def clean_text(text):
    """Cleans and standardizes text for better LLM training."""
    text = re.sub(r"\n{3,}", "\n\n", text)  # collapse excessive newlines
    text = re.sub(r"[ \t]+", " ", text)  # collapse spaces/tabs
    text = re.sub(r" +\n", "\n", text)  # remove trailing spaces on lines
    text = text.replace("’", "'").replace("“", '"').replace("”", '"')
    return text.strip()


def format_section_title(filename):
    """Converts a file name into a human-readable section title."""
    title = filename.replace(".txt", "").replace("_", " ").title()
    title = re.sub(r"\b(Btech|Bcom|Bsc|Ba Llb)\b", lambda m: m.group(0).upper(), title)
    return title


def merge_scraped_files(output_path= r"C:\\Users\\USER\\Documents\\ollamamodel\\college-data/merged_college_content.txt"):
    expected_files = list(pages.keys()) + [f"program_{name}" for name, _ in programs]
    existing_files = sorted(os.listdir(r"C:\\Users\\USER\\Documents\\ollamamodel\\college-data"))

    # Check for missing files
    missing_files = [file for file in expected_files if f"{file}.txt" not in existing_files]
    if missing_files:
        print(f"Missing files, cannot merge: {missing_files}")
        return

    try:
        with open(output_path, "w", encoding="utf-8") as outfile:
            for file in sorted(existing_files):
                full_path = os.path.join(r"C:\\Users\\USER\\Documents\\ollamamodel\\college-data", file)
                if file.endswith(".txt") and file != os.path.basename(output_path):
                    try:
                        section_title = format_section_title(file)
                        outfile.write("\n" + "=" * 80 + "\n")
                        outfile.write(f"{section_title}\n")
                        outfile.write("=" * 80 + "\n\n")
                        with open(full_path, "r", encoding="utf-8") as infile:
                            raw_text = infile.read()
                            clean = clean_text(raw_text)
                            outfile.write(clean + "\n")
                        print(f"Merged: {file}")
                    except Exception as e:
                        print(f"Merge failed for {file}: {e}")
        print(f"\nMerge complete. Output saved to: {output_path}")
    except Exception as e:
        print(f"Merge failed: {e}")


# Run the function
if __name__ == "__main__":
    merge_scraped_files()
