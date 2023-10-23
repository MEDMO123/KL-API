from rest_framework.serializers import ModelSerializer,SerializerMethodField 
from KL_app.models import *

#Serializers pour les modeles
class ModeleSerializer(ModelSerializer):
    class Meta:
        model=Modele
        fields=['id','img_modele','nom_modele','genre','description','prix','disponible','collection']

#Serializers pour les accessoires
class AccessoireSerializer(ModelSerializer):
    class Meta:
        model=Accessoire
        fields=['id','img_accessoire','nom_accessoire','genre','description','prix','disponible','collection']

#Serializers pour les collections 
class ColllectionSerializer(ModelSerializer):   
    class Meta:
        model=Collection
        fields=['id','nom_collection','Description','active']

#Serializers pour les collections details
class ColllectionDetailSerializer(ModelSerializer):
    modeles=SerializerMethodField()
    accessoires=SerializerMethodField()
    class Meta:
        model=Collection
        fields=['id','nom_collection','Description','active','modeles','accessoires']

        def get_modeles(self,instance):
            queryset=instance.modeles.filter(disponible=True)
            serializer=ModeleSerializer(queryset,many=True)
            return serializer.data

        def get_accessoires(self,instance):
            queryset=instance.accessoires.filter(disponible=True)
            serializer=AccessoireSerializer(queryset,many=True)
            return serializer.data
        
#Serializers pour les commandes modeles
class CmdModeleSerializer(ModeleSerializer):
    class Meta:
        model=Commandemodele
        fields=['id','date_cmd','modele','taille','reception','confirme','client']

#Serializers pour les commandes accessoires
class CmdAccessoireSerializer(ModeleSerializer):
    class Meta:
        model=Commandeaccessoire
        fields=['id','date_cmd','accessoire','reception','confirme','client']