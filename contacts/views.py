import csv
from django.shortcuts import get_object_or_404, redirect, render
from contacts.models import Person, Preference, Availability
from django.contrib import messages
from django.http import HttpResponse
from datetime import datetime

#For photo import
import os
from django.core.files import File

# Create your views here.
def contact(request):
    persons = Person.objects.all()
    if request.method == 'POST':
        if 'delete_all' in request.POST:
            Person.objects.all().delete()
            return redirect('contact')
        elif 'delete_selected' in request.POST:
            ids = request.POST.getlist('selected')
            Person.objects.filter(id__in=ids).delete()
            return redirect('contact')
        # ... handle other POST actions ...
    persons = Person.objects.all()
    return render(request, 'contacts/contact.html', {'persons': persons})

def import_csv(request):
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        decoded_file = csv_file.read().decode('utf-8').splitlines()
        reader = csv.DictReader(decoded_file)
        imported = 0
        image_base_path = os.path.expanduser('~/Downloads/girls/')
        
        for row in reader:
            # Handle photo import
            photo_file = None
            photo_path = row.get('photo_path', '').strip()
            print("photo_path",photo_path)
            if photo_path:
                full_photo_path = photo_path
                # If not absolute, join with base path
                if not os.path.isabs(photo_path):
                    full_photo_path = os.path.join(image_base_path, photo_path)
                    print(full_photo_path)
                if os.path.exists(full_photo_path):
                    photo_file = File(open(full_photo_path, 'rb'), name=os.path.basename(full_photo_path))
            
            # Create or update Person
            person, created = Person.objects.get_or_create(
                first_name=row['first_name'],
                last_name=row['last_name'],
                defaults={
                    'age': row['age'],
                    'email': row['email'],
                    'phone_number': row['phone_number'],
                    'relationship_status': row['relationship_status'],
                }
            )
            
            # If updating, update fields and photo if provided
            if not created:
                person.age = row['age']
                person.email = row['email']
                person.phone_number = row['phone_number']
                person.relationship_status = row['relationship_status']
            if photo_file:
                # Delete old photo if exists and filename is the same
                if person.photo and person.photo.name != photo_file.name:
                    person.photo.delete(save=False)
                person.photo.save(os.path.basename(photo_file.name), photo_file, save=False)
            person.save()
            
            # Create or update Preference
            Preference.objects.update_or_create(
                person=person,
                defaults={
                    'birthday': row['birthday'],
                    'favorite_flower': row['favorite_flower'],
                    'favorite_movie_genre': row['favorite_movie_genre'],
                    'favorite_food': row['favorite_food'],
                    'pet_name': row['pet_name'],
                }
            )
            # Create or update Availability
            Availability.objects.update_or_create(
                person=person,
                defaults={
                    'date_available': row['date_available'],
                }
            )
            imported += 1
        messages.success(request, f"Imported {imported} contacts.")
        return redirect('contact')
    return render(request, 'contacts/import_csv.html')

def export_csv(request):
    # Create the HttpResponse object with the appropriate CSV header.
    response = HttpResponse(content_type='text/csv')
    filename = f'contacts_{datetime.now().strftime("%Y%m%d_%H%M%s")}.csv'
    response['Content-Disposition'] = f'attachment; filename="{filename}"'
    
    writer = csv.writer(response)
    # Write header
    writer.writerow([
        'first_name', 'last_name', 'age', 'email', 'phone_number', 'relationship_status',
        'photo_path',
        'birthday', 'favorite_flower', 'favorite_movie_genre', 'favorite_food', 'pet_name',
        'date_available'
    ])
    
    for person in Person.objects.all():
        preference = person.preference.first()
        availability = person.availability.first()
        # Get the photo filename if it exists, else empty string
        photo_path = os.path.basename(person.photo.name) if person.photo and person.photo.name else ''
        writer.writerow([
            person.first_name,
            person.last_name,
            person.age,
            person.email,
            person.phone_number,
            person.relationship_status,
            photo_path,
            preference.birthday if preference else '',
            preference.favorite_flower if preference else '',
            preference.favorite_movie_genre if preference else '',
            preference.favorite_food if preference else '',
            preference.pet_name if preference else '',
            availability.date_available if availability else '',
        ])
    return response        
    
def add_record(request):
    if request.method == 'POST':
        photo = request.FILES.get('photo')
        person = Person.objects.create(
            first_name=request.POST['first_name'],
            last_name=request.POST['last_name'],
            age=request.POST['age'],
            email=request.POST['email'],
            phone_number=request.POST['phone_number'],
            relationship_status=request.POST['relationship_status'],
            photo=photo
        )
        Preference.objects.create(
            person=person,
            birthday=request.POST['birthday'],
            favorite_flower=request.POST['favorite_flower'],
            favorite_movie_genre=request.POST['favorite_movie_genre'],
            favorite_food=request.POST['favorite_food'],
            pet_name=request.POST['pet_name']
        )
        Availability.objects.create(
            person=person,
            date_available=request.POST['date_available']
        )
        return redirect('contact')
    return render(request, 'contacts/add_record.html')

def edit_record(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    preference = person.preference.first()
    availability = person.availability.first()
    if request.method == 'POST':
        person.first_name = request.POST['first_name']
        person.last_name = request.POST['last_name']
        person.age = request.POST['age']
        person.email = request.POST['email']
        person.phone_number = request.POST['phone_number']
        person.relationship_status = request.POST['relationship_status']
        if request.FILES.get('photo'):
            person.photo = request.FILES['photo']
        person.save()
        # Update preference
        if preference:
            preference.birthday = request.POST['birthday']
            preference.favorite_flower = request.POST['favorite_flower']
            preference.favorite_movie_genre = request.POST['favorite_movie_genre']
            preference.favorite_food = request.POST['favorite_food']
            preference.pet_name = request.POST['pet_name']
            preference.save()
        # Update availability
        if availability:
            availability.date_available = request.POST['date_available']
            availability.save()
        return redirect('contact')
    #Update fail, reload edit page
    return render(request, 'contacts/edit_record.html', {
        'person': person,
        'preference': preference,
        'availability': availability,
    })

def delete_record(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    return redirect('contact')
    
def preference(request, person_id):
    preference = get_object_or_404(Preference, person_id=person_id)
    return render(request, 'contacts/preference.html', {'preference': preference})

def availability(request, person_id):
    availability = get_object_or_404(Availability, person_id=person_id)
    return render(request, 'contacts/availability.html', {'availability': availability})