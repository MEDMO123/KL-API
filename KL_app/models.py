from django.db import models
from django.contrib.auth.models import AbstractUser 
from django.db import transaction
from rest_framework.response import Response

# modele    User
class User(AbstractUser):
    adresse=models.CharField(max_length=100)
    telephone=models.CharField(max_length=10)
    def __str__(self):
         return self.username
    
#Modele Collection
class Collection(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)  
    date_updated = models.DateTimeField(auto_now=True) 
    nom_collection=models.CharField(max_length=100)
    Description=models.CharField(max_length=250,blank=True)
    active=models.BooleanField(default=False)
    def __str__(self):
        return self.nom_collection
    
#Modele Modèles
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
        reception=request.data.get('reception', None)
        if not taille:
            return Response({'message': 'Veuillez spécifier la taille de la tenue pour passer une commande.'})
       
        Commandemodele(modele=modele, taille=taille,reception=reception, client=request.user).save()
        # Vous pouvez renvoyer une réponse de confirmation
        return Response({'message': 'La commande a été passée avec succès.'})
    

#Modele Accessoires
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
        
    @transaction.atomic    
    def commander(self,request):
        accessoire = self.get_object()
        Commandeaccessoire(accessoire=accessoire,client=request.user).save()          
        return Response({'message': 'La commande a été passée avec succès.'})
    

#Modele Commande modèle
class Commandemodele (models.Model):
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    modele=models.ForeignKey(Modele,on_delete=models.CASCADE)  
    date_cmd=models.DateTimeField(auto_now=True)       
    taille=models.CharField(max_length=5)
    reception=models.CharField(max_length=30)
    confirme=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date_cmd}_{self.client.username}_{self.confirme}"
    

#Modele Commande accessoire
class Commandeaccessoire (models.Model):
    client=models.ForeignKey(User,on_delete=models.CASCADE)
    accessoire=models.ForeignKey(Accessoire,on_delete=models.CASCADE)
    date_cmd=models.DateTimeField(auto_now=True)
    reception=models.CharField(max_length=30)    
    confirme=models.BooleanField(default=False)
    def __str__(self):
        return f"{self.date_cmd}_{self.client.username}_{self.confirme}"
 