from django.db import models

# Create your models here.
class Person(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    age = models.PositiveIntegerField()
    email = models.EmailField()
    phone_number = models.CharField(max_length=20)
    relationship_status = models.CharField(max_length=30)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Preference(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='preference')
    birthday = models.CharField(max_length=20)
    favorite_flower = models.CharField(max_length=50)
    favorite_movie_genre = models.CharField(max_length=50)
    favorite_food = models.CharField(max_length=50)
    pet_name = models.CharField(max_length=100)

    def __str__(self):
        return f"Preferences of {self.person}"

class Availability(models.Model):
    person = models.ForeignKey(Person, on_delete=models.CASCADE, related_name='availability')
    date_available = models.CharField(max_length=20)

    def __str__(self):
        return f"Availability of {self.person}"