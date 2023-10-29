from django.db import models

class Database(models.Model):
    food = models.CharField(max_length = 200)
    
    def __str__(self):
        return self.name
    
class Item(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    text = models.CharField(max_length = 200)
    complete = models.BooleanField()
    
    def __str__(self):
        return self.name