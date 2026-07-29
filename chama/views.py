from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.http import HttpResponse
from decimal import Decimal
import csv
import io
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
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
                return redirect('group_detail', pk=group.pk)
            else:
                last_order = Membership.objects.filter(group=group).count() + 1
                Membership.objects.create(user=request.user, group=group, rotation_order=last_order)
                messages.success(request, f"Successfully joined {group.name}")
                return redirect('group_detail', pk=group.pk)
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

    expected_payout = 0
    if total_members > 0:
        expected_payout = (group.contribution_amount - (group.contribution_amount * group.savings_rate / Decimal('100'))) * Decimal(total_members)

    contributions = Contribution.objects.filter(group=group, cycle=group.current_cycle).order_by('-paid_at')
    collected_payout = sum(c.payout_amount for c in contributions) or Decimal('0')

    return render(request, 'group_detail.html', {
        'group': group,
        'members': members,
        'next_recipient': next_recipient,
        'contributions': contributions,
        'total_members': total_members,
        'expected_payout': expected_payout,
        'collected_payout': collected_payout,
    })

@login_required
def record_contribution(request, group_id):
    group = get_object_or_404(ChamaGroup, pk=group_id)
    if request.user != group.creator:
        messages.error(request, "Only the group creator can update contribution records.")
        return redirect('group_detail', pk=group.pk)

    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        try:
            from django.contrib.auth.models import User
            member_user = group.members.get(id=member_id)
        except Exception:
            messages.error(request, "Invalid member selected.")
            return redirect('group_detail', pk=group.pk)

        if Contribution.objects.filter(group=group, member=member_user, cycle=group.current_cycle).exists():
            messages.error(request, f"{member_user.username} has already contributed in cycle {group.current_cycle}.")
            return redirect('group_detail', pk=group.pk)

        amount = Decimal(request.POST['amount'])
        savings_amount = amount * (group.savings_rate / Decimal('100'))
        payout_amount = amount - savings_amount

        Contribution.objects.create(
            group=group,
            member=member_user,
            cycle=group.current_cycle,
            total_paid=amount,
            savings_amount=savings_amount,
            payout_amount=payout_amount
        )

        group.savings_pot += savings_amount
        group.save()

        contributed_count = Contribution.objects.filter(group=group, cycle=group.current_cycle).count()
        if contributed_count >= group.members.count():
            messages.success(request, f"Cycle {group.current_cycle} complete! Payouts & savings ready.")
        else:
            messages.success(request, f"Contribution recorded for {member_user.username}! Savings deducted: KSh {savings_amount}")
        return redirect('group_detail', pk=group.pk)
    
    return render(request, 'record_contribution.html', {'group': group})

@login_required
def distributive_savings(request, group_id):
    group = get_object_or_404(ChamaGroup, pk=group_id)
    if request.user != group.creator:
        messages.error(request, "Only the group admin can distribute savings.")
        return redirect('group_detail', pk=group.pk)
    if request.method == 'POST':
        if group.savings_pot > 0:
            members_count = group.members.count()
            share = group.savings_pot / Decimal(members_count)
            messages.success(request, f"Savings pot of KSh {group.savings_pot} distributed equally! Each member gets KSh {share:.2f}")
            group.savings_pot = 0
            group.save()
        return redirect('group_detail', pk=group.pk)
    return redirect('group_detail', pk=group.pk)

@login_required
def update_savings_rate(request, group_id):
    group = get_object_or_404(ChamaGroup, pk=group_id)
    if request.method == 'POST' and request.user == group.creator:
        new_rate = request.POST.get('savings_rate')
        if new_rate is not None:
            group.savings_rate = Decimal(new_rate)
            group.save()
            messages.success(request, f"Savings rate updated to {new_rate}%.")
    return redirect('group_detail', pk=group.pk)

@login_required
def payout_recipient(request, group_id):
    group = get_object_or_404(ChamaGroup, pk=group_id)
    if request.user != group.creator:
        messages.error(request, "Only the group admin can issue payouts.")
        return redirect('group_detail', pk=group.pk)
    if request.method == 'POST':
        # Find the next recipient
        membership = Membership.objects.filter(group=group).order_by('rotation_order')
        members = [m.user for m in membership]
        total_members = membership.count()
        next_recipient_index = (group.current_cycle - 1) % total_members
        next_recipient = members[next_recipient_index] if members else None
        
        # We don't touch group.savings_pot, we just move to next cycle
        group.current_cycle += 1
        group.save()
        messages.success(request, f"Payout given to {next_recipient.username if next_recipient else 'recipient'}! Cycle advanced.")
        return redirect('group_detail', pk=group.pk)
    return redirect('group_detail', pk=group.pk)

@login_required
def download_transactions(request, group_id):
    group = get_object_or_404(ChamaGroup, pk=group_id)

    # Only members of the group can download
    if not group.members.filter(pk=request.user.pk).exists():
        messages.error(request, "You are not a member of this group.")
        return redirect('dashboard')

    contributions = Contribution.objects.filter(group=group).order_by('cycle', 'paid_at')

    # ── Build workbook ──────────────────────────────────────────────
    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Transactions"

    # Colour palette
    GREEN  = "1B5E20"
    LGREEN = "E8F5E9"
    AMBER  = "FF8F00"
    GREY   = "F5F5F5"

    # ── Group info header block ──────────────────────────────────────
    ws.merge_cells('A1:F1')
    title_cell = ws['A1']
    title_cell.value = f"{group.name} — Transaction Report"
    title_cell.font = Font(bold=True, size=14, color="FFFFFF")
    title_cell.fill = PatternFill("solid", fgColor=GREEN)
    title_cell.alignment = Alignment(horizontal="center", vertical="center")
    ws.row_dimensions[1].height = 30

    ws['A2'] = f"Frequency: {group.frequency.capitalize()}   |   Contribution: KSh {group.contribution_amount}   |   Savings rate: {group.savings_rate}%   |   Current cycle: {group.current_cycle}"
    ws.merge_cells('A2:F2')
    ws['A2'].font = Font(italic=True, size=10, color="555555")
    ws['A2'].alignment = Alignment(horizontal="center")
    ws.row_dimensions[2].height = 18

    ws.append([])   # blank spacer row 3

    # ── Column headers (row 4) ───────────────────────────────────────
    headers = ['Cycle', 'Member', 'Amount Paid (KSh)', 'Savings (KSh)', 'To Recipient (KSh)', 'Date & Time']
    ws.append(headers)
    header_row = ws.max_row
    for col_num, _ in enumerate(headers, start=1):
        cell = ws.cell(row=header_row, column=col_num)
        cell.font = Font(bold=True, color="FFFFFF")
        cell.fill = PatternFill("solid", fgColor=GREEN)
        cell.alignment = Alignment(horizontal="center")

    # ── Data rows ────────────────────────────────────────────────────
    total_paid = total_savings = total_payout = Decimal('0')
    for i, c in enumerate(contributions):
        row_bg = LGREEN if i % 2 == 0 else "FFFFFF"
        row_data = [
            c.cycle,
            c.member.username,
            float(c.total_paid),
            float(c.savings_amount),
            float(c.payout_amount),
            c.paid_at.strftime('%Y-%m-%d %H:%M'),
        ]
        ws.append(row_data)
        r = ws.max_row
        for col_num in range(1, 7):
            cell = ws.cell(row=r, column=col_num)
            cell.fill = PatternFill("solid", fgColor=row_bg)
            cell.alignment = Alignment(horizontal="center" if col_num != 2 else "left")
            if col_num in (3, 4, 5):
                cell.number_format = '#,##0.00'
        total_paid    += c.total_paid
        total_savings += c.savings_amount
        total_payout  += c.payout_amount

    # ── Totals row ───────────────────────────────────────────────────
    ws.append([])
    totals_row = ws.max_row + 1
    ws.cell(row=totals_row, column=1, value="TOTALS")
    ws.cell(row=totals_row, column=3, value=float(total_paid))
    ws.cell(row=totals_row, column=4, value=float(total_savings))
    ws.cell(row=totals_row, column=5, value=float(total_payout))
    for col_num in range(1, 7):
        cell = ws.cell(row=totals_row, column=col_num)
        cell.font = Font(bold=True)
        cell.fill = PatternFill("solid", fgColor=LGREEN)
        cell.alignment = Alignment(horizontal="center")
        if col_num in (3, 4, 5):
            cell.number_format = '#,##0.00'

    # ── Auto column widths ───────────────────────────────────────────
    col_widths = [10, 20, 22, 18, 22, 20]
    for i, width in enumerate(col_widths, start=1):
        ws.column_dimensions[get_column_letter(i)].width = width

    # ── Stream response ──────────────────────────────────────────────
    buffer = io.BytesIO()
    wb.save(buffer)
    buffer.seek(0)

    filename = f"{group.name.replace(' ', '_')}_transactions.xlsx"
    response = HttpResponse(
        buffer.read(),
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    return response
