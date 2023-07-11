from django.db import models

STATUS_CHOICES = (
    ('Active', "Active"),
    ('Inactive', "Inactive"),
    ('Overdue', 'Overdue')
)


# Create your models here.
class Card(models.Model):
    series = models.CharField(max_length=3)
    number = models.PositiveBigIntegerField()
    release_date = models.DateTimeField()
    end_date = models.DateTimeField()
    cvv = models.CharField(max_length=3)
    funds = models.CharField(max_length=100)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES)

    def __str__(self):
        return str(self.number)


class Purchase(models.Model):
    title = models.CharField(max_length=50)
    price = models.IntegerField()
    address = models.CharField(max_length=50)
    card = models.ForeignKey('Card', on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.card} -> {self.title}"
