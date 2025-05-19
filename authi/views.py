from django.shortcuts import render, HttpResponse, redirect
from .models import todo
from .forms import formm
from . import urls
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
# Create your views here.


@login_required(login_url='login')
def home(request):
    data = todo.objects.filter(usr=request.user).order_by('-id')
    paginator = Paginator(data, 4) # show 5 data in a page

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'home.html', {'dataa': data, 'page_obj': page_obj})

@login_required(login_url='login')
def task(request):
    if request.method == "POST":
      task1 = request.POST.get('task')
      date1 = request.POST.get('date')
      options1 = request.POST.get('options')
      tryy = todo(task=task1, dat=date1, select=options1, usr = request.user)
      tryy.save()
    return render(request, 'task.html')

def delete(request, id):
    dele = todo.objects.get(id=id)
    if dele:
        dele.delete()
        return redirect('home')


def update(request, id):
    dat = todo.objects.get(id=id)
    fo = formm(request.POST or None, instance=dat)
    if fo.is_valid():
        fo.save()
        return redirect('home')
    return render(request, 'update.html', {'form': fo})

def custom_404(request):
    return render(request, '')

def custom_500(request):
    return render(request, '')

def register(request):
    if request.method == 'POST':
        usern = request.POST.get('username')
        passw = request.POST.get('password')
        confirm = request.POST.get('cnf_pass')
        if passw == confirm:
            if User.objects.filter(username=usern).exists():
                print('Username and Password already exist')
                return redirect('register')
            else:
                tryy = User.objects.create_user(username = usern, password=passw)
                if tryy:
                    tryy.save()
                    return redirect('login')
        else:
            messages.info(request, 'Password Not Match')
            return redirect('register')
    return render(request, 'register.html')

def login(request):
    if request.method == "POST":
        userr = request.POST.get('username')
        passw = request.POST.get('password')
        log = authenticate(username=userr, password=passw)
        if log is not None:
            auth_login(request, log)
            return redirect('home')
        else:
            return redirect('login')
    return render(request, 'login.html')

def logout(request):
    auth_logout(request)
    return redirect('login')



# ------------------Method 1--------------------

# def search(request):

#     if 'q' in request.GET:
#         prod = request.GET.get('q')
#         query = todo.objects.all().filter(Q(task__icontains=prod)|Q(dat__icontains=prod), usr=request.user)
#     return render(request, 'search.html', {"qr":query})

# ------------------Method 2--------------------


def search(request):
    query = None
    prod = None
    if 'q' in request.GET:
        prod = request.GET.get('q')
        query = todo.objects.all().filter(Q(task__icontains = prod))


# ------------------Method 3--------------------

def search(request):
    if request.method == 'GET':
        query = None
        prod = request.GET.get('q')
        if prod:
            query = todo.objects.all().filter(Q(task__icontains=prod)|Q(dat__icontains=prod), usr=request.user)
        return render(request, 'search.html', {"qr":query})
