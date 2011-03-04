from django.core.management.base import BaseCommand, CommandError
from placeholders import *

class Scaffolder():
  
  def __init__(self, app , model_instances):
    self.app = app
    self.model_instances = model_instances
    
    self.scaffold()
  
  def scaffold(self):
    self.generate_forms()
    self.generate_urls()
    self.generate_views()
    self.generate_templates()
  


  def generate_urls(self):
    
    # All the libraries needed for the url config file
    urls = URL_IMPORTS

    # Generate CRUD urls for each model
    
    for model_instance in self.model_instances:
      urls += URL_CRUD_CONFIG % {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name } 
    
    # Previous line should be written in a better way
    
    urls += ")"
    
    # write to urls.py
    print urls
    



  def generate_views(self):
    # all the imports needed views
    views_content = VIEWS_IMPORTS
    
    for model_instance in self.model_instances:
      views_content += VIEWS_CREATE 
      views_content += VIEWS_LIST
      views_content += VIEWS_VIEW
      views_content += VIEWS_UPDATE

      views_content = views_content %  {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name, 'app': self.app } 
    
    print views_content
    
    
    
  def generate_templates(self):
    for model_instance in self.model_instances:
      print TEMPLATES_CREATE  %  { 'modelClass' : model_instance._meta.object_name }
      print TEMPLATES_LIST  %  { 'modelClass' : model_instance._meta.object_name }    
      print TEMPLATES_EDIT  %  { 'modelClass' : model_instance._meta.object_name } 
      print TEMPLATES_VIEW  %  { 'modelClass' : model_instance._meta.object_name,  'model' : model_instance._meta.object_name.lower() }       
    
  def generate_forms(self):
    
    forms_content = FORMS_IMPORTS
    for model_instance in self.model_instances:
      forms_content += FORMS_MODELFORM_CONFIG % { 'modelClass' : model_instance._meta.object_name }

    print forms_content
    
    
class Command(BaseCommand):

  def handle(self, *args, **options):
    "Usage : manage.py groundwork <app> <model>"
    
    try:
      app = args[0] # App name is the first parameter
      
      model_names = args[1:] # Models which need to be scaffolded will follow
      
      exec( "from %s.models import *" %(app) )

      model_instances = [ eval(x) for x in model_names]
      
      Scaffolder(app, model_instances)
    
    except:
      print "Usage : manage.py groundwork <app> <model>"

