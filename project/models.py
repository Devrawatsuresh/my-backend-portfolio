from django.db import models

def project_image_path(instance, filename):
    # This will save images in /media/project/<filename>
    return f"project/{filename}"

class Project(models.Model):
    title = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    description = models.TextField()
    
    # Single image example
    image = models.ImageField(upload_to=project_image_path, blank=True, null=True)

    # For multiple images as slideshow
    images = models.JSONField(default=list)  # We'll store list of URLs
    
    tags = models.JSONField(default=list)
    github = models.URLField(blank=True, null=True)
    live = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
