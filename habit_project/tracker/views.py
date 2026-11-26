from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Habit, HabitLog
from .forms import HabitForm

@login_required
def habit_list(request):
    habits = Habit.objects.filter(user=request.user)
    today = timezone.now().date()
    
    habits_data = []
    for habit in habits:
        is_done = HabitLog.objects.filter(habit=habit, date=today).exists()
        
        total_count = HabitLog.objects.filter(habit=habit).count()
        
        streak = 0
        current_date = today
        
        if not is_done:
            current_date = today - timedelta(days=1)
            
        while True:
            if HabitLog.objects.filter(habit=habit, date=current_date).exists():
                streak += 1
                current_date -= timedelta(days=1)
            else:
                break
                
        habits_data.append({
            'habit': habit,
            'is_done': is_done,
            'total_count': total_count,
            'streak': streak,
        })
    
    return render(request, 'tracker/habit_list.html', {'habits_data': habits_data})

@login_required
def add_habit(request):
    if request.method == 'POST':
        form = HabitForm(request.POST)
        if form.is_valid():
            habit = form.save(commit=False)
            habit.user = request.user
            habit.save()
            return redirect('habit_list')
    else:
        form = HabitForm()
    return render(request, 'tracker/add_habit.html', {'form': form})

@login_required
def toggle_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    today = timezone.now().date()
    log, created = HabitLog.objects.get_or_create(habit=habit, date=today)
    if not created:
        log.delete()
    return redirect('habit_list')

@login_required
def delete_habit(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    if request.method == 'POST':
        habit.delete()
    return redirect('habit_list')

@login_required
def habit_history(request, pk):
    habit = get_object_or_404(Habit, pk=pk, user=request.user)
    logs = HabitLog.objects.filter(habit=habit).order_by('-date')
    return render(request, 'tracker/habit_history.html', {'habit': habit, 'logs': logs})