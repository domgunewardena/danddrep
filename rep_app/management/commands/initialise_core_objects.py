from django.core.management.base import BaseCommand, CommandError
from django.contrib.auth.models import User
from rep_app.models import Manager, OpsDirector, Restaurant, Note
from rep_app.restaurant_list import restaurant_dict

class Command(BaseCommand):
    
    help = 'Create all restaurant, manager and ops director objects'
    
    def handle(self, *args, **options):

        ops_directors = {
            'michaelf@danddlondon.com':'Michael Farquhar',
            'jb@danddlondon.com':'JB Requien',
            'sharonw@danddlondon.com':'Sharon Whiston'
        }
        
        try:

            for email,name in ops_directors.items():

                director_user = User.objects.create_user(email, email, 'restaurant123')

                director_user.first_name = name.split(' ')[0]
                director_user.last_name = name.split(' ')[1]
                director_user.save()

                self.stdout.write(self.style.SUCCESS('User successfully created: ' + name))

                director = OpsDirector.objects.create(user=director_user)
                director.save()

                self.stdout.write(self.style.SUCCESS('Director successfully created: ' + name))

            for key, value in restaurant_dict.items():

                director_user = User.objects.filter(username=value['director'])[0]
                director = OpsDirector.objects.filter(user=director_user)[0]

                manager_email = value['manager']['email']
                manager_fname = value['manager']['name'].split(' ')[0]
                manager_lname = value['manager']['name'].split(' ')[1]
                manager_user = User.objects.create_user(manager_email, manager_email, 'restaurant123')
                manager_user.first_name = manager_fname
                manager_user.last_name = manager_lname
                manager_user.save()

                self.stdout.write(self.style.SUCCESS('User successfully created: ' + value['manager']['name']))

                manager = Manager.objects.create(user=manager_user)
                manager.save()

                self.stdout.write(self.style.SUCCESS('Manager successfully created: ' + value['manager']['name']))

                restaurant = Restaurant.objects.create(name=key,opsdirector=director,manager=manager)
                restaurant.save()

                self.stdout.write(self.style.SUCCESS('Restaurant successfully created: ' + key))
                
                note = Note.objects.create(restaurant=restaurant,text='')
                note.save()
                
                self.stdout.write(self.style.SUCCESS('Note successfully created: ' + key))
                
        except Exception as err:
            
            self.stdout.write(self.style.ERROR('Error when creating reviews: ' + str(err)))
            
            return
            
        self.stdout.write(self.style.SUCCESS('All core objects successfully created'))
        
        return