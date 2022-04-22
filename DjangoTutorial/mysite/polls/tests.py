import datetime

from django.utils import timezone
from django.test import TestCase

from .models import Question
# Create your tests here.
class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        time = timezone.now() + datetime.timedelta(30)
        future_question = Question(pub_date=time)
        self.assertIs(future_question.was_published_recently(), False)