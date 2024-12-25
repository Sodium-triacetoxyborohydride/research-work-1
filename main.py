from docx import Document
import joblib

# Функция для выбора типа документа
def select_document_type():
    print("Выберите тип документа для проверки:")
    print("1. Диплом")
    print("2. НИР")
    choice = input("Введите 1 или 2: ")
    return choice

# Загрузка моделей и векторайзеров
def load_models(choice):
    if choice == '1':
        # Логика для дипломов
        model = joblib.load('random_forest_model.pkl')
        tfidf_vectorizer = joblib.load('random_forest_model.pkl')
    elif choice == '2':
        # Логика для НИР
        model = joblib.load('random_forest_model.pkl')
        tfidf_vectorizer = joblib.load('random_forest_model.pkl')
    else:
        raise ValueError("Некорректный выбор. Перезапустите программу и выберите 1 или 2.")
    return model, tfidf_vectorizer

# Анализ документа в зависимости от типа
def analyze_document(filename, choice):
    doc = Document(filename)

    if choice == '1':
        from structure_analyzer import check_document_structure
        from text_format_analyzer import check_text_formatting
        from title_page_checker import check_title_page
        from table_checker import check_tables
        from formula_checker import check_formulas
    elif choice == '2':
        from structure_analyzer_nir import check_document_structure
        from text_format_analyzer_nir import check_text_formatting
        from title_page_checker_nir import check_title_page
        from table_checker_nir import check_tables
        from formula_checker import check_formulas

    # Анализ структуры
    print("Проверка структуры документа...")
    missing_sections = check_document_structure(doc)
    if missing_sections:
        print(f"Отсутствующие разделы: {', '.join(missing_sections)}")
    else:
        print("Все необходимые разделы присутствуют в документе.")

    # Анализ форматирования текста
    print("\nПроверка форматирования текста...")
    check_text_formatting(doc)

    # Проверка титульного листа
    print("\nПроверка титульного листа...")
    title_page_errors = check_title_page(doc)
    if title_page_errors:
        print("Ошибки на титульном листе:")
        for error in title_page_errors:
            print(f"- {error}")
    else:
        print("Титульный лист оформлен правильно.")

    # Проверка таблиц
    print("\nПроверка таблиц...")
    table_errors = check_tables(doc)
    if table_errors:
        print("Ошибки в таблицах:")
        for error in table_errors:
            print(f"- {error}")
    else:
        print("Таблицы оформлены правильно.")

    # Проверка формул
    print("\nПроверка формул...")
    formula_errors = check_formulas(doc)
    if formula_errors:
        print("Ошибки в формулах:")
        for error in formula_errors:
            print(f"- {error}")
    else:
        print("Формулы оформлены правильно.")

# Пример использования
if __name__ == "__main__":
    choice = select_document_type()
    model, tfidf_vectorizer = load_models(choice)
    analyze_document('tests/Рязанцева НИР 1.docx', choice)
