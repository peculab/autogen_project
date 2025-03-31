import os
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

def get_chinese_font_file() -> str:
    """
    只檢查 Windows 系統字型資料夾中是否存在候選中文字型（TTF 格式）。
    若找到則回傳完整路徑；否則回傳 None。
    """
    fonts_path = r"C:\Windows\Fonts"
    candidates = ["kaiu.ttf"]  # 這裡以楷體為例，可依需要修改
    for font in candidates:
        font_path = os.path.join(fonts_path, font)
        if os.path.exists(font_path):
            print("找到系統中文字型：", font_path)
            return os.path.abspath(font_path)
    print("未在系統中找到候選中文字型檔案。")
    return None

def generate_report(output_filename):
    # 先檢查並註冊中文字型
    chinese_font_path = get_chinese_font_file()
    if chinese_font_path:
        # 註冊中文字型，命名為 "ChineseFont"
        pdfmetrics.registerFont(TTFont("ChineseFont", chinese_font_path))
        print("已註冊中文字型：", chinese_font_path)
    else:
        print("無中文字型，將使用預設字型。")
    
    # 建立 PDF 文件
    doc = SimpleDocTemplate(output_filename, pagesize=A4)
    styles = getSampleStyleSheet()
    
    # 建立使用中文字型的段落樣式
    styles.add(ParagraphStyle(
        name='ChineseTitle',
        parent=styles['Title'],
        fontName='ChineseFont' if chinese_font_path else styles['Title'].fontName,
        fontSize=24,
        leading=28
    ))
    styles.add(ParagraphStyle(
        name='ChineseNormal',
        parent=styles['Normal'],
        fontName='ChineseFont' if chinese_font_path else styles['Normal'].fontName,
        fontSize=12,
        leading=14
    ))
    
    # === 1. 標題 (中文標題段落) ===
    title_paragraph = Paragraph("數界國中314班 第一次段考班級成績單", styles["ChineseTitle"])
    
    # === 2. 表格 ===
    # 表格資料：表頭、學生資料列以及班平均
    table_data = [
        ["座號", "國文", "數學", "英文", "社會", "自然", "總分", "平均分", "名次", "班排"],
        [76, 96, 85, 74, 82, 66, 419, 83.8, 1, 1],
        ["班平均", 66.6, 74.2, 62, 78, 68, "", "", "", ""],
    ]
    
    score_table = Table(table_data)
    score_table.setStyle(TableStyle([
        ("BOX", (0,0), (-1,-1), 1, colors.black),
        ("GRID", (0,0), (-1,-1), 0.5, colors.grey),
        ("BACKGROUND", (0,0), (-1,0), colors.lightgrey),
        ("ALIGN", (0,0), (-1,0), "CENTER"),
        ("ALIGN", (0,1), (-1,-1), "CENTER"),
        ("FONTNAME", (0,0), (-1,-1), "ChineseFont" if chinese_font_path else styles['Normal'].fontName)
    ]))
    
    # === 3. 文字敘述或備註區 (中文段落) ===
    text_paragraph_1 = Paragraph(
        "敬愛的家長：這次段考的成績還不錯，因為有家長的督促與孩子的努力，希望下次可以再創佳績。",
        styles["ChineseNormal"]
    )
    text_paragraph_2 = Paragraph(
        "家長的回應：家長自己的段考打 ____ 分，因為孩子的表現 ____ ，我可以在些地方再多加 ____ 。",
        styles["ChineseNormal"]
    )
    
    # 組合所有元素
    elements = [
        title_paragraph,
        Spacer(1, 12),
        score_table,
        Spacer(1, 20),
        text_paragraph_1,
        Spacer(1, 12),
        text_paragraph_2
    ]
    
    # 產生 PDF
    doc.build(elements)
    print("PDF 檔案已儲存至:", output_filename)

if __name__ == "__main__":
    generate_report("exam_report_chinese.pdf")
