import asyncio
import pandas as pd
from openpyxl.styles import Font
from src.crawler import crawl_domain
from src.extractor import extract_contacts
from src.validator import clean_and_select_email, verify_mx_record

INPUT_PATH = "data/input_domains.csv"
OUTPUT_PATH = "data/sample_output.xlsx"


async def process_company(row: dict, semaphore: asyncio.Semaphore) -> dict:
    company = row["company"]
    website = row["website"]
    print(f"[*] Crawling & enriching: {company} ({website})")

    pages = await crawl_domain(website, semaphore)
    extracted = extract_contacts(pages)

    best_email = clean_and_select_email(extracted["emails"], website)
    mx_status = await asyncio.to_thread(verify_mx_record, best_email)
    phone = extracted["phones"][0] if extracted["phones"] else "Not Found"

    return {
        "Company": company,
        "Website": website,
        "Verified Email": best_email,
        "Deliverability Status": mx_status,
        "Phone": phone,
        "LinkedIn URL": extracted["linkedin"],
    }


def export_formatted_excel(df: pd.DataFrame, path: str) -> None:
    with pd.ExcelWriter(path, engine="openpyxl") as writer:
        df.to_excel(writer, index=False, sheet_name="Enriched Leads")
        ws = writer.sheets["Enriched Leads"]

        for cell in ws[1]:
            cell.font = Font(bold=True)

        for col in ws.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            ws.column_dimensions[col[0].column_letter].width = min(max_len + 4, 45)


async def main() -> None:
    df_input = pd.read_csv(INPUT_PATH)
    semaphore = asyncio.Semaphore(5)

    tasks = [process_company(row, semaphore) for _, row in df_input.iterrows()]
    results = await asyncio.gather(*tasks)

    df_out = pd.DataFrame(results)
    export_formatted_excel(df_out, OUTPUT_PATH)
    print(f"\n[+] Pipeline complete! Saved {len(df_out)} enriched leads to {OUTPUT_PATH}")


if __name__ == "__main__":
    asyncio.run(main())