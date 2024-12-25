from docx import Document


def check_document_structure(doc):
    required_sections = [
        "СПИСОК ИСПОЛНИТЕЛЕЙ", "РЕФЕРАТ", "СОДЕРЖАНИЕ",
        "ТЕРМИНЫ И ОПРЕДЕЛЕНИЯ", "ПЕРЕЧЕНЬ СОКРАЩЕНИЙ И ОБОЗНАЧЕНИЙ", "ВВЕДЕНИЕ",
        "ОСНОВНАЯ ЧАСТЬ", "ЗАКЛЮЧЕНИЕ", "СПИСОК ИСПОЛЬЗОВАННЫХ ИСТОЧНИКОВ", "ПРИЛОЖЕНИЕ"
    ]

    found_sections = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip().upper()
        if text in required_sections:
            found_sections.append(text)

    # Проверка на отсутствие необходимых разделов
    missing_sections = [section for section in required_sections if section not in found_sections]
    return missing_sections


def check_headings_format(doc):
    errors = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text.isupper() and not text.endswith('.'):
            continue
        else:
            if text:  # Игнорировать пустые параграфы
                errors.append(f"Неправильно оформленный заголовок: {text}")

    return errors
