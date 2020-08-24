from django.shortcuts import render, redirect
from django.contrib import messages
from .models import *
import bcrypt

def index(request):
    return render(request, 'gloves/index.html')

def drills(request):
    return render(request, 'gloves/drills.html')

def media(request):
    return render(request, 'gloves/media.html')

def profile(request):
    return render(request, 'gloves/profile.html')

def warm_up(request):
    return render(request, 'gloves/warm_up.html')

def forum(request):
    if 'user' not in request.session:
        return redirect('/')
    context = {
        'wall_messages': Wall_Message.objects.all()
    }
    return render(request, 'gloves/forum.html', context)

def intro(request):
    if "user_id" not in request.session:
        return redirect('/')
    else:
        return render(request, 'gloves/intro.html')

def register(request):
    errors = User.objects.register_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.create(
            first_name = request.POST['first_name'],
            last_name = request.POST['last_name'],
            email = request.POST['email'],
            password = bcrypt.hashpw(request.POST['password'].encode(), bcrypt.gensalt()).decode()
        )
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/intro')

def login(request):
    errors = User.objects.login_validator(request.POST)

    if len(errors):
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        request.session['greeting'] = user.first_name
        return redirect('/intro')

def logout(request):
    request.session.flush()
    return redirect('/')

def post_mess(request):
    Wall_Message.objects.create(message=request.POST['mess'], poster=User.objects.get(id=request.session['id']))
    return redirect('/forum')

def post_comment(request, id):
    poster = User.objects.get(id=request.session['id'])
    message = Wall_Message.objects.get(id=id)
    Comment.objects.create(comment=request.POST['comment'], poster=poster, wall_message=message)
    return redirect('/forum')

def profile(request, id):
    context = {
        'user': User.objects.get(id=id)
    }
    return render(request, 'profile.html', context)

def add_like(request, id):
    liked_message = Wall_Message.objects.get(id=id)
    user_liking = User.objects.get(id=request.session['id'])
    liked_message.user_likes.add(user_liking)
    return redirect('/forum')

def delete_comment(request, id):
    destroyed = Comment.objects.get(id=id)
    destroyed.delete()
    return redirect('/forum')

def edit(request, id):
    edit_user = User.objects.get(id=id)
    edit_user.first_name = request.POST['first_name']
    edit_user.last_name = request.POST['last_name']
    edit_user.email = request.POST['email']
    edit_user.save()
    return redirect('/intro')
