from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import Question, Choice

def index(request):
    latest_question_list = Question.objects.all()
    context = {'latest_question_list': latest_question_list}
    return render(request, 'poll/index.html', context)

def detail(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/detail.html', {'question': question})

def results(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    return render(request, 'poll/results.html', {'question': question})

def vote(request, question_id):
    question = get_object_or_404(Question, pk=question_id)
    try:
        selected_choice = question.choice_set.get(pk=request.POST['choice'])
    except (KeyError, Choice.DoesNotExist):
        return render(request, 'poll/detail.html', {
            'question': question,
            'error_message': "You didn't select a choice.",
        })
    else:
        selected_choice.votes += 1
        selected_choice.save()
        return HttpResponseRedirect(reverse('poll:results', args=(question.id,)))

def signup(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
     #   confirm_password = request.POST.get('confirm_password')



        # Username exists check
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists")
            return redirect('poll:signup')

        # Email exists check
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email already exists")
            return redirect('poll:signup')

        # Username length check
        if len(username) > 10:
            messages.error(request, "Username is too long")
            return redirect('poll:signup')

        # Password length check
        if len(password) < 3:
            messages.error(request, "Password is too short")
            return redirect('poll:signup')

        # Create the user
        myuser = User.objects.create_user(username=username, email=email, password=password)
        myuser.save()

        messages.success(request, "Your account has been created successfully")
        return redirect('poll:signin')

    return render(request, "poll/signup.html")

def signin(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('poll:index')
        else:
            messages.error(request, "Invalid credentials")
            return redirect('poll:signin')

    return render(request, "poll/signin.html")

def signout(request):
    logout(request)
    messages.success(request, "Logged out successfully")
    return redirect('poll:signin')