from django.test import TestCase, Client
from django.urls import reverse
from .models import Roadmap, RoadmapStage, LearningTask
from .ai_service import TAJuniorAIService


class OdinForceModelAndServiceTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.roadmap = Roadmap.objects.create(
            domain="Artificial Intelligence",
            current_level="Beginner",
            goal="Become an AI Engineer",
            available_time="2 hours per day",
            duration="6 months",
            existing_skills="Python basics",
            user_name="Sam",
            greeting_message="Hello Sam! I am ODIN FORCE.",
            junior_advice="Take it one step at a time!"
        )
        self.stage1 = RoadmapStage.objects.create(
            roadmap=self.roadmap,
            title="Stage 1 — Foundations",
            description="Python and Math basics",
            why_it_matters="AI requires math foundations",
            what_to_practice="Vector drills in NumPy",
            suggested_projects="Vector math visualizer",
            order=1,
            estimated_duration="Weeks 1-4"
        )
        self.stage2 = RoadmapStage.objects.create(
            roadmap=self.roadmap,
            title="Stage 2 — Machine Learning",
            description="Supervised learning",
            why_it_matters="Core ML is the basis of all AI",
            what_to_practice="Regression models",
            suggested_projects="Churn predictor",
            order=2,
            estimated_duration="Weeks 5-8"
        )
        self.task1 = LearningTask.objects.create(
            stage=self.stage1,
            title="NumPy Basics",
            description="Array operations",
            task_type="topic",
            completed=False,
            order=1
        )
        self.task2 = LearningTask.objects.create(
            stage=self.stage1,
            title="Matrix Practice",
            description="Vector math",
            task_type="practice",
            completed=False,
            order=2
        )
        self.task3 = LearningTask.objects.create(
            stage=self.stage2,
            title="Decision Trees",
            description="Tree algorithms",
            task_type="topic",
            completed=False,
            order=1
        )

    def test_roadmap_properties(self):
        self.assertEqual(self.roadmap.total_tasks, 3)
        self.assertEqual(self.roadmap.completed_tasks, 0)
        self.assertEqual(self.roadmap.progress_percentage, 0)

        # Mark task 1 complete
        self.task1.completed = True
        self.task1.save()

        self.assertEqual(self.roadmap.completed_tasks, 1)
        self.assertEqual(self.roadmap.progress_percentage, 33)

        # Stage progress
        self.assertEqual(self.stage1.progress_percentage, 50)
        self.assertFalse(self.stage1.is_completed)

        # Current stage should be stage 1
        self.assertEqual(self.roadmap.current_stage, self.stage1)

        # Complete stage 1 tasks
        self.task2.completed = True
        self.task2.save()
        self.assertTrue(self.stage1.is_completed)
        self.assertEqual(self.roadmap.current_stage, self.stage2)

    def test_ai_service_known_domain(self):
        result = TAJuniorAIService.generate_roadmap(
            domain="Artificial Intelligence",
            current_level="Beginner",
            goal="Become an AI Engineer",
            available_time="2 hours per day",
            duration="6 months",
            existing_skills="Python basics",
            user_name="Jordan"
        )
        self.assertIn("greeting_message", result)
        self.assertIn("junior_advice", result)
        self.assertIn("stages", result)
        self.assertGreaterEqual(len(result["stages"]), 4)
        first_stage = result["stages"][0]
        self.assertIn("why_it_matters", first_stage)
        self.assertIn("what_to_practice", first_stage)
        self.assertIn("suggested_projects", first_stage)

    def test_ai_service_custom_domain(self):
        result = TAJuniorAIService.generate_roadmap(
            domain="Astronomy & Astrophotography",
            current_level="Complete Beginner",
            goal="Photograph deep space nebulae",
            available_time="1 hour per day",
            duration="3 months",
            existing_skills="None",
            user_name="Elena"
        )
        self.assertIn("greeting_message", result)
        self.assertEqual(len(result["stages"]), 5)
        self.assertIn("Astronomy & Astrophotography", result["stages"][0]["title"])

    def test_norse_council_methods(self):
        odin = TAJuniorAIService.get_odin_wisdom("Game Development", "Build an RPG")
        thor = TAJuniorAIService.get_thor_challenge("Physics Engines", "Game Development")
        loki = TAJuniorAIService.get_loki_hack("Shader Optimization", "Game Development")
        council = TAJuniorAIService.get_pantheon_council("Game Development", "Build an RPG")

        self.assertIn("Allfather Odin", odin)
        self.assertIn("Thor's Thunder Drill", thor)
        self.assertIn("Loki's Clever Hack", loki)
        self.assertIn("odin", council)
        self.assertIn("thor", council)
        self.assertIn("loki", council)

    def test_home_view(self):
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "ODIN FORCE")
        self.assertContains(response, "Council of Asgard")
        self.assertContains(response, "ALLFATHER ODIN")
        self.assertContains(response, "THOR THE THUNDERER")
        self.assertContains(response, "LOKI THE TRICKSTER")

    def test_generate_roadmap_post(self):
        data = {
            'domain': 'Digital Photography',
            'current_level': 'Beginner',
            'goal': 'Start a portrait business',
            'available_time': '1 hour per day',
            'duration': '3 months',
            'existing_skills': 'Smartphone camera',
            'user_name': 'Taylor'
        }
        response = self.client.post(reverse('generate_roadmap'), data, follow=True)
        self.assertEqual(response.status_code, 200)
        new_roadmap = Roadmap.objects.filter(domain='Digital Photography').first()
        self.assertIsNotNone(new_roadmap)
        self.assertGreater(new_roadmap.stages.count(), 0)

    def test_roadmap_detail_view(self):
        response = self.client.get(reverse('roadmap_detail', kwargs={'pk': self.roadmap.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.roadmap.goal)
        self.assertContains(response, "Why this matters")
        self.assertContains(response, "Odin's Vision")

    def test_daily_guidance_view(self):
        response = self.client.get(reverse('roadmap_daily_guidance', kwargs={'pk': self.roadmap.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Today's Strategic Goal")
        self.assertContains(response, "Core Concept to Master")
        self.assertContains(response, "Thunder Practice Drill")
        self.assertContains(response, "Loki's 80/20 Creative Hack")

    def test_progress_view(self):
        response = self.client.get(reverse('roadmap_progress', kwargs={'pk': self.roadmap.pk}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Valhalla")
        self.assertContains(response, "Milestones")

    def test_history_view_and_delete(self):
        response = self.client.get(reverse('roadmap_history'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.roadmap.domain)

        # Test search
        response_search = self.client.get(reverse('roadmap_history') + '?q=Artificial')
        self.assertContains(response_search, self.roadmap.domain)

        # Test delete
        del_response = self.client.post(reverse('delete_roadmap', kwargs={'pk': self.roadmap.pk}), follow=True)
        self.assertEqual(del_response.status_code, 200)
        self.assertEqual(Roadmap.objects.filter(pk=self.roadmap.pk).count(), 0)

    def test_toggle_task_ajax(self):
        url = reverse('toggle_task', kwargs={'pk': self.task1.pk}) + '?format=json'
        response = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(response.status_code, 200)
        data = response.json()
        self.assertTrue(data['success'])
        self.assertTrue(data['completed'])

        # Toggle back
        response2 = self.client.post(url, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        data2 = response2.json()
        self.assertFalse(data2['completed'])

    def test_ask_council_mentor_endpoints(self):
        url = reverse('ask_ta_junior', kwargs={'pk': self.roadmap.pk})
        
        # Test default
        res1 = self.client.post(url, {'question': 'How can I practice this?', 'stage_title': 'Stage 1'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res1.status_code, 200)
        self.assertTrue(res1.json()['success'])

        # Test Odin mentor
        res_odin = self.client.post(url, {'question': 'Give me wisdom', 'stage_title': 'Stage 1', 'mentor': 'odin'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res_odin.status_code, 200)
        self.assertIn("Odin", res_odin.json()['answer'])

        # Test Thor mentor
        res_thor = self.client.post(url, {'question': 'How to drill?', 'stage_title': 'Stage 1', 'mentor': 'thor'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res_thor.status_code, 200)
        self.assertIn("Thor", res_thor.json()['answer'])

        # Test Loki mentor
        res_loki = self.client.post(url, {'question': 'Any cheat codes?', 'stage_title': 'Stage 1', 'mentor': 'loki'}, HTTP_X_REQUESTED_WITH='XMLHttpRequest')
        self.assertEqual(res_loki.status_code, 200)
        self.assertIn("Loki", res_loki.json()['answer'])
