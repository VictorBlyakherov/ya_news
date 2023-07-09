# conftest.py
from datetime import datetime, timedelta

import pytest
from django.conf import settings
from django.urls import reverse
from django.utils import timezone

# Импортируем модель заметки, чтобы создать экземпляр.
from news.models import Comment, News


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def author(django_user_model):  
    return django_user_model.objects.create(username='Leo Tolstoy')


@pytest.fixture
# Используем встроенную фикстуру для модели пользователей django_user_model.
def reader(django_user_model):  
    return django_user_model.objects.create(username='Simple Reader')


@pytest.fixture
def author_client(author, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(author)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def reader_client(reader, client):  # Вызываем фикстуру автора и клиента.
    client.force_login(reader)  # Логиним автора в клиенте.
    return client


@pytest.fixture
def news():
    news = News.objects.create(  # Создаём объект заметки.
        title='Title',
        text='Note Text',
    )
    return news


@pytest.fixture
def comment(news, author):
    comment = Comment.objects.create(
        news=news,
        author=author,
        text=settings.COMMENT_TEXT,
    )
    return comment


@pytest.fixture
def news_list():
    today = datetime.today()
    all_news = [
        News(
            title=f'Новость {index}',
            text='Просто текст.',
            date=today - timedelta(days=index)
        )
        for index in range(settings.NEWS_COUNT_ON_HOME_PAGE + 1)
    ]
    News.objects.bulk_create(all_news)


@pytest.fixture
def comments_list(news, author):
    now = timezone.now()
    for index in range(2):
        comment = Comment.objects.create(
            text=f'Комментарий {index}',
            news=news,
            author=author,
        )
        comment.created = now + timedelta(days=index)
        comment.save()


@pytest.fixture
# Фикстура запрашивает другую фикстуру создания заметки.
def id_for_news(news):
    # И возвращает кортеж, который содержит slug заметки.
    # На то, что это кортеж, указывает запятая в конце выражения.
    return news.id,


@pytest.fixture
def get_detail_url(news):
    return reverse('news:detail', args=(news.id,))


@pytest.fixture
def get_edit_url(comment):
    return reverse('news:edit', args=(comment.id,))


@pytest.fixture
def get_delete_url(comment):
    return reverse('news:delete', args=(comment.id,))