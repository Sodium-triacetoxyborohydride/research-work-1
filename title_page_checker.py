from docx import Document

def check_title_page(doc):
    paragraphs = doc.paragraphs
    errors = []

    # Требования и ключевые фразы
    required_phrases = [
        "МИНИСТЕРСТВО ОБРАЗОВАНИЯ И НАУКИ",
        "ФЕДЕРАЛЬНОЕ ГОСУДАРСТВЕННОЕ АВТОНОМНОЕ ОБРАЗОВАТЕЛЬНОЕ УЧРЕЖДЕНИЕ",
        "Отделение",  # Это вы замените на конкретное имя
        "направление подготовки",           # Это вы замените на конкретное имя
        "кафедра",                     # Это вы замените на конкретное имя
        "ВЫПУСКНАЯ КВАЛИФИКАЦИОННАЯ РАБОТА",
        "Выполнил студент",
        "Выпускная квалификационная работа защищена:",
        "Обнинск, 2024",
    ]

    # Логика проверки по разделенным требованиям
    for phrase in required_phrases:
        phrase_found = any(phrase in p.text for p in paragraphs)
        if not phrase_found:
            errors.append(f"Отсутствует или неправильно оформлено: '{phrase}'.")

    # Дополнительная проверка выравнивания и формата, если доступно в docx
    # Вы можете расширить код для проверки конкретного выравнивания параграфов

    return errors