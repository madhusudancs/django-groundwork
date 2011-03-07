from django.core.management.base import BaseCommand, CommandError
from django.db import models
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
        self.display_messages()


    def display_messages(self):
        print "Configure your settings.py with the desired database and execute manage.py syncdb"
        print "Add your new app to the list of installed apps in settings.py"

    def generate_urls(self):
    
        # All the libraries needed for the url config file
        urls = URL_IMPORTS

        # Generate CRUD urls for each model

        for model_instance in self.model_instances:
            urls += URL_CRUD_CONFIG % {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name } 

        # Previous line should be written in a better way

        urls += URL_END

        # write to urls.py
        urlpath = os.path.join (self.PROJECT_ROOT , self.app, 'urls.py')
        f = open( urlpath , 'w')
        f.write(urls)
        f.close()
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

        # write to views.py
        viewspath = os.path.join (self.PROJECT_ROOT, self.app, 'views.py')
        f = open( viewspath, 'w')
        f.write(views_content)
        f.close()
        
        print "Views written to %s" % (viewspath)

    
    
    
    def generate_templates(self):
        template_dir = os.path.join(self.TEMPLATE_DIR, self.app )
        if not os.path.exists(template_dir):
            os.makedirs(template_dir)
        
        print "Generate base template? [Y/N]?"
        yn = raw_input()
        if yn.lower() == 'y':
            f = open(os.path.join(self.TEMPLATE_DIR, 'base.html') , 'w')
            f.write(TEMPLATES_BASE % {})
            f.close()
            
        for model_instance in self.model_instances:
            f = open(os.path.join( self.TEMPLATE_DIR, self.app, 'create_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w')
            f.write( TEMPLATES_CREATE  %  { 'modelClass' : model_instance._meta.object_name } )
            f.close()
            
            f = open(os.path.join( self.TEMPLATE_DIR, self.app, 'list_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w')
            f.write( TEMPLATES_LIST  %  { 'modelClass' : model_instance._meta.object_name } )
            f.close()
            
            f = open(os.path.join( self.TEMPLATE_DIR, self.app, 'edit_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w') 
            f.write( TEMPLATES_EDIT  %  { 'modelClass' : model_instance._meta.object_name } )
            f.close()
            
            f = open(os.path.join( self.TEMPLATE_DIR, self.app, 'view_%s.html' % (model_instance._meta.object_name.lower()) ) , 'w')
            f.write( TEMPLATES_VIEW  %  { 'modelClass' : model_instance._meta.object_name,  'model' : model_instance._meta.object_name.lower()} )
            f.close()

      
    def generate_forms(self):

        forms_content = FORMS_IMPORTS
        for model_instance in self.model_instances:
            forms_content += FORMS_MODELFORM_CONFIG % { 'modelClass' : model_instance._meta.object_name }

        formspath = os.path.join (self.PROJECT_ROOT, self.app, 'forms.py')
        f = open( formspath , 'w')
        f.write(forms_content)
        f.close()
        print "Forms written to %s" % (formspath)
    
    
class Command(BaseCommand):

    def handle(self, *args, **options):
        "Usage : manage.py groundwork <app> <model>"

        try:
            app = args[0] # App name is the first parameter

            model_names = args[1:] # Models which need to be scaffolded will follow

            model_instances = [ models.get_model(app, x) for x in model_names ]
    
            Scaffolder(app, model_instances)

        except:
            print "Usage : manage.py groundwork <app> <model>"

