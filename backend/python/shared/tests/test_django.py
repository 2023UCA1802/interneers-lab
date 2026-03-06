from django.test import SimpleTestCase
from shared.adapter.greeting_service import GreetingService

class TestGreeting(SimpleTestCase):

    def setUp(self):
        self.service=GreetingService()

    def test_greeting(self):
        test_cases=[
            ("Manas", 25, "Hello Manas, you are 25 years old."),
            ("Alice", 30, "Hello Alice, you are 30 years old."),
            ("Bob", 18, "Hello Bob, you are 18 years old."),
            ("Test", 1, "Hello Test, you are 1 years old."),
        ]
        for name, age, expected in test_cases:
            with self.subTest(name=name,age=age):
                result=self.service.generate_greeting(name,age)
                self.assertEqual(result,expected)