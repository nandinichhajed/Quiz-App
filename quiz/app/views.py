from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.paginator import Paginator
from django.http import HttpResponseNotFound
import pytz
from faunadb import query as q
from faunadb.objects import Ref
from faunadb.client import FaunaClient
from collections import Iterable
import hashlib
from datetime import datetime

client = FaunaClient(secret="fnAEZq7eVjAAQrXBuPTntiGCiAKAoIkueJe7Uql_")
indexes = client.query(q.paginate(q.indexes()))
print(indexes)
# # Create your views here.

def login(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        password = request.POST.get("password")

        try:
            user = client.query(q.get(q.match(q.index("users_index"), username)))
            if hashlib.sha512(password.encode()).hexdigest() == user["data"]["password"]:
                request.session["user"] = {
                    "id": user["ref"].id(),
                    "username": user["data"]["username"]
                }
                return redirect("app:dashboard")
            else:
                raise Exception()
        except:
            messages.add_message(request, messages.INFO,"You have supplied invalid login credentials, please try again!", "danger")
            return redirect("app:login")
    return render(request,"login.html")

def dashboard(request):
    if "user" in request.session:
        user=request.session["user"]["username"]
        context={"user":user}
        return render(request,"dashboard.html",context)
    else:
        return HttpResponseNotFound("Page not found")


def register(request):
    if request.method == "POST":
        username = request.POST.get("username").strip().lower()
        email = request.POST.get("email").strip().lower()
        password = request.POST.get("password")

        try:
            user = client.query(q.get(q.match(q.index("users_index"), username)))
            messages.add_message(request, messages.INFO, 'User already exists with that username.')
            return redirect("app:register")
        except:
            user = client.query(q.create(q.collection("Users"), {
                "data": {
                    "username": username,
                    "email": email,
                    "password": hashlib.sha512(password.encode()).hexdigest(),
                    "date": datetime.datetime.now(pytz.UTC)
                }
            }))
            messages.add_message(request, messages.INFO, 'Registration successful.')
            return redirect("app:login")
    return render(request,"register.html")

def create_quiz(request):
    if request.method=="POST":
        name=request.POST.get("quiz_name")
        description=request.POST.get("quiz_description")
        total_questions=request.POST.get("total_questions")
        try:
            quiz = client.query(q.get(q.match(q.index("quiz_index"), name)))
            messages.add_message(request, messages.INFO, 'A Quiz with that name already exists.')
            return redirect("app:create-quiz")
        except:
            quiz = client.query(q.create(q.collection("Quiz"), {
                "data": {
                    "status":"active",
                    "name": name,
                    "description": description,
                    "total_questions": total_questions,
                }
            }))
            messages.add_message(request, messages.INFO, 'Quiz Created Successfully.')
            return redirect("app:create-quiz")
    return render(request,"create_quiz.html")


def quiz(request):
    try:
        all_quiz=client.query(q.paginate(q.match(q.index("quiz_get_index"), "active")))["data"]
        quiz_count=len(all_quiz)
        page_number = int(request.GET.get('page', 1))
        quiz = client.query(q.get(q.ref(q.collection("Quiz"), all_quiz[page_number-1].id())))["data"]
        context={"count":quiz_count,"quiz":quiz, "next_page": min(quiz_count, page_number + 1), "prev_page": max(1, page_number - 1)}
        return render(request,"quiz.html",context)
    except:
        return render(request,"quiz.html")

def answer_quiz(request,slug):
    question_all=client.query(q.paginate(q.match(q.index("question_get_index"), slug)))["data"]
    question_count=len(question_all)
    page_number = int(request.GET.get('page', 1))
    question = client.query(q.get(q.ref(q.collection("Question"), question_all[page_number-1].id())))["data"]
    if page_number==question_count:
        context={"question":question,"next_page": min(question_count, page_number + 1), "prev_page": max(1, page_number - 1),"finish":"true"}
    else:
        context={"question":question,"next_page": min(question_count, page_number + 1), "prev_page": max(1, page_number - 1)}
    if request.method=="POST":
        answer=request.POST.get("answer")
        question=request.POST.get("question")
        try:
            check_answer=client.query(q.get(q.match(q.index("answer_get_index"), request.session["user"]["username"],question)))["data"]
            messages.add_message(request, messages.INFO, 'You already answered this question')
        except Exception:
            answer_create = client.query(q.create(q.collection("Answers"), {
                "data": {
                    "user": request.session["user"]["username"],
                    "quiz": slug,
                    "question": question,
                    "answer": answer,
                }
            }))
            messages.add_message(request, messages.INFO, 'Answer Saved')
    if request.GET.get("finish")=="true":
        score=0
        check_answer=client.query(q.paginate(q.match(q.index("answer_score_index"), request.session["user"]["username"],slug)))
        all_answer=[]
        for i in check_answer["data"]:
            all_answer.append(q.get(q.ref(q.collection("Answers"),i.id())))
        answers=client.query(all_answer)
        for i in answers:
            try:
                mark_answer=client.query(q.get(q.match(q.index("question_answer"),i["data"]["answer"])))
                score=score+1
            except:
                score=score
        context={"score":score,"question_count":question_count}
    return render(request,"answer_quiz.html",context)

def create_question(request):
    quiz_all=client.query(q.paginate(q.match(q.index("quiz_get_index"), "active")))
    all_quiz=[]
    for i in quiz_all["data"]:
        all_quiz.append(q.get(q.ref(q.collection("Quiz"),i.id())))
    context = {"quiz_all":client.query(all_quiz)}
    if request.method=="POST":
        quiz_name=request.POST.get("quiz_name")
        question_asked=request.POST.get("question")
        answer_1=request.POST.get("answer_1")
        answer_2=request.POST.get("answer_2")
        answer_3=request.POST.get("answer_3")
        answer_4=request.POST.get("answer_4")
        correct_answer=request.POST.get("correct_answer")
        try:
            question_create = client.query(q.get(q.match(q.index("question_index"), question_asked)))
            messages.add_message(request, messages.INFO, 'This question already exists')
            return redirect("app:create-question")
        except:
            question_create = client.query(q.create(q.collection("Question"), {
                "data": {
                    "quiz_name": quiz_name,
                    "question_asked": question_asked,
                    "answer_1": answer_1,
                    "answer_2": answer_2,
                    "answer_3": answer_3,
                    "answer_4": answer_4,
                    "correct_answer": correct_answer,
                }
            }))
            messages.add_message(request, messages.INFO, 'Question Created Successfully.')
            return redirect("app:create-question")
    return render(request,"create-questions.html",context)