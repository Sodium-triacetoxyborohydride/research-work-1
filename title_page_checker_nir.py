from docx import Document

def check_title_page(doc):
    paragraphs = doc.paragraphs
    errors = []

    required_phrases = [
        "МИНИСТЕРСТВО НАУКИ И ВЫСШЕГО ОБРАЗОВАНИЯ РОССИЙСКОЙ ФЕДЕРАЦИИ",
        "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ ВЫСШЕГО ОБРАЗОВАНИЯ",
        "НАУЧНО-ИССЛЕДОВАТЕЛЬСКАЯ РАБОТА",
        "ПО НАПРАВЛЕНИЮ ПОДГОТОВКИ:",
        "НАПРАВЛЕННОСТЬ",
        "ВЫПОЛНИЛ:",
        "СТУДЕНТ",
        "РУКОВОДИТЕЛЬ ВКР",
        "Нормоконтроль",
        "РУКОВОДИТЕЛЬ ОБРАЗОВАТЕЛЬНОЙ ПРОГРАММЫ"
    ]

    for phrase in required_phrases:
        found = any(phrase in p.text.upper() for p in paragraphs)
        if not found:
            errors.append(f"Отсутствует или неправильно оформлено: '{phrase}'.")

    return errors
