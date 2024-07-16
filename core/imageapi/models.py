from django.db import models

class Image(models.Model):
    original = models.ImageField(upload_to='images/')
    processed = models.ImageField(upload_to='images/', blank=True, null=True)
    width = models.PositiveIntegerField(null=True)
    height = models.PositiveIntegerField(null=True)
    shape = models.CharField(null=True, max_length=10, choices=[('rectangle', 'Rectangle'), ('circle', 'Circle'), ('oval', 'Oval')])
    uploaded_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return f'Image {self.id} - {self.shape} ({self.width}x{self.height})'
