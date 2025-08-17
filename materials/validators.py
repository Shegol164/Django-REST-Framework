from django.core.exceptions import ValidationError
from urllib.parse import urlparse

def validate_youtube_url(value):
    """Проверяет, что ссылка ведет на youtube.com"""
    if value:
        domain = urlparse(value).netloc
        if not (domain == 'youtube.com' or domain.endswith('.youtube.com')):
            raise ValidationError('Разрешены только ссылки на youtube.com')