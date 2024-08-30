from django.core.mail import send_mail
from django.conf import settings
from .forms import TicketForm
from .models import Ticket
from django.shortcuts import render, redirect, get_object_or_404
from .utils import send_sms
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import Commande,Produit
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, 'titi/home.html')
    
# views.py
def formulaire_rendezvous(request):
    return render(request, 'titi/formulaire_rendezvous.html')

def tarifs(request):
    return render(request, 'titi/tarifs.html')

def boutique(request):
    produits = Produit.objects.all()
    return render(request, 'titi/boutique.html', {'produits': produits})

def relooking(request):
    return render(request,'titi/relooking.html')
   

def category(request):
    return render(request,'titi/category.html')

def about(request):
    return render(request,'titi/about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')

        # Compose the email message
        full_message = f"Message from {name} ({email}):\n\n{message}"
        
        # Send the email
        send_mail(
            subject,
            full_message,
            settings.DEFAULT_FROM_EMAIL,
            ['armeltoure92@gmail.com'],  # Replace with your email
        )
        
        return redirect('contact')  # Redirect to the same page or any other page

    return render(request, 'titi/contact.html')

def reservation_list(request):
    # Récupérer les réservations triées par nom (ordre alphabétique)
    reservations = Ticket.objects.all().order_by('name')    
    # Calculer le total des tickets réservés
    total_tickets = sum(reservation.ticket_quantity for reservation in reservations)    
    return render(request, 'titi/reservation_list.html', {
        'reservations': reservations,
        'total_tickets': total_tickets
    })



def confirm_reservation(request, reservation_id):
    reservation = get_object_or_404(Ticket, id=reservation_id)
    reservation.confirmed = True
    reservation.save()

    # Récupérer et formater le numéro de téléphone
    phone_number = reservation.phone_number
    if not phone_number.startswith('+'):
        phone_number = '+225' + phone_number.lstrip('0')  # Ajouter le code du pays, si nécessaire

    # Vérifier le format du numéro de téléphone
    if len(phone_number) == 13 and phone_number.startswith('+225'):  # Vérifiez que le numéro commence par +225
        # Envoyer un SMS de confirmation
        send_sms(phone_number, f"Votre réservation pour {reservation.ticket_quantity} billets a été confirmée.")
    else:
        # Gérer les erreurs de numéro de téléphone ici
        # Par exemple, vous pourriez enregistrer une erreur dans les logs ou afficher un message d'erreur
        print("Erreur: Numéro de téléphone invalide.")

    return redirect('reservation')

import re  # noqa: E402

def ticket_view(request):
    if request.method == 'POST':
        form = TicketForm(request.POST)
        if form.is_valid():
            phone_number = form.cleaned_data['phone_number']

            # Vérifiez si le numéro de téléphone est au format +225XXXXXXXXXX
            if not re.match(r'^\+225\d{10}$', phone_number):
                form.add_error('phone_number', "Veuillez entrer un numéro de téléphone valide au format +225XXXXXXXXXX.")
            else:
                # Vérifiez si le numéro de téléphone existe déjà
                if Ticket.objects.filter(phone_number=phone_number).exists():
                    form.add_error('phone_number', 'Ce numéro de téléphone est déjà utilisé, utilisez un autre numéro de téléphone.')
                else:
                    # Enregistrer les informations dans le modèle Ticket seulement si aucune erreur n'a été ajoutée
                    if not form.errors:
                        ticket = Ticket(
                            name=form.cleaned_data['name'],
                            phone_number=phone_number,
                            email=form.cleaned_data['email'],
                            ticket_quantity=form.cleaned_data['ticket_quantity'],
                            message=form.cleaned_data['message']
                        )
                        ticket.save()
                        return render(request, 'titi/ticket_booking.html', {
                            'form': form,
                            'success': True,
                            'name': ticket.name,
                            'phone_number': ticket.phone_number,
                            'ticket_quantity': ticket.ticket_quantity
                        })
    else:
        form = TicketForm()

    return render(request, 'titi/ticket_booking.html', {'form': form})




def acheter(request, produit_id):
    produit = get_object_or_404(Produit, id=produit_id)
    
    if request.method == 'POST':
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        numero = request.POST.get('numero')
        quantite = int(request.POST.get('quantite'))
        lieu_livraison = request.POST.get('lieu_livraison')
        prix_total = produit.prix * quantite
        
        # Création et sauvegarde de la commande
        commande = Commande(
            nom=nom,
            prenoms=prenoms,
            numero=numero,
            quantite=quantite,
            lieu_livraison=lieu_livraison,
            produit=produit,
            prix_total=prix_total
        )
        commande.save()
        
        # Redirection vers la confirmation de commande avec l'identifiant de la commande
        return redirect('confirmation_commande', commande_id=commande.id)
    
    return render(request, 'titi/acheter.html', {'produit': produit})




def valider_commande(request):
    if request.method == 'POST':
        produit_id = request.POST.get('produit_id')
        produit = get_object_or_404(Produit, id=produit_id)
        nom = request.POST.get('nom')
        prenoms = request.POST.get('prenoms')
        numero = request.POST.get('numero')
        quantite = int(request.POST.get('quantite'))
        lieu_livraison = request.POST.get('lieu_livraison')
        prix_total = produit.prix * quantite
        
        # Création et sauvegarde de la commande
        commande = Commande(
            nom=nom,
            prenoms=prenoms,
            numero=numero,
            quantite=quantite,
            lieu_livraison=lieu_livraison,
            produit=produit,
            prix_total=prix_total,
            code_produit=produit.code,
            nom_produit=produit.nom 
        )
        commande.save()
        
        messages.success(request, 'Votre commande a été passée avec succès !')
        return redirect('confirmation_commande')  # Assurez-vous que cette vue existe

    return redirect('boutique')  # Redirection en cas d'erreur ou de méthode GET




def confirmation_commande(request, commande_id):
    commande = get_object_or_404(Commande, id=commande_id)
    return render(request, 'titi/confirmation_commande.html', {'commande': commande})



def liste_commandes(request):
    commandes = Commande.objects.all()
    return render(request, 'titi/liste_commandes.html', {'commandes': commandes})



@csrf_exempt
def update_status(request, id, next_status):
    try:
        commande = Commande.objects.get(id=id)
        if next_status in dict(Commande.STATUT_CHOICES):
            commande.status = next_status
            commande.save()
            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid status'})
    except Commande.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Commande not found'})



def delete_command(request, id):
    if request.method == 'POST':
        try:
            commande = Commande.objects.get(id=id)
            commande.delete()
            return JsonResponse({'success': True})
        except Commande.DoesNotExist:
            return JsonResponse({'success': False})
        
        
