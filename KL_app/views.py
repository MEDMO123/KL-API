from rest_framework.viewsets import ModelViewSet,ReadOnlyModelViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from KL_app.models import *
from KL_app.serializers import *

##########################_ViewSets Admin_##################################################

#Viewset pour les collections
class AdminCollectionViewSet(ModelViewSet):
    serializer_class=ColllectionSerializer
    detail_serializer_class=ColllectionDetailSerializer  
   

    def get_queryset(self):    
        return Collection.objects.filter(active=True)        
    def get_serializer_class(self):
        if self.action=='retrieve':
            return self.detail_serializer_class
        return self.serializer_class   

#Viewset pour les modeleles
class CmdModeleViewset(ModelViewSet):
    serializer_class=CmdModeleSerializer
    queryset=Commandemodele.objects.all()

class CmdAccessoireViewset(ModelViewSet):
    serializer_class=CmdAccessoireSerializer
    queryset=Commandeaccessoire.objects.all()    

##########################_ViewSets utilisateur_##################################################

#Viewset pour les collections
class CollectionViewSet(ReadOnlyModelViewSet):
    serializer_class=ColllectionSerializer
    detail_serializer_class=ColllectionDetailSerializer  
    # permission_classes=[IsAuthenticated]

    def get_queryset(self):    
        return Collection.objects.filter(active=True)        
    def get_serializer_class(self):
        if self.action=='retrieve':
            return self.detail_serializer_class
        return self.serializer_class

   
#Viewset pour la liste des modeles
class ModeleListViewSet(ReadOnlyModelViewSet):
    serializer_class=ModeleSerializer
    def get_queryset(self):
       queryset=Modele.objects.filter(disponible=True)
       collection_id=self.request.GET.get('collection_id')
       if collection_id:
          queryset=queryset.filter(collection_id=collection_id)
       return queryset
        


#Viewset pour la liste des Accessoires
class AccessoireListViewSet(ReadOnlyModelViewSet):
    serializer_class=AccessoireSerializer
    def get_queryset(self):
       queryset=Accessoire.objects.filter(disponible=True)
       collection_id=self.request.GET.get('collection_id')
       if collection_id:
          queryset=queryset.filter(collection_id=collection_id)
       return queryset
        

#Viewset pour les Commandes modeles
class ModeleViewSet(ModelViewSet):
    queryset = Modele.objects.filter(disponible=True)
    serializer_class = ModeleSerializer
    permission_classes=[IsAuthenticated]

  
    @action(detail=True, methods=['POST'])
    def commander(self, request, pk=None):
        modele = self.get_object()
        taille = request.data.get('taille', None)
        reception=request.data.get('reception', None)

        if not taille:
            return Response({'message': 'Veuillez spécifier la taille de la tenue pour passer une commande.'})
       
        Commandemodele(modele=modele, taille=taille, reception=reception,client=request.user).save()
        # Vous pouvez renvoyer une réponse de confirmation
        return Response({'message': 'La commande a été passée avec succès.'})
    
    
#Viewset pour les Commandes accessoires   
class AccessoireViewSet(ModelViewSet):
    queryset = Accessoire.objects.filter(disponible=True)
    serializer_class = AccessoireSerializer
    permission_classes=[IsAuthenticated]

    @action(detail=True, methods=['POST'])
    def commander(self, request, pk=None):
        accessoire = self.get_object()    

        commande_accessoire = Commandeaccessoire(accessoire=accessoire,client=request.user)
        commande_accessoire.save()
    
        return Response({'message': 'La commande a été passée avec succès.'}, status=status.HTTP_201_CREATED)
    
