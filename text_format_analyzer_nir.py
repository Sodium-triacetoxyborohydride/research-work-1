from docx import Document


def check_text_formatting(doc):
    errors = []

    for paragraph in doc.paragraphs:
        style = paragraph.style.name

        if style != 'Normal':  # Проверка базового стиля
            errors.append(f"Параграф с текстом '{paragraph.text[:30]}...' не соответствует стилю 'Normal'.")

        for run in paragraph.runs:
            font_name = run.font.name or 'N/A'
            font_size = run.font.size.pt if run.font.size else 'N/A'

            if font_name != 'Times New Roman' or font_size != 14:
                errors.append(
                    f"Параграф с текстом '{paragraph.text[:30]}...' не соответствует стилю шрифта Times New Roman 14pt.")

    return errors
