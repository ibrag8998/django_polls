import datetime

from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from django.conf import settings

from .models import Question

q_text = 'default question'
choice_text = 'default choice'
default_choices = [{'text': choice_text}]


def create_question(text=None, days=0, choices=None):
    """ Create question with given text and days difference from now """
    if text is None:
        text = q_text
    if choices is None:
        choices = default_choices

    q = Question.objects.create(text=text,
                                pub_date=timezone.now() +
                                datetime.timedelta(days=days))
    for choice in choices:
        q.choice_set.create(**choice)

    return q


def login_testuser(client):
    """ Log testuser in """
    client.post(reverse('users:signup'), settings.TESTING['SIGNUP_CREDS'])
    client.post(reverse('users:signin'), settings.TESTING['SIGNIN_CREDS'])


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
    url = reverse('polls:index')

    def test_no_questions(self):
        """ When there are no questions """
        resp = self.client.get(self.url)

        self.assertEqual(resp.status_code, 200)
        self.assertContains(resp, 'No polls are available.')
        self.assertQuerysetEqual(resp.context['most_recent'], [])

    def test_past(self):
        """ Test on past question """
        create_question(days=-3)
        resp = self.client.get(self.url)

        self.assertQuerysetEqual(resp.context['most_recent'],
                                 [f'<Question: {q_text}>'])

    def test_future(self):
        """ Test on future question """
        create_question(days=3)
        resp = self.client.get(self.url)

        self.assertContains(resp, 'No polls are available.')
        self.assertQuerysetEqual(resp.context['most_recent'], [])

    def test_future_and_past(self):
        """ Test with both future and past questions """
        create_question(days=-3)
        create_question(days=3)
        resp = self.client.get(self.url)

        self.assertQuerysetEqual(resp.context['most_recent'],
                                 [f'<Question: {q_text}>'])

    def test_two_past(self):
        """ Two past """
        create_question(text='1', days=-3)
        create_question(text='2', days=-4)
        resp = self.client.get(self.url)

        self.assertQuerysetEqual(resp.context['most_recent'],
                                 ['<Question: 1>', '<Question: 2>'])

    def test_no_choices(self):
        """ Question without choices should not be displayed """
        create_question(choices=[])
        resp = self.client.get(self.url)

        self.assertQuerysetEqual(resp.context['most_recent'], [])


class QuestionDetailViewTests(TestCase):
    @staticmethod
    def url(q_id):
        """ Get `detail` url with given q.id """
        return reverse('polls:detail', args=(q_id, ))

    def test_future(self):
        """ Should get 404 on future question """
        q = create_question(days=3)
        resp = self.client.get(self.url(q.id))

        self.assertEqual(resp.status_code, 404)

    def test_past(self):
        """ Past question should be shown successfully """
        q = create_question(days=-3)
        resp = self.client.get(self.url(q.id))

        self.assertContains(resp, q.text)

    def test_no_choices(self):
        """ Should get 404 on question without choices """
        q = create_question(choices=[])
        resp = self.client.get(self.url(q.id))

        self.assertEqual(resp.status_code, 404)


class QuestionVoteViewTests(TestCase):
    @staticmethod
    def url(q_id):
        """ Get `vote` url with given q.id """
        return reverse('polls:vote', args=(q_id, ))

    def login_create_question(self):
        """ Log testuser in, create default question, return it """
        login_testuser(self.client)
        return create_question()

    def test_not_logged_in(self):
        """ Redirect guest user to `users:signin` """
        q = create_question()
        resp = self.client.post(self.url(q.id), follow=True)

        self.assertContains(resp, "Sign In")

    def test_logged_in(self):
        """ Everything OK if user logged int """
        q = self.login_create_question()
        resp = self.client.post(self.url(q.id), {'choice': '1'}, follow=True)

        self.assertContains(resp, "Results on")

    def test_no_choices(self):
        """ No redirect if choice not selected """
        q = self.login_create_question()
        resp = self.client.post(self.url(q.id), follow=True)

        self.assertEqual(resp.status_code, 200)
