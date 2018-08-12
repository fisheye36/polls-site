import datetime

from django.test import TestCase
from django.utils import timezone

from .models import Question


class QuestionModelTests(TestCase):

    def test_was_published_recently_with_future_question(self):
        future_question = Question(publication_date=timezone.now() + datetime.timedelta(days=30))
        self.assertFalse(future_question.was_published_recently())

    def test_was_published_recently_with_old_question(self):
        publication_date = timezone.now() - datetime.timedelta(days=1.0, seconds=1.0)
        old_question = Question(publication_date=publication_date)
        self.assertFalse(old_question.was_published_recently())

    def test_was_published_recently_with_recent_question_default_period(self):
        publication_date = timezone.now() - datetime.timedelta(hours=23.0, minutes=59.0, seconds=59.0)
        recent_question = Question(publication_date=publication_date)
        self.assertTrue(recent_question.was_published_recently())

    def test_was_published_recently_with_recent_question_supplied_period(self):
        period = datetime.timedelta(weeks=1.0)
        recent_question = Question(publication_date=timezone.now() - period)
        self.assertTrue(recent_question.was_published_recently(recent_period=period + datetime.timedelta(seconds=1.0)))
