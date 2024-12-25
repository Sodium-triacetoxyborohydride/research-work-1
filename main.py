from docx import Document
import joblib
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

# Загрузка и инициализация лемматизатора
nltk.download('punkt')
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

# Функция для предобработки текста
def preprocess_text(text):
    words = word_tokenize(text.lower())
    lemmatized_text = " ".join([lemmatizer.lemmatize(word) for word in words if word.isalnum()])
    return lemmatized_text

# Функция для выбора типа документа
def select_document_type():
    print("Выберите тип документа для проверки:")
    print("1. Диплом")
    print("2. НИР")
    choice = input("Введите 1 или 2: ")
    return choice

# Загрузка моделей и векторайзеров
def load_models():
    model = joblib.load('gradient_boosting_model.pkl')
    tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')
    return model, tfidf_vectorizer

# Анализ текста с использованием модели
def analyze_text_section(text, model, tfidf_vectorizer, expected_labels):
    preprocessed_text = preprocess_text(text)
    vectorized_text = tfidf_vectorizer.transform([preprocessed_text])
    prediction = model.predict(vectorized_text)[0]

    found_labels = [label for label in expected_labels if label in preprocessed_text]
    not_found_labels = [label for label in expected_labels if label not in found_labels]

    return prediction, found_labels, not_found_labels

# Обработка раздела документа
def process_section(doc, section_title):
    section_start = False
    section_texts = []

    for para in doc.paragraphs:
        if para.text.strip().upper() == section_title:
            section_start = True
        elif section_start and para.text.strip().upper() in ["ВВЕДЕНИЕ", "ЗАКЛЮЧЕНИЕ", "СОДЕРЖАНИЕ"]:
            break
        elif section_start:
            section_texts.append(para.text.strip())

    return " ".join(section_texts)

# Анализ документа в зависимости от типа
def analyze_document(filename, choice):
    doc = Document(filename)
    model, tfidf_vectorizer = load_models()

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

    # Ожидаемые ключевые слова для введения и заключения
    intro_labels = ['актуальность', 'цель', 'задачи', 'объект и предмет', 'гипотеза']
    conclusion_labels = ['изучено', 'решено', 'разработано', 'результаты', 'выводы']

    # Проверка введения
    print("Анализ введения...")
    vvedenie_text = process_section(doc, "ВВЕДЕНИЕ")
    if vvedenie_text:
        prediction, found, not_found = analyze_text_section(vvedenie_text, model, tfidf_vectorizer, intro_labels)
        print(f"Прогноз модели: {prediction}")
        print(f"Во введении найдено: {', '.join(found)}")
        print(f"Не найдено: {', '.join(not_found)}")

    # Проверка заключения
    print("Анализ заключения...")
    zaklyuchenie_text = process_section(doc, "ЗАКЛЮЧЕНИЕ")
    if zaklyuchenie_text:
        prediction, found, not_found = analyze_text_section(zaklyuchenie_text, model, tfidf_vectorizer, conclusion_labels)
        print(f"Прогноз модели: {prediction}")
        print(f"В заключении найдено: {', '.join(found)}")
        print(f"Не найдено: {', '.join(not_found)}")

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
    filename = "tests/Рязанцева НИР 1.docx"
    analyze_document(filename, choice)
