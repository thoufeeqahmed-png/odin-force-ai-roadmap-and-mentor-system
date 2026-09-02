from django import forms
from .models import Roadmap


class RoadmapGenerationForm(forms.ModelForm):
    TIME_CHOICES = [
        ('30 minutes per day', '30 minutes per day (Bite-sized consistency)'),
        ('1 hour per day', '1 hour per day (Steady standard pace)'),
        ('2 hours per day', '2 hours per day (Accelerated deep focus)'),
        ('4+ hours per day', '4+ hours per day (Intensive bootcamp immersion)'),
        ('5-10 hours per week', '5-10 hours per week (Flexible weekend schedule)'),
    ]

    DURATION_CHOICES = [
        ('1 month', '1 Month (Rapid sprint / Foundations)'),
        ('3 months', '3 Months (Quarterly deep dive)'),
        ('6 months', '6 Months (Comprehensive transformation)'),
        ('1 year', '1 Year (Complete mastery & portfolio)'),
    ]

    available_time = forms.ChoiceField(
        choices=TIME_CHOICES,
        initial='2 hours per day',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_available_time'})
    )

    duration = forms.ChoiceField(
        choices=DURATION_CHOICES,
        initial='6 months',
        widget=forms.Select(attrs={'class': 'form-select', 'id': 'id_duration'})
    )

    mentor = forms.ChoiceField(
        choices=[
            ('auto', 'Let ODIN FORCE pick your mentor based on your goal'),
            ('odin', 'ODIN — Wise & Strategic (Long-term goals, career planning)'),
            ('thor', 'THOR — Motivating & Action-focused (Practical skills, projects)'),
            ('loki', 'LOKI — Creative & Problem-solving (Innovation, creative subjects)'),
        ],
        initial='auto',
        widget=forms.RadioSelect(attrs={'class': 'form-radio'})
    )

    class Meta:
        model = Roadmap
        fields = ['user_name', 'domain', 'current_level', 'goal', 'available_time', 'duration', 'existing_skills', 'mentor']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Alex (or leave as Learner)',
                'autocomplete': 'off'
            }),
            'domain': forms.TextInput(attrs={
                'class': 'form-input domain-input',
                'placeholder': 'e.g. Artificial Intelligence, Digital Photography, Finance, UI/UX...',
                'required': True,
                'autocomplete': 'off'
            }),
            'current_level': forms.Select(attrs={
                'class': 'form-select',
            }),
            'goal': forms.TextInput(attrs={
                'class': 'form-input',
                'placeholder': 'e.g. Become an AI Engineer, Launch a creative portfolio, Get hired...',
                'required': True,
                'autocomplete': 'off'
            }),
            'existing_skills': forms.Textarea(attrs={
                'class': 'form-textarea',
                'rows': 3,
                'placeholder': 'e.g. Python basics, Basic photo editing, None (complete beginner) — tell me what you already know!',
            }),
        }
        labels = {
            'user_name': 'Your Name (Optional)',
            'domain': 'Any Domain or Topic',
            'current_level': 'Your Current Skill Level',
            'goal': 'Your Learning or Career Goal',
            'available_time': 'Available Study Time',
            'duration': 'Target Completion Duration',
            'existing_skills': 'Existing Skills & Background (Optional)',
            'mentor': 'Choose Your Mentor Guide',
        }
        help_texts = {
            'domain': 'Enter literally any domain—tech, creative arts, business, music, science, or hobby.',
            'goal': 'What do you want to achieve or build at the end of this journey?',
            'existing_skills': 'TA Junior will tailor the roadmap to build on top of what you already know.',
            'mentor': 'Each mentor has a different teaching style. Choose one or let us pick!',
        }
