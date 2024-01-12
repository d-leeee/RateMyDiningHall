from django.db import models

class Database(models.Model):
    name = models.CharField(max_length=50)
    stars =  models.IntegerField(max_length=50)
    review =  models.CharField(max_length=600)
    food_name = models.CharField(max_length=600)
    
    class Meta:
        db_table = "reviews"
        
class Item(models.Model):
    database = models.ForeignKey(Database, on_delete=models.CASCADE)
    text = models.CharField(max_length = 200)
    complete = models.BooleanField()
    
    def __str__(self):
        return self.name