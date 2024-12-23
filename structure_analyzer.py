from docx import Document


def check_document_structure(doc):
    required_sections = [
        "Индивидуальное задание", "Рецензия", "Содержание",
        "Список сокращений и условных обозначений", "Введение", "Основная часть",
        "Заключение", "Список источников и литературы", "Приложения"
    ]

    found_sections = []

    for paragraph in doc.paragraphs:
        text = paragraph.text.strip()
        if text in required_sections:
            found_sections.append(text)

    missing_sections = [section for section in required_sections if section not in found_sections]
    return missing_sections
