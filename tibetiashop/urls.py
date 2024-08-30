from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('category/', views.category, name='category'),
    path('about/', views.about, name='about'),
    path('relooking/', views.relooking, name='relooking'),
    path('contact/', views.contact, name='contact'),
    path('boutique/', views.boutique, name='boutique'),
    path('billetterie/', views.ticket_view, name='ticket_view'),
    path('reservations/', views.reservation_list, name='reservation'),
    path('confirm_reservation/<int:reservation_id>/', views.confirm_reservation, name='confirm_reservation'),
    path('ticket-booking/', views.ticket_view, name='ticket_view'),  # This is the key line
    path('acheter/<int:produit_id>/', views.acheter, name='acheter'),
    path('valider_commande/', views.valider_commande, name='valider_commande'),
    path('confirmation_commande/<int:commande_id>/', views.confirmation_commande, name='confirmation_commande'),
    path('commandes/', views.liste_commandes, name='liste_commandes'),
    path('update_status/<int:id>/<str:next_status>/', views.update_status, name='update_status'),
    path('delete_command/<int:id>/', views.delete_command, name='delete_command'),
    path('tarifs/', views.tarifs, name='tarifs'),
    path('formulaire-rendezvous/', views.formulaire_rendezvous, name='formulaire_rendezvous'),
    


    
]
