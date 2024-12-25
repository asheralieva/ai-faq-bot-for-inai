import json
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.svm import LinearSVC
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.http import JsonResponse
from .models import QuestionAnswer

# Load FAQ data
with open("faq/faq_data.json", "r", encoding="utf-8") as file:
    faq_data = json.load(file)

faq_list = []
for section, qna in faq_data.items():
    for question, answer, *_  in qna:
        faq_list.append({"section": section, "question": question, "answer": answer})
faq_df = pd.DataFrame(faq_list)

# Train the model
vectorizer = TfidfVectorizer(stop_words=None)
X = vectorizer.fit_transform(faq_df["question"])
y = faq_df["section"]

classifier = LinearSVC()
classifier.fit(X, y)

def preprocess_query(query):
    return query.lower().strip()

def get_answer(user_query):
    user_query = preprocess_query(user_query)
    user_vector = vectorizer.transform([user_query])
    predicted_section = classifier.predict(user_vector)[0]
    section_questions = faq_df[faq_df["section"] == predicted_section]

    similarities = cosine_similarity(user_vector, vectorizer.transform(section_questions["question"]))
    closest_question_index = similarities.argmax()
    answer = section_questions.iloc[closest_question_index]["answer"]

    if similarities.max() < 0.3:
        return "Sorry, I don't understand your request."
    return answer

# Django view

# def faq_view(request):
#     if request.method == "POST":
#         user_input = request.POST.get("question", "")
#         response = get_answer(user_input)
#         return JsonResponse({"response": response})
#     return render(request, "faq/index.html")

def faq_view(request):
    if request.method == "POST":
        # Получаем вопрос от пользователя
        question = request.POST.get('question', '').strip()  # Удаляем лишние пробелы
        # Генерируем ответ (или получаем из другой логики)
        response = get_answer(question)  # Функция для получения ответа

        # Сохраняем вопрос и ответ в базу данных
        if question:
            QuestionAnswer.objects.create(question=question, answer=response)

    # Получаем все вопросы и ответы для отображения
    history = QuestionAnswer.objects.order_by('-created_at')  # Последние сверху
    return render(request, 'faq/index.html', {'history': history})