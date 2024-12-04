from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=255,db_index=True)
    def __str__(self):
        return self.title



class MenuItems(models.Model):
    title = models.CharField(max_length=255,db_index=True)
    price = models.DecimalField(max_digits=6,decimal_places=2,db_index=True)
    featured = models.BooleanField(db_index=True)
    category = models.ForeignKey(Category,on_delete=models.PROTECT)
    def __str__(self):
        return self.title


class Card(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    menuitem = models.ForeignKey(MenuItems,on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together = ('menuitem','user')


class Order(models.Model):
    user = models.ForeignKey(User,on_delete=models.PROTECT)
    delivery_crew = models.ForeignKey(User,on_delete=models.SET_NULL,related_name="delivery_crew",null=True)
    status = models.BooleanField(db_index=True,default=0)
    total= models.DecimalField(max_digits=6,decimal_places=2)
    date = models.DateField(db_index=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order,on_delete=models.PROTECT)
    menuitem = models.ForeignKey(MenuItems,on_delete=models.PROTECT)
    quantity = models.SmallIntegerField()
    unit_price = models.DecimalField(max_digits=6,decimal_places=2)
    price = models.DecimalField(max_digits=6,decimal_places=2)

    class Meta:
        unique_together = ('order','menuitem')

