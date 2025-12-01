import random
import string
import os
from django.utils.text import slugify
import re
from bs4 import BeautifulSoup



def get_filename(path):
    return os.path.basename(path)


def random_string_generator(size=10, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for i in range(size))


def unique_slug_generator(instance, new_slug=None):
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)
    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
            slug=slug,
            randstr=random_string_generator(size=4)
        )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


def calculate_reading_time(blog_post, words_per_minute=250):
    words = re.findall(r'\b\w+\b', blog_post)
    word_count = len(words)

    minutes = word_count / words_per_minute

    return word_count, minutes


def count_words(text):
    soup = BeautifulSoup(text, 'html.parser')
    plain_text = soup.get_text()

    words = plain_text.split()
    num_words = len(words)

    return num_words
