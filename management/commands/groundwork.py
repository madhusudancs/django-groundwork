from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):

  def handle(self, *args, **options):
    "Usage : manage.py groundwork <app> <model>"
    
    try:
      app = args[0] # App name is the first parameter
      
      model_names = args[1:] # Models which need to be scaffolded will follow
      
      exec( "from %s.models import *" %(app) )

      model_instances = [ eval(x) for x in model_names]
      
      #scaffold(model_instances)
      
    except:
      print "Usage : manage.py groundwork <app> <model>"
