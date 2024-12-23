from docx import Document

def check_formulas(doc):
    errors = []

    # Поиск формул в тексте (для простоты формулы определяются по шаблонам или специальным меткам)
    formula_texts = []  # Список текстов, которые идентифицируются как формулы
    for paragraph in doc.paragraphs:
        # Предположим, что формулы заключены в $$ или имеют другие маркеры
        if "$$" in paragraph.text:
            formula_texts.append(paragraph.text)

    # Проверка правильного оформления формул
    for i, formula in enumerate(formula_texts):
        # Проверка на использование символа умножения
        if "*" in formula:
            errors.append(f"Формула {i+1}: Использован неверный символ умножения '*', следует использовать '×'.")

        # Проверка на правильность нумерации формул
        if f"({i+1})" not in formula:
            errors.append(f"Формула {i+1}: Отсутствует или неправильно оформлена нумерация формулы.")

    return errors

# Пример использования
if __name__ == "__main__":
    doc = Document('your_document.docx')
    formula_errors = check_formulas(doc)
    if formula_errors:
        print("Ошибки в формулах:")
        for error in formula_errors:
            print(f"- {error}")
    else:
        print("Формулы оформлены правильно.")
