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
def join_group(request):
    if request.method == 'POST':
        code = request.POST.get('join_code').strip().upper()
        try:
            group = ChamaGroup.objects.get(join_code=code)
            if Membership.objects.filter(group=group, user=request.user).exists():
                messages.warning(request, "You are already a member")
            else:
                last_order = Membership.objects.filter(group=group).count() + 1
                Membership.objects.create(user=request.user, group=group, rotation_order=last_order)
                messages.success(request, f"Successfully joined {group.name}")
        except ChamaGroup.DoesNotExist:
            messages.error(request, "Invalid join code")
    return render(request, 'join_group.html')

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

@login_required
def record_contribution(request, group_id):
    group = get_object_or_404(ChamaGroup, pk=group_id)
    if request.method == 'POST':
        amount = Decimal(request.POST['amount'])
        savings_amount = amount * (group.savings_rate / Decimal('100'))
        payout_amount = amount - savings_amount

        Contribution.objects.create(
            group=group,
            member=request.user,
            cycle=group.current_cycle,
            total_paid=amount,
            savings_amount=savings_amount,
            payout_amount=payout_amount
        )

        group.savings_pot += savings_amount
        group.save()

        contributed_count = Contribution.objects.filter(group=group, cycle=group.current_cycle).count()
        if contributed_count >= group.members.count():
            messages.success(request, f"Cycle, {group.current_cycle} complete! Payouts & savings ready.")

        messages.success(request, f"Contribution recorded! Savings deducted: KSh {savings_amount}")
        return redirect('group_detail', pk=group.pk)
    
    return render(request, 'record_contribution.html', {'group': group})

@login_required
def distributive_savings(request, group_id):
    group = get_object_or_404(ChamaGroup, pk=group_id)
    if request.method == 'POST':
        if group.savings_pot > 0:
            members_count = group.members.count()
            share = group.savings_pot / Decimal(members_count)
            messages.success(request, f"Savings pot of KSh {group.savings_pot} distributed equally! Each member gets KSh {share:.2f}")
            group.savings_pot = 0
            group.current_cycle += 1
            group.save()
        return redirect('group_detail', pk=group.pk)
    return redirect('group_detail', pk=group.pk)
