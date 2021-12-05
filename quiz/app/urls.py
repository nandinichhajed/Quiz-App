from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from . import views

app_name = "app"

urlpatterns = [
    path("", views.login, name="login"),
    path("login", views.login, name="login"),
    path("dashboard", views.dashboard, name="dashboard"),
    path("quiz", views.quiz, name="quiz"),
    path("register", views.register, name="register"),
    path("create-quiz", views.create_quiz, name="create-quiz"),
    path("create-questions", views.create_question, name="create-question"),
    path("answer-quiz/<slug>", views.answer_quiz, name="answer-quiz"),
]