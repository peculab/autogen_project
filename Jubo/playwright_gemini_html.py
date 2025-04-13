import asyncio
from playwright.async_api import async_playwright
from datetime import datetime
from google import genai
import pandas as pd
import os
from dotenv import find_dotenv, load_dotenv
import webbrowser
import markdown2

load_dotenv()

TIME_RANGES = {
    "Last 24 Hours": "last24hours",
    "Last 3 Days": "lastThreeDays",
    "Last 7 Days": "lastSevenDays",
    "Last 14 Days": "lastFourteenDays",
    "Last 30 Days": "lastThirtyDays"
}

load_dotenv(override=True)

dotenv_path = find_dotenv()
print(f"✅ 目前使用的 .env 路徑: {dotenv_path}")

load_dotenv(dotenv_path)

client = genai.Client(api_key=os.getenv('GEMINI_API_KEY'))
username = os.getenv('JUBO_USER')
password = os.getenv('JUBO_PASS')

async def login(page):
    await page.goto("https://demo-vitallink.jubohealth.com/login/us")
    await page.locator('input.MuiInputBase-input[type="text"]').fill(username)
    await page.locator('input.MuiInputBase-input[type="password"]').fill(password)
    await page.locator('button:has-text("Sign In")').click()
    await page.wait_for_timeout(5000)

async def select_dropdown(page, option_value):
    try:
        await page.locator('div[role="combobox"]').first.click()
        await page.wait_for_selector(f'li[data-value="{option_value}"]', timeout=5000)
        await page.locator(f'li[data-value="{option_value}"]').click()
        await page.wait_for_timeout(1500)
    except Exception as e:
        print(f"⚠️ 選擇時間區段 {option_value} 失敗: {e}")

async def check_has_data(page):
    data_row_locator = page.locator('div.sc-fHjqPf.iIQGbB')
    return await data_row_locator.count() > 0

async def extract_data(page):
    records = []
    data_rows = page.locator('div.sc-fHjqPf.iIQGbB')
    row_count = await data_rows.count()

    for i in range(row_count):
        row = data_rows.nth(i)
        columns = await row.locator('div.sc-dAbbOL.bcUgUX, div.sc-hzhJZQ').all_inner_texts()
        records.append(columns)
    return records

def save_to_csv(records, timestamp, headers):
    if not os.path.exists('output'):
        os.makedirs('output')
    output_file = f'output/health_report_{timestamp}.csv'
    df = pd.DataFrame(records, columns=headers)
    df.to_csv(output_file, index=False, encoding='utf-8-sig')
    print(f"✅ CSV 已保存：{output_file}")
    return output_file

def generate_ai_analysis(records, headers):
    print("🤖 Starting Gemini analysis")
    input_text = (
        "Please analyze the following health data and generate professional care recommendations in English, "
        "using clear sections and bullet points. Format example:\n"
        "[Category Name]\nIssues:\n- ...\nRecommendations:\n- ...\n\n"
        "Categories include:\n1. Hypertension\n2. Abnormal Body Temperature\n3. Abnormal Respiratory Rate\n\n"
        "Here is the data:\n"
    )
    for record in records:
        input_text += " | ".join(record) + "\n"

    response = client.models.generate_content(
        model="gemini-2.0-flash",
        contents=input_text,
    )
    result = response.text if hasattr(response, 'text') else "Analysis generation failed."
    print("✅ Gemini analysis complete")
    return result

def generate_html_report(analysis_text, records, headers, timestamp):
    html_file = f'output/health_report_{timestamp}.html'
    # 將 Markdown 轉成 HTML
    analysis_html = markdown2.markdown(analysis_text)

    table_html = "<table border='1'><tr>" + "".join(f"<th>{header}</th>" for header in headers) + "</tr>"
    for record in records:
        table_html += "<tr>" + "".join(f"<td>{cell}</td>" for cell in record) + "</tr>"
    table_html += "</table>"

    html_content = f"""
    <html>
    <head>
        <title>Health Report - {timestamp}</title>
        <style>
            body {{ font-family: Arial, sans-serif; padding: 20px; background-color: #f9f9f9; color: #333; }}
            h1, h2 {{ color: #2c3e50; }}
            table {{ border-collapse: collapse; width: 80%; margin-top: 20px; margin-bottom: 40px; table-layout: fixed; word-break: break-word; background: white; }}
            th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
            th {{ background-color: #3498db; color: white; }}
            tr:nth-child(even) {{ background-color: #f2f2f2; }}
        </style>
    </head>
    <body>
        <h1>Gemini AI Care Recommendations</h1>
        {analysis_html}
        <h2>Patient Data Table</h2>
        {table_html}
    </body>
    </html>
    """

    with open(html_file, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"✅ HTML report generated: {html_file}")
    return html_file

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        context = await browser.new_context()
        page = await context.new_page()

        await login(page)
        await page.goto("https://demo-vitallink.jubohealth.com/healthrecordmonitor")
        await page.wait_for_timeout(3000)

        all_records = []
        headers = ["Type", "Location", "Name", "Temp(°F)", "HR", "RR", "BP(mmHg)", "SpO2(Flow)", "Pain", "Info", "Mood", "Infection S&S", "Prog Note", "Protocol", "Recorded by", "Record Time"]

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")

        for time_label, time_value in TIME_RANGES.items():
            print(f"🕒 測試時間區段: {time_label}")
            await select_dropdown(page, time_value)

            if await check_has_data(page):
                print(f"✅ {time_label} 有資料")
                records = await extract_data(page)
                for record in records:
                    all_records.append([time_label] + record)

                save_to_csv(all_records, timestamp, ["時間區段"] + headers)
            else:
                print(f"❌ {time_label} 無資料")

        await browser.close()

        # ✅ 這裡要特別注意： all_records 是否為空，決定要不要繼續走
        if all_records:
            analysis_text = generate_ai_analysis(all_records, ["時間區段"] + headers)
            html_file = generate_html_report(analysis_text, all_records, ["時間區段"] + headers, timestamp)

            # ✅ 這裡成功之後，再自動打開
            webbrowser.open(f"file://{os.path.abspath(html_file)}")
        else:
            print("⚠️ 無有效資料，流程結束。")

if __name__ == "__main__":
    asyncio.run(main())