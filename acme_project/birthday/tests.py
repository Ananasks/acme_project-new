from datetime import date

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Birthday


class BirthdayAccessTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.author = get_user_model().objects.create_user(username='author')
        cls.other = get_user_model().objects.create_user(username='other')
        cls.birthday = Birthday.objects.create(
            first_name='Анна',
            birthday=date(2000, 1, 1),
            author=cls.author,
        )

    def test_anonymous_access(self):
        response = self.client.get(reverse('birthday:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, 'Изменить запись')
        self.assertNotContains(response, 'Удалить запись')
        self.assertNotContains(response, 'Калькулятор дней рождения')
        detail_url = reverse('birthday:detail', args=[self.birthday.pk])
        self.assertEqual(self.client.get(detail_url).status_code, 200)
        for name in ('edit', 'delete'):
            url = reverse(f'birthday:{name}', args=[self.birthday.pk])
            for method in (self.client.get, self.client.post):
                with self.subTest(name=name, method=method.__name__):
                    self.assertRedirects(
                        method(url), f'{reverse("login")}?next={url}',
                        fetch_redirect_response=False,
                    )

    def test_other_user_cannot_change_record(self):
        self.client.force_login(self.other)
        for name in ('edit', 'delete'):
            url = reverse(f'birthday:{name}', args=[self.birthday.pk])
            for method in (self.client.get, self.client.post):
                with self.subTest(name=name, method=method.__name__):
                    self.assertEqual(method(url).status_code, 403)
        self.birthday.refresh_from_db()
        self.assertEqual(self.birthday.first_name, 'Анна')
        response = self.client.get(reverse('birthday:list'))
        self.assertNotContains(response, 'Изменить запись')
        self.assertNotContains(response, 'Удалить запись')
        self.assertContains(response, 'Калькулятор дней рождения')

    def test_author_can_edit_and_delete(self):
        self.client.force_login(self.author)
        response = self.client.get(reverse('birthday:list'))
        self.assertContains(response, 'Изменить запись')
        self.assertContains(response, 'Удалить запись')
        self.assertContains(response, 'Калькулятор дней рождения')
        edit_url = reverse('birthday:edit', args=[self.birthday.pk])
        self.assertEqual(self.client.get(edit_url).status_code, 200)
        response = self.client.post(edit_url, {
            'first_name': 'Мария',
            'last_name': '',
            'birthday': '2000-01-01',
        })
        self.assertRedirects(response, self.birthday.get_absolute_url())
        self.birthday.refresh_from_db()
        self.assertEqual(self.birthday.first_name, 'Мария')
        self.assertEqual(self.birthday.author, self.author)
        delete_url = reverse('birthday:delete', args=[self.birthday.pk])
        self.assertEqual(self.client.get(delete_url).status_code, 200)
        self.assertRedirects(
            self.client.post(delete_url), reverse('birthday:list'),
        )
        self.assertFalse(Birthday.objects.filter(pk=self.birthday.pk).exists())
