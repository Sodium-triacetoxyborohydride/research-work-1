from docx import Document


def check_formulas(doc):
    errors = []

    # Поиск формул в тексте
    for paragraph in doc.paragraphs:
        formula_text = paragraph.text  # Предположим, что формулы разделены специальными тегами или маркерами

        # Проверка на использование правильных символов
        if "*" in formula_text:
            errors.append("Использован неверный символ умножения '*', следует использовать '×'.")

        # Проверка на наличие корректных ссылок на формулы
        if not formula_text.endswith(')'):
            errors.append(f"Формула '{formula_text[:30]}...' не имеет корректной нумерации.")

    return errors
