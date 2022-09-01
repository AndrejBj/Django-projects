from django.db import models

class Drinks(models.Model):                        #svaka klasa koju pravimo mora biti izvedena iz modela
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=500)

    def __str__(self):                             #kad napravimo objekat u tabeli drinks, ispisace imena tih objekata, a ne samo objekat 1/objekat 2...
        return self.name+" "+self.description


class Food(models.Model):                          #pravimo drugi model Food
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=500)

    def __str__(self):                           
        return self.name+" "+self.description
        

class Alcohol(models.Model):                          
    name=models.CharField(max_length=200)
    description=models.CharField(max_length=500)

    def __str__(self):                           
        return self.name+" "+self.description