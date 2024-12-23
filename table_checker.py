from docx import Document


def check_tables(doc):
    tables = doc.tables
    errors = []

    for i, table in enumerate(tables):
        # Проверка на наличие заголовка таблицы
        if not table.rows[0].cells[0].text.startswith("Таблица"):
            errors.append(f"Таблица {i + 1}: Отсутствует заголовок или он неправильно оформлен.")

        # Проверка нумерации таблиц (например, Таблица 1, Таблица 2 и т.д.)
        expected_title = f"Таблица {i + 1}"
        if not table.rows[0].cells[0].text.startswith(expected_title):
            errors.append(f"Таблица {i + 1}: Неправильная нумерация таблицы.")

        # Проверка на размещение таблицы после абзаца
        if i > 0:  # Если это не первая таблица
            prev_table = tables[i - 1]
            if prev_table._element.getparent() is not None:
                errors.append(f"Таблица {i + 1}: Похоже, что таблицы находятся подряд без текста между ними.")

    return errors


# Пример использования
if __name__ == "__main__":
    doc = Document('your_document.docx')
    table_errors = check_tables(doc)
    if table_errors:
        print("Ошибки в таблицах:")
        for error in table_errors:
            print(f"- {error}")
    else:
        print("Таблицы оформлены правильно.")
