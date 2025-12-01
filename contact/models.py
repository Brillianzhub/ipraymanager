from django.db import models

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20, blank=True, null=True)  # optional
    subject = models.CharField(max_length=200)
    message = models.TextField()
    handled = models.BooleanField(default=False)
    remark = models.TextField(blank=True, null=True)  # admin remarks

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

