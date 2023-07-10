from online.models import Choice, Poll, Vote
from online.forms import AddChoiceForm, AddPollForm, EditPollForm, LoginForm, RegisterForm, UserProfileForm
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Count
from django.contrib import messages
from django.http import HttpResponse

# Create your views here.

def index(request):
    polls = Poll.objects.all()
    return render(request,'index.html', {'polls':polls})

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'registration/registration_form.html', { 'form': form}) 
    if request.method == 'POST':
        form = RegisterForm(request.POST) 
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            messages.success(request, 'You have singed up successfully.')
            login(request, user)
            return redirect('login')
        else:
            return render(request, 'registration/registration_form.html', {'form': form})
        
def sign_in(request):

    if request.method == 'GET':
        if request.user.is_authenticated:
            return redirect('index')
        
        form = LoginForm()
        return render(request,'registration/login.html', {'form': form})
    
    elif request.method == 'POST':
        form = LoginForm(request.POST)
        
        if form.is_valid():
            username = form.cleaned_data['username']
            password=form.cleaned_data['password']
            user = authenticate(request,username=username,password=password)
            if user:
                login(request, user)
                messages.success(request,f'Hi {username.title()}, welcome back!')
                return redirect('index')
        
        # either form not valid or user is not authenticated
        messages.error(request,f'Invalid username or password')
        return render(request,'registration/login.html',{'form': form})


def sign_out(request):
    logout(request)
    messages.success(request,f'You have been logged out.')
    return redirect('login') 

@login_required(login_url='/accounts/login/')    
def user_profile(request):
    if request.method == 'POST':
        profile_form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if  profile_form.is_valid():
            profile_form.save()
            return redirect('home')
    else:
        profile_form = UserProfileForm(instance=request.user)
    return render(request, 'profile.html',{ "profile_form": profile_form})

@login_required(login_url='/accounts/login/')
def polls_list(request):
    all_polls = Poll.objects.all()
    search_term = ''
    if 'name' in request.GET:
        all_polls = all_polls.order_by('description')

    if 'date' in request.GET:
        all_polls = all_polls.order_by('pub_date')

    if 'vote' in request.GET:
        all_polls = all_polls.annotate(Count('vote')).order_by('vote__count')

    if 'search' in request.GET:
        search_term = request.GET['search']
        all_polls = all_polls.filter(text__icontains=search_term)

    paginator = Paginator(all_polls, 6)
    page = request.GET.get('page')
    polls = paginator.get_page(page)
    get_dict_copy = request.GET.copy()
    context = {
        'polls': polls,
        'search_term': search_term,
    }
    return render(request, 'poll_list.html', context)

@login_required()
def polls_add(request):
        if request.method == 'POST':
            form = AddPollForm(request.POST)
            if form.is_valid:
                poll = form.save(commit=False)
                poll.owner = request.user
                poll.save()
                messages.success(
                    request, "Poll & Choices added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
                return redirect('list')
        else:
            form = AddPollForm()
        context = {
            'form': form,
        }
        return render(request, 'add_poll.html', context)

@login_required
def polls_edit(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('index')

    if request.method == 'POST':
        form = EditPollForm(request.POST, instance=poll)
        if form.is_valid:
            form.save()
            messages.success(request, "Poll Updated successfully.",
                             extra_tags='alert alert-success alert-dismissible fade show')
            return redirect("list")
    else:
        form = EditPollForm(instance=poll)
    return render(request, "edit_poll.html", {'form': form, 'poll': poll})

@login_required
def polls_delete(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('index')
    poll.delete()
    messages.success(request, "Poll Deleted successfully.",extra_tags='alert alert-success alert-dismissible fade show')
    return redirect("list")

@login_required
def add_choice(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('index')
    if request.method == 'POST':
        form = AddChoiceForm(request.POST)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(request, "Choice added successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('edit', poll_id)
    else:
        form = AddChoiceForm()
    context = {
        'form': form,
    }
    return render(request, 'add_choice.html', context)

@login_required
def choice_edit(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('index')

    if request.method == 'POST':
        form = AddChoiceForm(request.POST, instance=choice)
        if form.is_valid:
            new_choice = form.save(commit=False)
            new_choice.poll = poll
            new_choice.save()
            messages.success(
                request, "Choice Updated successfully.", extra_tags='alert alert-success alert-dismissible fade show')
            return redirect('edit', poll.id)
    else:
        form = AddChoiceForm(instance=choice)
    context = {
        'form': form,
        'edit_choice': True,
        'choice': choice,
    }
    return render(request, 'add_choice.html', context)

@login_required
def choice_delete(request, choice_id):
    choice = get_object_or_404(Choice, pk=choice_id)
    poll = get_object_or_404(Poll, pk=choice.poll.id)
    if request.user != poll.owner:
        return redirect('index')
    choice.delete()
    messages.success(request, "Choice Deleted successfully.", extra_tags='alert alert-success alert-dismissible fade show')
    return redirect('edit', poll.id)

@login_required
def poll_vote(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    choice_id = request.POST.get('choice')
    if not poll.user_can_vote(request.user):
        messages.error(request, "You already voted this poll!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("list")

    if choice_id:
        choice = Choice.objects.get(id=choice_id)
        vote = Vote(user=request.user, poll=poll, choice=choice)
        vote.save()
        print(vote)
        return render(request, 'poll_results.html', {'poll': poll})
    else:
        messages.error(
            request, "No choice selected!", extra_tags='alert alert-warning alert-dismissible fade show')
        return redirect("detail", poll_id)

def poll_detail(request, poll_id):
    poll = get_object_or_404(Poll, id=poll_id)
    if not poll.active:
        return render(request, 'poll_results.html', {'poll': poll})
    loop_count = poll.choice_set.count()
    context = {
        'poll': poll,
        'loop_time': range(0, loop_count),
    }
    return render(request, 'poll_detail.html', context)

@login_required
def endpoll(request, poll_id):
    poll = get_object_or_404(Poll, pk=poll_id)
    if request.user != poll.owner:
        return redirect('index')
    if poll.active is True:
        poll.active = False
        poll.save()
        return render(request, 'poll_results.html', {'poll': poll})
    else:
        return render(request, 'poll_results.html', {'poll': poll})

@login_required()
def list_by_user(request):
    all_polls = Poll.objects.filter(owner=request.user)
    paginator = Paginator(all_polls, 7)  
    page = request.GET.get('page')
    polls = paginator.get_page(page)

    context = {
        'polls': polls,
    }
    return render(request, 'poll_list.html', context)
