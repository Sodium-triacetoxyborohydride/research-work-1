import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib
import nltk
from nltk.stem import WordNetLemmatizer

# Загрузка и инициализация лемматизатора
nltk.download('wordnet')
lemmatizer = WordNetLemmatizer()

def lemmatize_text(text):
    words = nltk.word_tokenize(text)
    lemmatized_text = " ".join([lemmatizer.lemmatize(word) for word in words])
    return lemmatized_text

# Загрузка данных из файлов
def load_data():
    with open('vvedenie.txt', 'r', encoding='utf-8') as f:
        vvedenie_texts = f.read().split('---')

    with open('zaklyuchenie.txt', 'r', encoding='utf-8') as f:
        zaklyuchenie_texts = f.read().split('---')

    # Лемматизация текста
    vvedenie_texts = [lemmatize_text(text) for text in vvedenie_texts]
    zaklyuchenie_texts = [lemmatize_text(text) for text in zaklyuchenie_texts]

    # Создание спискового представления для меток.
    vvedenie_labels = ['введение' if 'актуальность' not in text else 'введение: актуальность'
                       for text in vvedenie_texts]

    zaklyuchenie_labels = ['заключение: изучен' if 'решен' in text else
                           'заключение: поставлен' if 'решен' in text else
                           'заключение: завершающая часть'
                           for text in zaklyuchenie_texts]

    # Создание DataFrame
    data = {'text': vvedenie_texts + zaklyuchenie_texts,
            'label': vvedenie_labels + zaklyuchenie_labels}
    return pd.DataFrame(data)

# Загрузка данных
df = load_data()

# Предобработка данных
tfidf_vectorizer = TfidfVectorizer(max_features=1000)
X = tfidf_vectorizer.fit_transform(df['text'])
y = df['label']

# Разделение данных на обучающую и тестовую выборки
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Обучение модели Random Forest
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Предсказание и оценка
y_pred = model.predict(X_test)
print("Точность модели (Random Forest):", accuracy_score(y_test, y_pred))
print(classification_report(y_test, y_pred, zero_division=1))

# Сохранение модели и векторайзера
joblib.dump(model, 'random_forest_model_v2.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer_v2.pkl')
