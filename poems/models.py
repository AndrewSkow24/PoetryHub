from django.db import models
from django.contrib.auth.models import User


class PoemTag(models.Model):
    name = models.CharField(max_length=50, unique=True, verbose_name="Название тега")
    color = models.CharField(
        max_length=7,
        default="#6c757d",
        verbose_name="Цвет тега",
        help_text="Цвет тега в hex-формате (#ffffff)",
    )


class PoemLike(models.Model):
    poem = models.ForeignKey("Poem", on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ["poem", "user"]
        verbose_name = "Лайк"
        verbose_name_plural = "Лайки"

    def __str__(self):
        return f"Like by {self.user} to {self.poem}"


class Poem(models.Model):
    title = models.CharField(
        max_length=255, verbose_name="Название", help_text="Название"
    )
    content = models.TextField(verbose_name="Содержание", help_text="Содержание")
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, verbose_name="Автор", help_text="Автор"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Дата и время создания",
        help_text="Дата и время создания",
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Дата и время обновления",
        help_text="Дата и время обновления",
    )

    is_published = models.BooleanField(
        default=True,
        verbose_name="Опубликовано",
        help_text="Отображать ли произведение на сайте",
    )

    tags = models.ManyToManyField(
        PoemTag, blank=True, verbose_name="Теги", help_text="Теги"
    )

    class Meta:
        verbose_name = "Стихотворение"
        verbose_name_plural = "Стихотворения"
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.title} ({self.author})"

    # метод получения количества лайков
    @property
    def likes_count(self):
        return self.likes.count()  # likes is a related name

    # метод проверки сделал ли пользователь лайк
    def is_liked_by_user(self, user):
        if user.is_authenticated:
            return self.likes.filter(user=user).exists()
        return False

    # метод для добавления или удаления лайка
    def toggle_like(self, user):
        if not user.is_authenticated:
            return False

        like, created = PoemLike.objects.get_or_create(
            poem=self,
            user=user,
        )

        if not created:
            like.delete()
            return False  # лайк удалён
        return True  # лайк добавлен
