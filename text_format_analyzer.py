def check_text_formatting(doc):
    for paragraph in doc.paragraphs:
        if paragraph.style.name != 'Normal':
            print(f"Параграф с текстом '{paragraph.text[:30]}...' не соответствует стилю 'Normal'.")

        for run in paragraph.runs:
            font_name = run.font.name
            font_size = run.font.size.pt if run.font.size else None

            if font_name != 'Times New Roman' or font_size != 14:
                print(
                    f"Параграф с текстом '{paragraph.text[:30]}...' не соответствует стилю шрифта Times New Roman 14pt.")
