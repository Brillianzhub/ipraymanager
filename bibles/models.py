from django.db import models

# Create your models here.


class Category(models.Model):
    title = models.CharField(max_length=255, unique=True)
    featured = models.BooleanField(
        default=False, help_text="Mark as featured to show in featured categories")

    def __str__(self):
        return self.title


class Book(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(
        Category, related_name='book_category', on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f"{self.name} {self.category}"

    def get_next_book(self):
        next_book = Book.objects.filter(id__gt=self.id).order_by('id').first()
        return next_book

    def get_previous_book(self):
        previous_book = Book.objects.filter(
            id__lt=self.id).order_by('-id').first()
        return previous_book


class Chapter(models.Model):
    book = models.ForeignKey(
        Book, related_name='chapters', on_delete=models.CASCADE)
    number = models.IntegerField()

    class Meta:
        unique_together = ('book', 'number')
        verbose_name = "Chapter"
        verbose_name_plural = "Chapters"
        ordering = ['book', 'number']

    def __str__(self):
        return f"{self.book.name} {self.number}"

    def get_next_chapter(self):
        next_chapter = Chapter.objects.filter(
            book=self.book, number=self.number + 1).first()
        return next_chapter

    def get_previous_chapter(self):
        previous_chapter = Chapter.objects.filter(
            book=self.book, number=self.number - 1).first()
        return previous_chapter


class VerseKJV(models.Model):
    chapter = models.ForeignKey(
        Chapter, related_name='verses_kjv', on_delete=models.CASCADE)
    verse = models.IntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ('chapter', 'verse')

    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.verse}"

    def next_verse(self):
        next_verse = VerseKJV.objects.filter(
            chapter=self.chapter, verse__gt=self.verse).order_by('verse').first()

        if next_verse:
            return next_verse

        next_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__gt=self.chapter.number).order_by('number').first()

        if next_chapter:
            return VerseKJV.objects.filter(chapter=next_chapter).order_by('verse').first()

        return None

    def previous_verse(self):
        previous_verse = VerseKJV.objects.filter(
            chapter=self.chapter, verse__lt=self.verse).order_by('-verse').first()

        if previous_verse:
            return previous_verse

        previous_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__lt=self.chapter.number).order_by('-number').first()

        if previous_chapter:
            return VerseKJV.objects.filter(chapter=previous_chapter).order_by('-verse').first()

        return None


class VerseAMP(models.Model):
    chapter = models.ForeignKey(
        Chapter, related_name='verses_amp', on_delete=models.CASCADE)
    verse = models.IntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ('chapter', 'verse')

    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.verse}"

    def next_verse(self):
        next_verse = VerseAMP.objects.filter(
            chapter=self.chapter, verse__gt=self.verse).order_by('verse').first()

        if next_verse:
            return next_verse

        next_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__gt=self.chapter.number).order_by('number').first()

        if next_chapter:
            return VerseAMP.objects.filter(chapter=next_chapter).order_by('verse').first()

        return None

    def previous_verse(self):
        previous_verse = VerseAMP.objects.filter(
            chapter=self.chapter, verse__lt=self.verse).order_by('-verse').first()

        if previous_verse:
            return previous_verse

        previous_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__lt=self.chapter.number).order_by('-number').first()

        if previous_chapter:
            return VerseAMP.objects.filter(chapter=previous_chapter).order_by('-verse').first()

        return None


class VerseASV(models.Model):
    chapter = models.ForeignKey(
        Chapter, related_name='verses_asv', on_delete=models.CASCADE)
    verse = models.IntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ('chapter', 'verse')

    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.verse}"

    def next_verse(self):
        next_verse = VerseASV.objects.filter(
            chapter=self.chapter, verse__gt=self.verse).order_by('verse').first()

        if next_verse:
            return next_verse

        next_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__gt=self.chapter.number).order_by('number').first()

        if next_chapter:
            return VerseASV.objects.filter(chapter=next_chapter).order_by('verse').first()

        return None

    def previous_verse(self):
        previous_verse = VerseASV.objects.filter(
            chapter=self.chapter, verse__lt=self.verse).order_by('-verse').first()

        if previous_verse:
            return previous_verse

        previous_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__lt=self.chapter.number).order_by('-number').first()

        if previous_chapter:
            return VerseASV.objects.filter(chapter=previous_chapter).order_by('-verse').first()

        return None


class VerseNIV(models.Model):
    chapter = models.ForeignKey(
        Chapter, related_name='verses_niv', on_delete=models.CASCADE)
    verse = models.IntegerField()
    text = models.TextField()

    class Meta:
        unique_together = ('chapter', 'verse')

    def __str__(self):
        return f"{self.chapter.book.name} {self.chapter.number}:{self.verse}"

    def next_verse(self):
        next_verse = VerseNIV.objects.filter(
            chapter=self.chapter, verse__gt=self.verse).order_by('verse').first()

        if next_verse:
            return next_verse

        next_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__gt=self.chapter.number).order_by('number').first()

        if next_chapter:
            return VerseNIV.objects.filter(chapter=next_chapter).order_by('verse').first()

        return None

    def previous_verse(self):
        previous_verse = VerseNIV.objects.filter(
            chapter=self.chapter, verse__lt=self.verse).order_by('-verse').first()

        if previous_verse:
            return previous_verse

        previous_chapter = Chapter.objects.filter(
            book=self.chapter.book, number__lt=self.chapter.number).order_by('-number').first()

        if previous_chapter:
            return VerseNIV.objects.filter(chapter=previous_chapter).order_by('-verse').first()

        return None
