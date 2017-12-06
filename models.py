from django.conf import settings
from django.db import models
from django.db.models.signals import pre_save
from django.urls import reverse
from django.utils import timezone
from django.utils.text import slugify


class PostManager(models.Manager):
    def active(self, *args, **kwargs):
        return super(PostManager, self).filter(published__lte=timezone.now(), draft=False)


def upload_location(instance, filename):
    return f"{instance.id}/{filename}"

# Create your models here.
class Post(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1)
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    image = models.ImageField(null=True,
                              blank=True,
                              upload_to=upload_location,
                              width_field="width_field",
                              height_field="height_field")
    height_field = models.IntegerField(default=0)
    width_field = models.IntegerField(default=0)
    content = models.TextField()
    draft = models.BooleanField(default=False)
    published = models.DateField(auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(auto_now=True,auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False,auto_now_add=True)

    objects = PostManager()

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-timestamp', "-updated")

    def get_absolute_url(self):
        return reverse("posts:detail", kwargs={"id": self.id})


def create_slug(instance, new_slug=None):
    main_slug = slugify(instance.title)
    count = 1
    slug = main_slug
    while True:
        exists = Post.objects.filter(slug=slug).exists()
        if exists:
            slug = f"{main_slug}-{count}"
            count += 1
        else:
            return slug


def pre_save_post_signal_receiver(sender, instance, *args, **kwargs):
    instance.slug = create_slug(instance)



pre_save.connect(pre_save_post_signal_receiver, sender=Post)