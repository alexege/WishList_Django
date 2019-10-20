# messages.error(request, "This is a custom error message")

from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, "wish_app/index.html")

def register(request):

    #Check if username already exists in database
    if(User.objects.filter(email=request.POST['email'])):
        print("User already exists in db")
        messages.add_message(request, messages.INFO, 'User already exists in db')
        return redirect('/')

    errors = User.objects.registration_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        print("Plaintext_password", request.POST['password'])
        hashed_password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt())
        print("hashed_password", hashed_password)

        #Store user object we just created in variable called "current_user"
        current_user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], password=hashed_password)
        
        #Store current user's id in session as a key called "current_user_id"
        request.session['current_user_id'] = current_user.id

    return redirect('/dashboard')

def login(request):

    errors = User.objects.login_validator(request.POST)
        # check if the errors dictionary has anything in it
    if len(errors) > 0:
        # if the errors dictionary contains anything, loop through each key-value pair and make a flash message
        for key, value in errors.items():
            messages.error(request, value)
        # redirect the user back to the form to fix the errors
        return redirect('/')
    else:
        print("email",request.POST['email'])
        print(request.POST['password'])

        if User.objects.filter(email=request.POST['email']):
            #Get User object
            current_user = User.objects.get(email=request.POST['email'])
            #Get user objects' password
            user_password = current_user.password #User's password (hashed)
            #Get the plaintext password from the login page
            entered_password = request.POST['password'] #User's entered password from login (plaintext)
            print("user's hashed password", user_password)
        is_match = bcrypt.checkpw(entered_password.encode(), user_password.encode())

        if(is_match == True):
            request.session['current_user_id'] = current_user.id
            return redirect('/dashboard')
        else:
            return redirect('/')

    return redirect('/dashboard')

def dashboard(request):
    current_user_object = User.objects.get(id=request.session['current_user_id'])

    context = {
        'current_user' : current_user_object,
        'my_list_of_wishes' : Wish.objects.filter(created_by=current_user_object).exclude(granted=True),
        'all_granted_wishes' : Wish.objects.filter(granted=True).order_by('created_at')
    }
    return render(request, "wish_app/dashboard.html", context)

def new_wish(request):
    return render(request, "wish_app/new_wish.html")

def create_wish(request):

    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/new')
    else:
        #Query database to find current logged in user's object
        current_user = User.objects.get(id=request.session['current_user_id'])

        #Create a new wish
        Wish.objects.create(name=request.POST['name'], description=request.POST['description'],created_by=current_user)
    return redirect('/dashboard')

def remove_wish(request, wish_id):
    current_wish = Wish.objects.get(id=wish_id)
    current_wish.delete()
    return redirect('/dashboard')

def edit_wish(request, wish_id):
    context = {
        'current_wish_object' : Wish.objects.get(id=wish_id)
    }
    return render(request, 'wish_app/edit_wish.html', context)

def update_wish(request):

    errors = Wish.objects.wish_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/wishes/edit/' + request.POST['id'])
    else:
        #Get the wish id from the hidden input
        current_wish_id = request.POST['id']

        current_wish = Wish.objects.get(id=current_wish_id)

        current_wish.name = request.POST['name']
        current_wish.description = request.POST['description']
        current_wish.save()

    return redirect('/dashboard')

def grant_wish(request, wish_id):
    current_wish = Wish.objects.get(id=wish_id)
    current_wish.granted = True
    current_wish.save()
    return redirect('/dashboard')

def like_wish(request, wish_id):
    current_wish = Wish.objects.get(id=wish_id)
    current_user = User.objects.get(id=request.session['current_user_id'])
    current_wish.users_who_liked.add(current_user)
    return redirect('/dashboard')

def unlike_wish(request, wish_id):
    current_wish = Wish.objects.get(id=wish_id)
    current_user = User.objects.get(id=request.session['current_user_id'])
    current_wish.users_who_liked.remove(current_user)
    return redirect('/dashboard')

def stats(request):

    current_user_object = User.objects.get(id=request.session['current_user_id'])

    context = {
        'current_user' : current_user_object,
        'total_wishes_granted' : Wish.objects.filter(granted=True).count,
        'my_granted_wishes_count' : Wish.objects.filter(created_by=current_user_object).filter(granted=True).count,
        'my_pending_wishes_count' : Wish.objects.filter(created_by=current_user_object).filter(granted=False).count
    }

    return render(request, 'wish_app/stats.html', context)

def logout(request):
    request.session.clear()
    return redirect('/')