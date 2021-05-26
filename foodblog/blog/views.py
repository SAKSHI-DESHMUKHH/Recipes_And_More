from django.shortcuts import render, redirect
from .models import Category, Food
from .forms import FoodForm,CreateUserForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .decorators import unauthenticated_user, allowed_users, admin_only
from django.contrib.auth.models import Group
# Create your views here.
@unauthenticated_user
def registerPage(request):

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            group = Group.objects.get(name="customer")
            user.groups.add(group)
            messages.success(request, 'Account was created successfully for ' + username)
            return redirect('login_page')
                # print(request.POST)
    context = {'form':form}
    return render(request,'blog/register.html',context)

@unauthenticated_user
def loginPage(request):
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'Username or password is incorrect')
                # return render(request,'blog/login.html')
    context={}
    return render(request,'blog/login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login_page')

def userPage(request):
    context={}
    return render(request,'blog/user.html',context)

@login_required(login_url='login_page')
@admin_only
def home(request):
    category = request.GET.get('category')
    if category == None:
        foods = Food.objects.all()
    else:
        foods = Food.objects.filter(category__name__contains=category)

    categories = Category.objects.all()
    # foods = Food.objects.all()
    data = {
        'categories':categories,
        'foods':foods,
    }
    return render(request, 'blog/home.html', data)

@login_required(login_url='login_page')
def viewFood(request,pk):
    food = Food.objects.get(id=pk)

    return render(request, 'blog/food.html', {'food':food})

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def addFood(request):
    categories = Category.objects.all()
    if request.method == 'POST':
        data = request.POST
        image = request.FILES.get('image')

        if data['category'] != 'none':
            category = Category.objects.get(id=data['category'])
        elif data['category_new'] != '':
            category, created = Category.objects.get_or_create(name=data['category_new'])
        else:
            category = None

        food = Food.objects.create(
            category=category,
            description=data['description'],
            image=image,
            short_description=data['short_description'],
            title=data['title'],
            ingredients=data['ingredients'],
        )
        return redirect('home')
    context = {
        'categories':categories,
    }
    return render(request, 'blog/add.html',context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def updateRecipes(request,pk):
    food = Food.objects.get(id=pk)
    form = FoodForm(instance=food)
    if request.method == "POST":
        # print(request.POST)
        form = FoodForm(request.POST,instance=food)
        if form.is_valid():
            form.save()
        return redirect('/')        
    context={'form':form}
    return render(request, 'blog/recipes_form.html',context)

@login_required(login_url='login_page')
@allowed_users(allowed_roles=['admin'])
def deleteRecipes(request,pk):
    food = Food.objects.get(id=pk)
    if request.method == "POST":
        food.delete()
        return redirect('/') 
    context={'item':food}
    return render(request, 'blog/delete.html',context)