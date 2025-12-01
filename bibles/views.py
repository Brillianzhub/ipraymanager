# views.py
from urllib.parse import unquote
from rest_framework.response import Response
from rest_framework.decorators import api_view
from django.shortcuts import get_object_or_404
from .models import Book, Chapter
from .serializers import VerseSerializer


from .models import VerseKJV, VerseNIV, VerseASV, VerseAMP

VERSION_MODELS = {
    "kjv": VerseKJV,
    "niv": VerseNIV,
    "asv": VerseASV,
    "amp": VerseAMP,
}


# @api_view(["GET"])
# def get_chapter_verses(request, version, book_name, chapter_number):
#     # Ensure version exists
#     Model = VERSION_MODELS.get(version.lower())
#     if not Model:
#         return Response({"error": "Invalid version"}, status=400)

#     # Find the chapter
#     book = get_object_or_404(Book, name__iexact=book_name)
#     chapter = get_object_or_404(Chapter, book=book, number=chapter_number)

#     # Fetch verses
#     verses = Model.objects.filter(chapter=chapter).order_by("verse")
#     serializer = VerseSerializer(verses, many=True)
#     return Response(serializer.data)


@api_view(["GET"])
def get_chapter_verses(request, version, book_name, chapter_number):
    book_name = unquote(book_name)  # converts '1%20Kings' → '1 Kings'

    Model = VERSION_MODELS.get(version.lower())
    if not Model:
        return Response({"error": "Invalid version"}, status=400)

    book = get_object_or_404(Book, name__iexact=book_name)
    chapter = get_object_or_404(Chapter, book=book, number=chapter_number)

    verses = Model.objects.filter(chapter=chapter).order_by("verse")
    serializer = VerseSerializer(verses, many=True)
    return Response(serializer.data)
