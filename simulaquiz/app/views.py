from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Theme, Exam, Moderator, Question, Choices
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Q

def home(request):
    return render(request, 'app/home.html')

def login(request):
    if request.method == 'POST':
        username_email = request.POST.get('username-email')  
        password = request.POST.get('password')

        if username_email and password:
            user = authenticate(request, username=username_email, password=password)
            
            if user is None:
                try:
                    user = User.objects.get(email=username_email)
                    if user.check_password(password):
                        user = authenticate(request, username=user.username, password=password)
                    else:
                        user = None
                except User.DoesNotExist:
                    user = None

            if user is not None:
                auth_login(request, user)
                messages.success(request, 'Login successful!')
                return redirect(reverse('home'))
            else:
                messages.error(request, 'Invalid username/email or password.')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'app/login.html')

def logout_user(request):
    logout(request)
    return redirect(reverse('home'))

def sign_up(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm-password')

        if username and email and password and confirm_password:
            if password == confirm_password:
                if User.objects.filter(username=username).exists():
                    messages.error(request, 'Username already exists.')
                elif User.objects.filter(email=email).exists():
                    messages.error(request, 'Email is already registered.')
                else:
                    user = User.objects.create_user(username=username, email=email, password=password)
                    user.save()
                    Moderator.objects.create(
                        user = user
                    )
                    messages.success(request, 'Registration successful!')
                    return redirect(reverse('home'))
            else:
                messages.error(request, 'Passwords do not match.')
        else:
            messages.error(request, 'All fields are required.')

    return render(request, 'app/sign-up.html')

def exams(request):
    query = request.GET.get('q')  
    if query:
        exams = Exam.objects.filter(
            Q(title__icontains=query) | Q(theme__title__icontains=query)
        ).order_by('-date_created')
    else:
        exams = Exam.objects.all().order_by('-date_created')

    context = {'exams': exams}
    return render(request, 'app/exams.html', context)

def exam(request, id):
    exam = Exam.objects.get(id=id)

    if exam:
        context = {'exam': exam}

    return render(request, 'app/exam.html', context)

def feedback(request, id):
    exam = Exam.objects.get(id=id)

    exam.how_many_submissions += 1
    exam.save()

    questions = exam.question_set.all()
    
    choices_submitted = {f'question{i+1}': request.POST.get(f'question{i+1}') for i in range(len(questions))}
    
    question_status = {}
    score = 0
    score_sum = 0

    for question in questions:
        correct_choice = question.choices_set.filter(is_correct=True).first()
        submitted_answer = choices_submitted.get(f'question{question.id}')
        
        if correct_choice and submitted_answer == correct_choice.text:
            question_status[question.id] = 'correct'
            score += question.weight
        else:
            question_status[question.id] = 'incorrect'
        
        score_sum += question.weight
    
    context = {
        'exam': exam,
        'question_status': question_status,
        'choices_submitted': choices_submitted,
        'score': int((score / score_sum) * 100),
        'score_sum': score_sum,
    }
    
    return render(request, 'app/feedback.html', context)


@login_required
def my_exams(request):
    user = request.user

    exams = Exam.objects.filter(moderator=user.moderator).order_by('-last_change')

    context = {
        'exams': exams,
    }

    return render(request, 'app/my-exams.html', context)

@login_required
def my_exam(request, id):
    exam = get_object_or_404(Exam, id=id)

    context = {
        'exam': exam,
    }

    return render(request, 'app/my-exam.html', context)

@login_required
def create_exam(request):
    if request.method == 'POST':
        theme_title = request.POST.get('theme')
        choices_title = request.POST.get('title')

        if theme_title and choices_title:
            theme, created = Theme.objects.get_or_create(title=theme_title)
            moderator = get_object_or_404(Moderator, user=request.user)

            exam = Exam.objects.create(
                theme=theme,
                moderator=moderator,
                title=choices_title
            )

            return redirect(reverse('my-exams'))

    return render(request, 'app/create-exam.html')

@login_required
def create_question(request, id):
    exam = get_object_or_404(Exam, id=id)

    if request.method == 'POST':
        question_text = request.POST.get('question-text')
        question_weight = request.POST.get('weight')
                
        if question_text and question_weight:
            Question.objects.create(
                exam = exam,
                text = question_text,
                weight = question_weight
            )
            return redirect(reverse('my-exam', args=[exam.id]))

    context = {
        'exam': exam,
    }
    return render(request, 'app/create-question.html', context)

@login_required
def create_choice(request, id):
    question = get_object_or_404(Question, id=id)

    if request.method == 'POST':
        choice_text = request.POST.get('choice-text')
        correct = request.POST.get('correct')
                
        if choice_text:
            if correct == None:
                correct = 0
            else:
                correct = 1
            
            Choices.objects.create(
                question = question,
                text = choice_text,
                is_correct = correct
            )
            return redirect(reverse('my-exam', args=[question.exam.id]))

    context = {
        'question': question,
    }
    return render(request, 'app/create-choice.html', context)

@login_required
def edit_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    themes = Theme.objects.all()

    if request.method == 'POST':
        theme_id = request.POST.get('theme')

        if theme_id == None:
            theme_id = exam.theme.id

        title = request.POST.get('title')

        theme = get_object_or_404(Theme, id=theme_id)
        exam.theme = theme
        exam.title = title
        exam.save()
        
        return redirect(reverse('my-exam', args=[exam.id]))
    
    context = {
        'exam': exam,
        'themes': themes,
    }

    return render(request, 'app/edit-exam.html', context)

@login_required
def edit_question(request, id):
    question = get_object_or_404(Question, id=id)

    if request.method == 'POST':
        question_text = request.POST.get('question-text')
        question_weight = request.POST.get('weight')
        
        question.text = question_text
        question.weight = question_weight
        question.save()

        return redirect(reverse('my-exam', args=[question.exam.id]))
    
    context = {
        'question': question,
    }

    return render(request, 'app/edit-question.html', context)

@login_required
def edit_choice(request, id):
    choice = get_object_or_404(Choices, id=id)

    if request.method == 'POST':
        choice_text = request.POST.get('choice-text')
        correct = request.POST.get('correct')

        if correct == None:
            correct = False
        else:
            correct = True

        choice.text = choice_text
        choice.is_correct = correct

        choice.save()

        return redirect(reverse('my-exam', args=[choice.question.exam.id]))
    
    context = {
        "choice": choice,
    }

    return render(request, 'app/edit-choice.html', context)

@login_required
def delete_exam(request, id):
    exam = get_object_or_404(Exam, id=id)
    exam.delete()
    return redirect(reverse('my-exams'))

@login_required
def delete_question(request, id):
    question = get_object_or_404(Question, id=id)
    question.delete()
    return redirect(reverse('my-exams'))

@login_required
def delete_choice(request, id):
    choice = get_object_or_404(Choices, id=id)
    choice.delete()
    return redirect(reverse('my-exams'))