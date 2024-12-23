import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report
import joblib

# Загрузка данных из файлов
def load_data():
    with open('vvedenie.txt', 'r', encoding='utf-8') as f:
        vvedenie_texts = f.read().split('---')

    with open('zaklyuchenie.txt', 'r', encoding='utf-8') as f:
        zaklyuchenie_texts = f.read().split('---')

    # Создание DataFrame
    data = {'text': vvedenie_texts + zaklyuchenie_texts,
            'label': ['введение'] * len(vvedenie_texts) + ['заключение'] * len(zaklyuchenie_texts)}
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
joblib.dump(model, 'random_forest_model.pkl')
joblib.dump(tfidf_vectorizer, 'tfidf_vectorizer.pkl')