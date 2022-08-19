from django.shortcuts import redirect, render
from django.contrib.auth import login, logout, authenticate
from .forms import *
from .models import *
from django.http import HttpResponse
import random
from django.db.models import Avg, Max, Min


# Create your views here.
def home(request):
    item = QuesModel.objects.all()
    if request.method == 'POST':
        print(request.POST)
        """if request.user.is_staff:
            questions = item
        else:"""
        questions = random.sample(list(item), 5)

        print(questions)

        score = 0
        wrong = 0
        correct = 0
        total = 0
        attempt = 0
        for q in questions:
            total += 1
            print(q.ans)
            print('done')
            print(request.POST.get(q.question))
            if q.ans == request.POST.get(q.question):
                score += 10
                correct += 1
            else:
                wrong += 1
        percent = score / (total * 10) * 100
        Userm = UserModel(user=request.user, rightans=correct, wrongans=wrong, no_of_attempt=attempt + 1)
        Userm.save()
        userrealted = UserModel.objects.filter(user=request.user)
        no_of_attempts = UserModel.objects.filter(user=request.user).count()
        highestscore = userrealted.aggregate(Max('rightans')).get('rightans__max')
        lowestscore = userrealted.aggregate(Min('rightans')).get('rightans__min')
        averagescore = "{:.2f}".format(userrealted.aggregate(Avg('rightans')).get('rightans__avg'))
        context = {
            'score': score,
            'time': request.POST.get('timer'),
            'correct': correct,
            'wrong': wrong,
            'percent': percent,
            'total': total,
            'highestscore': highestscore,
            'lowestscore': lowestscore,
            'averagescore': averagescore,
            'no_of_attempts': no_of_attempts,
            'details': userrealted
        }
        print(context)
        return render(request, 'Quiz/result.html', context)
    else:
        """if request.user.is_staff:
            questions = item
        else:"""
        questions = random.sample(list(item), 5)
        context = {
            'questions': questions
        }
        return render(request, 'Quiz/home.html', context)


def addQuestion(request):
    if request.user.is_staff:
        form = addQuestionform()
        if request.method == 'POST':
            form = addQuestionform(request.POST)
            if form.is_valid():
                form.save()
                return redirect('/')
        context = {'form': form}
        return render(request, 'Quiz/addQuestion.html', context)
    else:
        return redirect('home')


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = createuserform()
        if request.method == 'POST':
            form = createuserform(request.POST)
            if form.is_valid():
                user = form.save()
                return redirect('login')
        context = {
            'form': form,
        }
        return render(request, 'Quiz/register.html', context)


def SummaryPage(request):
    userrealted = UserModel.objects.filter(user=request.user)
    no_of_attempts = UserModel.objects.filter(user=request.user).count()
    highestscore = userrealted.aggregate(Max('rightans')).get('rightans__max')
    lowestscore = userrealted.aggregate(Min('rightans')).get('rightans__min')
    averagescore = "{:.2f}".format(userrealted.aggregate(Avg('rightans')).get('rightans__avg'))
    context = {
            'highestscore': highestscore,
            'lowestscore': lowestscore,
            'averagescore': averagescore,
            'no_of_attempts': no_of_attempts,
            'details': userrealted
        }
    return render(request, 'Quiz/summary.html',context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == "POST":
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('/')
        context = {}
        return render(request, 'Quiz/login.html', context)


def logoutPage(request):
    logout(request)
    return redirect('/')
