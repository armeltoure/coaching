from django.contrib import admin

# Register your models here.

from .models import Ticket,Produit,Commande

admin.site.register(Ticket)


@admin.register(Produit)
class ProduitAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prix', 'description')
    
@admin.register(Commande)
class CommandeAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenoms', 'numero','quantite','code_produit','nom_produit','lieu_livraison')    
