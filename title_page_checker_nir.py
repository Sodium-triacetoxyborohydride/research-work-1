from docx import Document

def check_title_page(doc):
    paragraphs = doc.paragraphs
    errors = []

    required_phrases = [
        "НАИМЕНОВАНИЕ МИНИСТЕРСТВА", "НАИМЕНОВАНИЕ ОРГАНИЗАЦИИ", "УДК",
        "РЕГИСТРАЦИОННЫЙ НОМЕР", "ГРИФ СОГЛАСОВАНИЯ", "ОТЧЕТ О НИР",
        "НАИМЕНОВАНИЕ НИР", "НАИМЕНОВАНИЕ ОТЧЕТА", "ВИД ОТЧЕТА", "НАУЧНЫЙ РУКОВОДИТЕЛЬ",
        "МЕСТО И ГОД СОСТАВЛЕНИЯ"
    ]

    for phrase in required_phrases:
        found = any(phrase in p.text.upper() for p in paragraphs)
        if not found:
            errors.append(f"Отсутствует или неправильно оформлено: '{phrase}'.")

    return errors
