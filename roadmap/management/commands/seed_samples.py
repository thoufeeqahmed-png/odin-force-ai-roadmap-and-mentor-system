from django.core.management.base import BaseCommand
from roadmap.models import Roadmap, RoadmapStage, LearningTask
from roadmap.ai_service import TAJuniorAIService
import json


class Command(BaseCommand):
    help = "Seeds initial sample roadmaps for ODIN TA Junior"

    def handle(self, *args, **options):
        if Roadmap.objects.exists():
            self.stdout.write("Database already contains roadmaps.")
            return

        samples = [
            {
                "domain": "Artificial Intelligence",
                "current_level": "Beginner",
                "goal": "Become an AI Engineer",
                "available_time": "2 hours per day",
                "duration": "6 months",
                "existing_skills": "Python basics",
                "user_name": "Alex"
            },
            {
                "domain": "Digital Photography",
                "current_level": "Complete Beginner",
                "goal": "Start a Portrait & Landscape Photography Studio",
                "available_time": "1 hour per day",
                "duration": "3 months",
                "existing_skills": "Basic smartphone shooting",
                "user_name": "Sarah"
            }
        ]

        for s in samples:
            ai_data = TAJuniorAIService.generate_roadmap(
                domain=s["domain"],
                current_level=s["current_level"],
                goal=s["goal"],
                available_time=s["available_time"],
                duration=s["duration"],
                existing_skills=s["existing_skills"],
                user_name=s["user_name"]
            )

            roadmap = Roadmap.objects.create(
                domain=s["domain"],
                current_level=s["current_level"],
                goal=s["goal"],
                available_time=s["available_time"],
                duration=s["duration"],
                existing_skills=s["existing_skills"],
                user_name=s["user_name"],
                greeting_message=ai_data.get("greeting_message", ""),
                junior_advice=ai_data.get("junior_advice", ""),
                roadmap_content=json.dumps(ai_data, indent=2)
            )

            for s_idx, stage_info in enumerate(ai_data.get("stages", []), start=1):
                stage = RoadmapStage.objects.create(
                    roadmap=roadmap,
                    title=stage_info.get("title", f"Stage {s_idx}"),
                    description=stage_info.get("description", ""),
                    why_it_matters=stage_info.get("why_it_matters", ""),
                    what_to_practice=stage_info.get("what_to_practice", ""),
                    suggested_projects=stage_info.get("suggested_projects", ""),
                    estimated_duration=stage_info.get("estimated_duration", "Weeks 1-4"),
                    order=s_idx
                )

                for t_idx, task_info in enumerate(stage_info.get("tasks", []), start=1):
                    # Mark the first task of the first roadmap complete as a starter demonstration
                    is_completed = (s_idx == 1 and t_idx == 1 and s["domain"] == "Artificial Intelligence")
                    LearningTask.objects.create(
                        stage=stage,
                        title=task_info.get("title", f"Task {t_idx}"),
                        description=task_info.get("desc", ""),
                        task_type=task_info.get("type", "topic"),
                        completed=is_completed,
                        order=t_idx
                    )

        self.stdout.write(self.style.SUCCESS("Successfully seeded sample roadmaps!"))
