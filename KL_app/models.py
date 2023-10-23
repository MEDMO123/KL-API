from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db import transaction
from rest_framework.response import Response

class User(AbstractUser):
    adresse=models.CharField(max_length=100)
    telephone=models.CharField(max_length=10)
    def __str__(self):
         return self.username
    
class Collection(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)  
    date_updated = models.DateTimeField(auto_now=True) 
    nom_collection=models.CharField(max_length=100)
    Description=models.CharField(max_length=250,blank=True)
    active=models.BooleanField(default=False)
    def __str__(self):
        return self.nom_collection

class Modele(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.CASCADE,related_name='modeles')    
    img_modele=models.ImageField(upload_to='media')
    genre=models.CharField(max_length=5)
    nom_modele=models.CharField(max_length=100)
    description =models.CharField(max_length=250)
    prix=models.IntegerField(default=0)
    disponible=models.BooleanField(default=False)    
    def __str__(self):
        return self.nom_modele
    
    @transaction.atomic   
    def commander(self,request):
        modele = self.get_object()
        taille =self.request.data.get('taille', None)

        if not taille:
            return Response({'message': 'Veuillez spécifier la taille de la tenue pour passer une commande.'}, status=status.HTTP_400_BAD_REQUEST)
       
        Commandemodele(modele=modele, taille=taille, client=request.user).save()
        # Vous pouvez renvoyer une réponse de confirmation
        return Response({'message': 'La commande a été passée avec succès.'}, status=status.HTTP_201_CREATED)
    


class Accessoire(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)
    collection=models.ForeignKey(Collection,on_delete=models.CASCADE,related_name='accessoires')    
    nom_accessoire=models.CharField(max_length=100)   
    img_accessoire=models.ImageField(upload_to='media')  
    genre=models.CharField(max_length=5) 
    description =models.CharField(max_length=250)
    prix=models.IntegerField(default=0)
    disponible=models.BooleanField(default=False)
    def __str__(self):
        return self.nom_accessoire  

class Commandemodele (models.Model):
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    modele=models.ForeignKey(Modele,on_delete=models.CASCADE)  
    date_cmd=models.DateTimeField(auto_now=True)       
    taille=models.CharField(max_length=5)
    reception=models.CharField(max_length=30)
    confirme=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date_cmd}_{self.client.username}_{self.confirme}"

class Commandeaccessoire (models.Model):
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    accessoire=models.ForeignKey(Accessoire,on_delete=models.CASCADE)
    date_cmd=models.DateTimeField(auto_now=True)
    reception=models.CharField(max_length=30)    
    confirme=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date_cmd}_{self.client.username}_{self.confirme}"
 