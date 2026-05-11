from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from decimal import Decimal
from .models import ChamaGroup, Membership, Contribution
from .forms import ChamaGroupForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('dashboard')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form':form})

def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def dashboard(request):
    groups = ChamaGroup.objects.filter(members=request.user)
    return render(request, 'dashboard.html', {'groups': groups})

@login_required
def create_group(request):
    if request.method == 'POST':
        form = ChamaGroupForm(request.POST)
        if form.is_valid():
            group = form.save()
            Membership.objects.create(user=request.user, group=group, rotation_order=1)
            messages.success(request, "Chama created successfully!")
            return redirect('group_detail', pk=group.pk)
    else:
        form = ChamaGroupForm()
    return render(request, 'create_group.html', {'form': form})

@login_required
def group_detail(request, pk):
    group = get_object_or_404(ChamaGroup, pk=pk)
    membership = Membership.objects.filter(group=group).order_by('rotation_order')
    members = [m.user for m in membership]

    total_members = membership.count()
    next_recipient_index = (group.current_cycle - 1) % total_members
    next_recipient = members[next_recipient_index] if members else None

    contributions = Contribution.objects.filter(group=group, cycle=group.current_cycle).order_by('-paid_at')

    return render(request, 'group_detail.html', {
        'group': group,
        'members': members,
        'next_recipient': next_recipient,
        'contributions': contributions,
        'total_members': total_members,
    })
