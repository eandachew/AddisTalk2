from django.db import models

class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)  # Field is named created_on
    is_read = models.BooleanField(default=False)
    resolved = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_on']  # Changed from created_at to created_on
        verbose_name = 'Contact Message'
        verbose_name_plural = 'Contact Messages'

    def __str__(self):
        return f"{self.subject} - {self.name}"