import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import accuracy_score, classification_report
import nltk
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer
import joblib

# Загрузка необходимых ресурсов
nltk.download('punkt')
nltk.download('wordnet')
nltk.download('stopwords')
from nltk.corpus import stopwords

# Инициализация инструментов для предобработки текста
lemmatizer = WordNetLemmatizer()
stop_words = set(stopwords.words('russian'))

# Функция для предобработки текста
def preprocess_text(text):
    words = word_tokenize(text.lower())
    lemmatized_words = [lemmatizer.lemmatize(word) for word in words if word.isalnum() and word not in stop_words]
    return " ".join(lemmatized_words)

# Загрузка данных из файлов
def load_data():
    with open('vvedenie.txt', 'r', encoding='utf-8') as f:
        vvedenie_texts = f.read().split('---')

    with open('zaklyuchenie.txt', 'r', encoding='utf-8') as f:
        zaklyuchenie_texts = f.read().split('---')

    # Присвоение меток для введения
    vvedenie_labels = []
    for text in vvedenie_texts:
        if 'актуальность' in text:
            vvedenie_labels.append('введение: актуальность')
        elif 'цель' in text or 'задачи' in text:
            vvedenie_labels.append('введение: цели и задачи')
        elif 'гипотеза' in text:
            vvedenie_labels.append('введение: гипотеза')
        elif 'объект' in text or 'предмет' in text:
            vvedenie_labels.append('введение: объект и предмет')
        elif 'методология' in text or 'методологическая база' in text:
            vvedenie_labels.append('введение: методологические основы')
        else:
            vvedenie_labels.append('введение: прочее')

    # Присвоение меток для заключения
    zaklyuchenie_labels = []
    for text in zaklyuchenie_texts:
        if 'решено' in text or 'решены' in text:
            zaklyuchenie_labels.append('заключение: решено')
        elif 'изучено' in text or 'разработано' in text:
            zaklyuchenie_labels.append('заключение: изучено и разработано')
        elif 'результаты' in text:
            zaklyuchenie_labels.append('заключение: результаты')
        elif 'выводы' in text:
            zaklyuchenie_labels.append('заключение: выводы')
        else:
            zaklyuchenie_labels.append('заключение: прочее')

    # Объединение данных
    texts = vvedenie_texts + zaklyuchenie_texts
    labels = vvedenie_labels + zaklyuchenie_labels

    # Применение предобработки
    texts = [preprocess_text(text) for text in texts]

    # Создание DataFrame
    data = pd.DataFrame({'text': texts, 'label': labels})

    # Удаление редких классов
    data = data.groupby('label').filter(lambda x: len(x) > 1)

    return data

# Загрузка данных
data = load_data()

# Проверка распределения классов
print(data['label'].value_counts())

# Представление данных в формате TF-IDF
tfidf_vectorizer = TfidfVectorizer(max_features=1000)
X = tfidf_vectorizer.fit_transform(data['text'])
y = data['label']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.33, random_state=42, stratify=y)

# Обучение модели Gradient Boosting
model = GradientBoostingClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Оценка модели
y_pred = model.predict(X_test)
print("Точность модели:", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, zero_division=1))

# Сохранение модели и векторайзера
joblib.dump(model, 'gradient_boosting_model.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')
