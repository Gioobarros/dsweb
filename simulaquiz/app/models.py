from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Moderator(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    profile_image = models.ImageField(upload_to='moderator_images/', null=True)
    description = models.TextField(null=True)

    def __str__(self):
        return f"(ID:{self.id}) (Username: {self.user.username})"

class Theme(models.Model):
    title = models.CharField(max_length=255)
    date_created = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ID:{self.id}) (Title: {self.title}) (Date Created: {self.date_created}) (Last Change:{self.last_change})"

class Exam(models.Model):
    theme = models.ForeignKey(Theme, on_delete=models.CASCADE)
    moderator = models.ForeignKey(Moderator, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    how_many_submissions = models.IntegerField(default=0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ID:{self.id}) (Theme ID:{self.theme.id}) (Title: {self.title}) (How Many Submissions: {self.how_many_submissions}) (Date Created: {self.date_created}) (Last Change:{self.last_change})"
    
class Question(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE)
    text = models.TextField()
    weight = models.FloatField(default=1.0)
    date_created = models.DateTimeField(auto_now_add=True)
    last_change = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return f"(ID:{self.id}) (Exam ID:{self.exam.id}) (Text: {self.text[:15]}...) (Weight: {self.weight}) (Date Created: {self.date_created}) (Last Change:{self.last_change})"

class Choices(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    text = models.TextField()
    is_correct = models.BooleanField(default=False)
    date_created = models.DateField(auto_now_add=True)
    last_change = models.DateField(auto_now=True)

def __str__(self) -> str:
    return f"(ID:{self.id}) (Question ID:{self.question.id}) (Text: {self.text[:15]}...) (Is Correct: {self.is_correct}) (Date Created: {self.date_created}) (Last Change:{self.last_change})"

