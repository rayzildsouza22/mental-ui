from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib import messages
from datetime import datetime
from .models import Activity, Mood, Message
from .forms import ActivityForm
import random


@login_required
def home(request):

    mood_obj = Mood.objects.filter(user=request.user).first()

    if request.method == "POST":
        mood_value = request.POST.get("mood")
        if mood_value:
            if mood_obj:
                mood_obj.mood = mood_value
                mood_obj.save()
            else:
                Mood.objects.create(
                    user=request.user,
                    mood=mood_value
                )
            return redirect('home')

    now = datetime.now().time()

    next_activity = (
        Activity.objects
        .filter(user=request.user, time__gte=now)
        .order_by('time')
        .first()
    )

    mood_obj = Mood.objects.filter(user=request.user).first()

    return render(request, 'app/home.html', {
        'next_activity': next_activity,
        'today_mood': mood_obj
    })

# ================== CHAT ==================

@login_required
def chat(request):
    if request.method == "POST":
        user_text = request.POST.get("message")

        if user_text:
            # Save user message
            Message.objects.create(
                user=request.user,
                text=user_text,
                is_bot=False
            )

            # Simple intelligent reply logic
            reply = generate_reply(user_text)

            Message.objects.create(
                user=request.user,
                text=reply,
                is_bot=True
            )

        return redirect('chat')

    messages_list = Message.objects.filter(user=request.user).order_by('created_at')

    return render(request, 'app/chat.html', {
        'messages': messages_list
    })


def generate_reply(user_text):
    text = user_text.lower()

    # Physical symptoms
    if any(word in text for word in ["headache", "fever", "pain", "stomach", "body ache"]):
        responses = [
            "I'm sorry you're not feeling well. Have you had enough water today?",
            "Headaches can sometimes be caused by stress or dehydration. Try resting for a bit.",
            "Maybe take a short break and relax your eyes. Are you looking at screens for long hours?"
        ]
        return random.choice(responses)

    # Stress / Anxiety
    elif any(word in text for word in ["stress", "stressed", "anxious", "overwhelmed"]):
        responses = [
            "It sounds like things feel heavy right now. What’s causing the stress?",
            "Take 3 slow deep breaths with me. Inhale… hold… exhale.",
            "You don’t have to handle everything at once. What’s the main pressure?"
        ]
        return random.choice(responses)

    # Sadness
    elif any(word in text for word in ["sad", "upset", "cry", "lonely", "hurt"]):
        responses = [
            "I'm really sorry you're feeling that way. Do you want to talk about it?",
            "It's okay to feel sad sometimes. I'm here to listen.",
            "What happened today that made you feel this way?"
        ]
        return random.choice(responses)

    # Anger
    elif any(word in text for word in ["angry", "mad", "frustrated"]):
        responses = [
            "Anger is valid. What triggered it?",
            "Take a slow breath before reacting. Do you want to tell me what happened?",
            "It helps to pause and reflect. What’s bothering you most?"
        ]
        return random.choice(responses)

    # Happiness
    elif any(word in text for word in ["happy", "excited", "great", "good day"]):
        responses = [
            "That’s wonderful 🌸 What made today good?",
            "I love hearing that! Tell me more!",
            "That’s beautiful. What are you grateful for today?"
        ]
        return random.choice(responses)

    # Sleep
    elif any(word in text for word in ["sleep", "tired", "insomnia"]):
        responses = [
            "Sleep is important. Try reducing screen time before bed.",
            "A calm breathing exercise might help you sleep better.",
            "Have you been sleeping at regular times?"
        ]
        return random.choice(responses)
    # Motivation
    elif any(word in text for word in ["motivation", "lazy", "procrastinate", "unmotivated"]):
        return (
            "It’s normal to feel stuck sometimes. "
            "Start with one small task — even 5 minutes can help."
        )

    # Meditation
    elif "meditation" in text:
        return (
            "Let’s try something simple:\n"
            "Inhale for 4 seconds.\n"
            "Hold for 4 seconds.\n"
            "Exhale for 4 seconds.\n"
            "Repeat 4 times."
        )

    # Relationship
    elif any(word in text for word in ["relationship", "breakup", "fight"]):
        return (
            "Relationships can be emotionally intense. "
            "Do you want to share what happened?"
        )

    # Default
    else:
        return "I'm here for you. Tell me more about what you're feeling."
# ================== SCHEDULE ==================

@login_required
def schedule(request):
    activities = Activity.objects.filter(user=request.user).order_by('time')

    if request.method == "POST":
        form = ActivityForm(request.POST)
        if form.is_valid():
            activity = form.save(commit=False)
            activity.user = request.user
            activity.save()
            return redirect('schedule')
    else:
        form = ActivityForm()

    return render(request, 'app/schedule.html', {
        'activities': activities,
        'form': form
    })


@login_required
def delete_activity(request, id):
    activity = Activity.objects.get(id=id, user=request.user)
    activity.delete()
    return redirect('schedule')


@login_required
def edit_activity(request, id):
    activity = Activity.objects.get(id=id, user=request.user)

    if request.method == "POST":
        form = ActivityForm(request.POST, instance=activity)
        if form.is_valid():
            form.save()
            return redirect('schedule')
    else:
        form = ActivityForm(instance=activity)

    return render(request, 'edit.html', {
        'form': form
    })


# ================== AUTH ==================

def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')
    else:
        form = UserCreationForm()

    return render(request, 'register.html', {
        'form': form
    })