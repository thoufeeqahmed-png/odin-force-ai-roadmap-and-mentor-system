import json
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.http import JsonResponse, HttpResponse
from django.contrib import messages
from django.db import transaction
from django.views.decorators.http import require_POST

from .models import Roadmap, RoadmapStage, LearningTask
from .forms import RoadmapGenerationForm
from .ai_service import TAJuniorAIService


def home_view(request):
    """
    Landing Page for ODIN TA Junior with Norse Pantheon showcase.
    """
    total_roadmaps = Roadmap.objects.count()
    recent_roadmaps = Roadmap.objects.all()[:3]
    council = TAJuniorAIService.get_pantheon_council(
        domain="Any Skill or Goal",
        goal="Mastery & Achievement"
    )
    return render(request, 'roadmap/home.html', {
        'total_roadmaps': total_roadmaps,
        'recent_roadmaps': recent_roadmaps,
        'council': council,
    })


def generate_roadmap_view(request):
    """
    Roadmap Generator Form & AI synthesis processor.
    """
    if request.method == 'POST':
        form = RoadmapGenerationForm(request.POST)
        if form.is_valid():
            user_name = form.cleaned_data.get('user_name') or 'Learner'
            domain = form.cleaned_data['domain']
            current_level = form.cleaned_data['current_level']
            goal = form.cleaned_data['goal']
            available_time = form.cleaned_data['available_time']
            duration = form.cleaned_data['duration']
            existing_skills = form.cleaned_data.get('existing_skills', '')
            mentor = form.cleaned_data.get('mentor', 'auto')

            try:
                # Call AI service with mentor
                ai_data = TAJuniorAIService.generate_roadmap(
                    domain=domain,
                    current_level=current_level,
                    goal=goal,
                    available_time=available_time,
                    duration=duration,
                    existing_skills=existing_skills,
                    user_name=user_name,
                    mentor=mentor
                )

                # Persist in atomic transaction
                with transaction.atomic():
                    roadmap = form.save(commit=False)
                    roadmap.greeting_message = ai_data.get('greeting_message', '')
                    roadmap.junior_advice = ai_data.get('junior_advice', '')
                    roadmap.mentor = ai_data.get('selected_mentor', mentor)
                    roadmap.mentor_greeting = ai_data.get('mentor_greeting', '')
                    roadmap.roadmap_content = json.dumps(ai_data, indent=2)
                    roadmap.save()

                    stages_list = ai_data.get('stages', [])
                    for s_idx, stage_info in enumerate(stages_list, start=1):
                        stage = RoadmapStage.objects.create(
                            roadmap=roadmap,
                            title=stage_info.get('title', f"Stage {s_idx}"),
                            description=stage_info.get('description', ''),
                            why_it_matters=stage_info.get('why_it_matters', ''),
                            what_to_practice=stage_info.get('what_to_practice', ''),
                            suggested_projects=stage_info.get('suggested_projects', ''),
                            estimated_duration=stage_info.get('estimated_duration', 'Weeks 1-4'),
                            order=s_idx,
                        )

                        tasks_list = stage_info.get('tasks', [])
                        for t_idx, task_info in enumerate(tasks_list, start=1):
                            LearningTask.objects.create(
                                stage=stage,
                                title=task_info.get('title', f"Task {t_idx}"),
                                description=task_info.get('desc', ''),
                                task_type=task_info.get('type', 'topic'),
                                completed=False,
                                order=t_idx
                            )

                messages.success(request, f"🎉 Woohoo! TA Junior & the Council created your personalized '{roadmap.domain}' roadmap!")
                return redirect('roadmap_detail', pk=roadmap.pk)

            except Exception as e:
                messages.error(request, f"An error occurred while generating your roadmap: {str(e)}")
    else:
        # Pre-fill initial domain if passed as query parameter
        initial_domain = request.GET.get('domain', '')
        initial_data = {}
        if initial_domain:
            initial_data['domain'] = initial_domain
        form = RoadmapGenerationForm(initial=initial_data)

    return render(request, 'roadmap/generate.html', {'form': form})


def roadmap_detail_view(request, pk):
    """
    Display the complete personalized roadmap, stages, tasks, and Norse council advice.
    """
    roadmap = get_object_or_404(Roadmap.objects.prefetch_related('stages__tasks'), pk=pk)
    stages = roadmap.stages.all().order_by('order')
    current_stage = roadmap.current_stage
    next_task = roadmap.next_daily_task
    daily_practice = roadmap.daily_practice_task

    odin_wisdom = TAJuniorAIService.get_odin_wisdom(roadmap.domain, roadmap.goal, roadmap.current_level)
    thor_challenge = TAJuniorAIService.get_thor_challenge(current_stage.title if current_stage else "Roadmap", roadmap.domain)
    loki_hack = TAJuniorAIService.get_loki_hack(current_stage.title if current_stage else "Roadmap", roadmap.domain)

    return render(request, 'roadmap/detail.html', {
        'roadmap': roadmap,
        'stages': stages,
        'current_stage': current_stage,
        'next_task': next_task,
        'daily_practice': daily_practice,
        'odin_wisdom': odin_wisdom,
        'thor_challenge': thor_challenge,
        'loki_hack': loki_hack,
    })


def daily_guidance_view(request, pk=None):
    """
    Dedicated view for Today's Goal, What to Learn, Practice Task, Thor's Drill, and Loki's Hack.
    """
    if pk:
        roadmap = get_object_or_404(Roadmap.objects.prefetch_related('stages__tasks'), pk=pk)
    else:
        roadmap = Roadmap.objects.first()
        if not roadmap:
            messages.info(request, "Please create a roadmap first to view daily guidance.")
            return redirect('generate_roadmap')

    current_stage = roadmap.current_stage
    next_task = roadmap.next_daily_task
    daily_practice = roadmap.daily_practice_task
    today_quote = TAJuniorAIService.SUPPORTIVE_QUOTES[hash(str(roadmap.pk)) % len(TAJuniorAIService.SUPPORTIVE_QUOTES)]

    stage_title = current_stage.title if current_stage else "Foundations"
    thor_drill = TAJuniorAIService.get_thor_challenge(stage_title, roadmap.domain)
    loki_hack = TAJuniorAIService.get_loki_hack(stage_title, roadmap.domain)
    odin_vision = TAJuniorAIService.get_odin_wisdom(roadmap.domain, roadmap.goal, roadmap.current_level)

    return render(request, 'roadmap/daily_guidance.html', {
        'roadmap': roadmap,
        'current_stage': current_stage,
        'next_task': next_task,
        'daily_practice': daily_practice,
        'today_quote': today_quote,
        'thor_drill': thor_drill,
        'loki_hack': loki_hack,
        'odin_vision': odin_vision,
    })


def progress_view(request, pk=None):
    """
    Progress tracking dashboard: completed topics, current stage, overall %, projects.
    """
    if pk:
        roadmap = get_object_or_404(Roadmap.objects.prefetch_related('stages__tasks'), pk=pk)
    else:
        roadmap = Roadmap.objects.first()
        if not roadmap:
            messages.info(request, "Please create a roadmap first to track progress.")
            return redirect('generate_roadmap')

    stages = roadmap.stages.all().order_by('order')
    all_tasks = LearningTask.objects.filter(stage__roadmap=roadmap).order_by('stage__order', 'order')

    return render(request, 'roadmap/progress.html', {
        'roadmap': roadmap,
        'stages': stages,
        'all_tasks': all_tasks,
    })


def history_view(request):
    """
    Roadmap History: List, search, view, or delete previous roadmaps.
    """
    query = request.GET.get('q', '').strip()
    roadmaps = Roadmap.objects.all()
    if query:
        roadmaps = roadmaps.filter(domain__icontains=query) | roadmaps.filter(goal__icontains=query)

    return render(request, 'roadmap/history.html', {
        'roadmaps': roadmaps,
        'query': query,
    })


@require_POST
def delete_roadmap_view(request, pk):
    """
    Delete a saved roadmap with confirmation.
    """
    roadmap = get_object_or_404(Roadmap, pk=pk)
    domain = roadmap.domain
    roadmap.delete()
    messages.info(request, f"Roadmap for '{domain}' was deleted.")
    return redirect('roadmap_history')


@require_POST
def toggle_task_view(request, pk):
    """
    Toggle completed status of a LearningTask via AJAX or form POST.
    """
    task = get_object_or_404(LearningTask, pk=pk)
    task.completed = not task.completed
    task.save()

    stage = task.stage
    roadmap = stage.roadmap

    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.GET.get('format') == 'json':
        return JsonResponse({
            'success': True,
            'task_id': task.pk,
            'completed': task.completed,
            'stage_id': stage.pk,
            'stage_progress': stage.progress_percentage,
            'stage_completed_count': stage.completed_tasks_count,
            'stage_total_count': stage.total_tasks_count,
            'roadmap_progress': roadmap.progress_percentage,
            'completed_tasks': roadmap.completed_tasks,
            'total_tasks': roadmap.total_tasks,
            'completed_topics': roadmap.completed_topics,
            'completed_projects': roadmap.completed_projects,
        })

    # Standard POST fallback
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or reverse('roadmap_detail', kwargs={'pk': roadmap.pk})
    return redirect(next_url)


@require_POST
def ask_ta_junior_view(request, pk):
    """
    Interactive Q&A response from TA Junior or specific Norse Mentors.
    """
    roadmap = get_object_or_404(Roadmap, pk=pk)
    question = request.POST.get('question', '').strip()
    stage_title = request.POST.get('stage_title', 'General Roadmap')
    mentor = request.POST.get('mentor', 'ta_junior').lower()

    if not question:
        return JsonResponse({'error': 'Please provide a question.'}, status=400)

    if mentor == 'odin':
        answer = f"👁️ **Allfather Odin answers:**\n\nRegarding *'{question}'* in **{stage_title}**:\nLook beyond the immediate frustration. The challenge you face is the exact trial designed to test your strategic fortitude. Meditate upon foundational principles, consult your notes (the ravens' memory), and proceed with deliberate precision."
    elif mentor == 'thor':
        answer = f"⚡ **Thor answers:**\n\nRegarding *'{question}'* in **{stage_title}**:\nHaha! Don't overthink it—strike the problem! If you are stuck on '{question}', put away all distractions for 20 minutes and code/practice 5 quick variations until your hands master it. Action dispels fear!"
    elif mentor == 'loki':
        answer = f"🐍 **Loki answers:**\n\nRegarding *'{question}'* in **{stage_title}**:\nShh, here is the secret: you don't have to follow the boring standard path. For '{question}', look for existing open-source examples, copy the pattern, tweak one variable at a time, and see why it breaks. Reverse-engineering is the fastest cheat code!"
    else:
        answer = TAJuniorAIService.ask_ta_junior_for_stage_help(stage_title, question, roadmap.domain)

    return JsonResponse({
        'success': True,
        'question': question,
        'stage_title': stage_title,
        'mentor': mentor,
        'answer': answer,
    })
