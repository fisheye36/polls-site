import datetime

from django.test import TestCase
from django.urls import reverse
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


def _create_question(question_text, days):
    publication_date = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, publication_date=publication_date)


class IndexViewTests(TestCase):
    NO_POLLS = 'No polls are available at this time.'

    def test_no_questions(self):
        response = self.client.get(reverse('polls:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.NO_POLLS)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question_text = 'Past question'
        _create_question(question_text, days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: %s>' % question_text])

    def test_future_question(self):
        _create_question('Future question', days=1)
        response = self.client.get(reverse('polls:index'))
        self.assertContains(response, self.NO_POLLS)
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_and_past_questions(self):
        past_question_text = 'Past question'
        _create_question(past_question_text, days=-1)
        _create_question('Future question', days=7)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'], ['<Question: %s>' % past_question_text])

    def test_past_questions_order(self):
        old_question_text = 'Old question'
        _create_question(old_question_text, days=-7)
        recent_question_text = 'Recent question'
        _create_question(recent_question_text, days=-1)
        response = self.client.get(reverse('polls:index'))
        self.assertQuerysetEqual(response.context['latest_question_list'],
                                 ['<Question: %s>' % recent_question_text, '<Question: %s>' % old_question_text])


class DetailViewTests(TestCase):

    def test_past_question(self):
        past_question = _create_question('Past question', days=-1)
        response = self.client.get(reverse('polls:detail', args=(past_question.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, past_question.question_text)

    def test_future_question(self):
        future_question = _create_question('Future question', days=1)
        response = self.client.get(reverse('polls:detail', args=(future_question.pk,)))
        self.assertEqual(response.status_code, 404)
