from docx import Document
from structure_analyzer import check_document_structure
from text_format_analyzer import check_text_formatting
from title_page_checker import check_title_page
from table_checker import check_tables
from formula_checker import check_formulas
import joblib

# Загрузка модели и векторайзера
model = joblib.load('random_forest_model.pkl')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.pkl')

def analyze_text_section(text):
    vectorized_text = tfidf_vectorizer.transform([text])
    prediction = model.predict(vectorized_text)
    sections = ['section', 'part1', 'part2', 'part3']
    return {sections[i]: prediction[0][i] for i in range(len(sections))}

def analyze_document(filename):
    doc = Document(filename)

    print("Проверка структуры документа...")
    missing_sections = check_document_structure(doc)
    if missing_sections:
        print(f"Отсутствующие разделы: {', '.join(missing_sections)}")
    else:
        print("Все необходимые разделы присутствуют в документе.")

    print("\nПроверка форматирования текста...")
    check_text_formatting(doc)

    print("\nПроверка титульного листа...")
    title_page_errors = check_title_page(doc)
    if title_page_errors:
        print("Ошибки на титульном листе:")
        for error in title_page_errors:
            print(f"- {error}")
    else:
        print("Титульный лист оформлен правильно.")

    print("\nПроверка таблиц...")
    table_errors = check_tables(doc)
    if table_errors:
        print("Ошибки в таблицах:")
        for error in table_errors:
            print(f"- {error}")
    else:
        print("Таблицы оформлены правильно.")

    print("\nПроверка формул...")
    formula_errors = check_formulas(doc)
    if formula_errors:
        print("Ошибки в формулах:")
        for error in formula_errors:
            print(f"- {error}")
    else:
        print("Формулы оформлены правильно.")

    print("\nАнализ текстовых разделов...")
    for para in doc.paragraphs:
        prediction = analyze_text_section(para.text)
        print(f"Текст: {para.text[:30]}... -> {prediction}")

# Пример использования
if __name__ == "__main__":
    analyze_document('tests/типа диплом.docx')
