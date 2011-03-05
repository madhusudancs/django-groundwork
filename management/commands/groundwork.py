from django.core.management.base import BaseCommand, CommandError
from placeholders import *
import os

class Scaffolder():
  
  def __init__(self, app , model_instances):
    self.app = app
    self.model_instances = model_instances
    self.PROJECT_ROOT = os.path.abspath( os.path.join(os.path.dirname(__file__) , "..", "..", ".."))
    self.TEMPLATE_DIR = os.path.join ( self.PROJECT_ROOT , 'templates')
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
    urlpath = os.path.join (self.PROJECT_ROOT, self.app, 'urls.py')
#    with open( urlpath, 'w') as f:
#      f.write(urls)
    print "URL Config has been written to %s. \n\nAdd the following line to %s" % (urlpath, os.path.join (self.PROJECT_ROOT, 'urls.py'))
    print "(r'^%(app)s/', include('%(app)s.urls'))," % {'app': self.app }



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
    # write to views.py
    viewspath = os.path.join (self.PROJECT_ROOT, self.app, 'views.py')
#    with open( viewspath , 'w') as f:
#      f.write(views_content)
    print "Views written to %s" % (viewspath)

    
    
    
  def generate_templates(self):
    os.mkdir( os.path.join(self.TEMPLATE_DIR, self.app ) )
    
    for model_instance in self.model_instances:
      with  open(os.path.join( self.TEMPLATE_DIR, self.app, 'create_%s' % (model_instance._meta.object_name.lower()) ) ) as f:
        f.write( TEMPLATES_CREATE  %  { 'modelClass' : model_instance._meta.object_name } )
      with  open(os.path.join( self.TEMPLATE_DIR, self.app, 'list_%s' % (model_instance._meta.object_name.lower()) ) ) as f:
        f.write( TEMPLATES_LIST  %  { 'modelClass' : model_instance._meta.object_name } )
      with  open(os.path.join( self.TEMPLATE_DIR, self.app, 'edit_%s' % (model_instance._meta.object_name.lower()) ) ) as f:
        f.write( TEMPLATES_EDIT  %  { 'modelClass' : model_instance._meta.object_name } )
      with  open(os.path.join( self.TEMPLATE_DIR, self.app, 'view_%s' % (model_instance._meta.object_name.lower()) ) ) as f:
        f.write( TEMPLATES_VIEW  %  { 'modelClass' : model_instance._meta.object_name,  'model' : model_instance._meta.object_name.lower()} )

      
  def generate_forms(self):
    
    forms_content = FORMS_IMPORTS
    for model_instance in self.model_instances:
      forms_content += FORMS_MODELFORM_CONFIG % { 'modelClass' : model_instance._meta.object_name }

    print forms_content
    formspath = os.path.join (self.PROJECT_ROOT, self.app, 'forms.py')
#    with open( formspath , 'w') as f:
#      f.write(forms_content)
    print "Forms written to %s" % (formspath)
    
    
class Command(BaseCommand):

  def handle(self, *args, **options):
    "Usage : manage.py groundwork <app> <model>"
    
#    try:
    app = args[0] # App name is the first parameter
    
    model_names = args[1:] # Models which need to be scaffolded will follow
    
    exec( "from %s.models import *" %(app) )

    model_instances = [ eval(x) for x in model_names]
    
    Scaffolder(app, model_instances)
  
#    except:
    print "Usage : manage.py groundwork <app> <model>"

