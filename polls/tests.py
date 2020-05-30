import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse

from .models import Question

q_text = 'default'


def create_question(text=None, days=0):
    """ Create question with given text and days difference from now """
    if text is None:
        text = q_text
    return Question.objects.create(text=text,
                                   pub_date=timezone.now() +
                                   datetime.timedelta(days=days))


class QuestionModelTests(TestCase):
    def test_is_recent_on_future(self):
        """ `question.is_recent()` should return False when `question.pub_date`
        is future
        """
        q = create_question(days=3)
        self.assertIs(q.is_recent(), False)

    def test_is_recent_on_old(self):
        """ `question.is_recent()` should return False on old date """
        q = create_question(days=-3)
        self.assertIs(q.is_recent(), False)

    def test_is_recent_on_recent(self):
        """ Check if it return True on recent date """
        q = create_question()
        self.assertIs(q.is_recent(), True)


class QuestionIndexViewTests(TestCase):
    def test_no_questions(self):
        """ When there are no questions """
        resp = self.client.get(reverse('polls:index'))

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'No polls are available.')
        self.assertQuerysetEqual(resp.context['most_recent'], [])

    def test_past_question(self):
        """ Test on past question """
        q = create_question(days=-3)
        resp = self.client.get(reverse('polls:index'))

        self.assertIs(q.is_recent(), False)
        self.assertQuerysetEqual(resp.context['most_recent'],
                                 [f'<Question: {q_text}>'])

    def test_future_question(self):
        """ Test on future question """
        create_question(days=3)
        resp = self.client.get(reverse('polls:index'))

        self.assertContains(resp, 'No polls are available.')
        self.assertQuerysetEqual(resp.context['most_recent'], [])

    def test_future_question_and_past_question(self):
        """ Test with both future and past questions """
        create_question(days=-3)
        create_question(days=3)
        resp = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(resp.context['most_recent'],
                                 [f'<Question: {q_text}>'])

    def test_two_past_questions(self):
        """ Two past """
        create_question(text='1', days=-3)
        create_question(text='2', days=-4)
        resp = self.client.get(reverse('polls:index'))

        self.assertQuerysetEqual(resp.context['most_recent'],
                                 ['<Question: 1>', '<Question: 2>'])


class QuestionDetailViewTests(TestCase):
    def test_future_question(self):
        """ Should get 404 on future question """
        q = create_question(days=3)
        resp = self.client.get(reverse('polls:detail', args=(q.id, )))

        self.assertEqual(resp.status_code, 404)

    def test_past_question(self):
        """ Past question should be shown successfully """
        q = create_question(days=-3)
        resp = self.client.get(reverse('polls:detail', args=(q.id, )))

        self.assertContains(resp, q.text)
