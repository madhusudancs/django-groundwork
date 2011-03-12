from django.core.management.base import BaseCommand, CommandError
from django.db import models
from placeholders import *
import os
    
class Command(BaseCommand):

    def handle(self, *args, **options):
        "Usage : manage.py groundwork <app> <model>"

        PROJECT_ROOT = os.getcwd() 
        TEMPLATE_DIR = os.path.join ( PROJECT_ROOT , 'templates')


        try:
            app = args[0] # App name is the first parameter
            model_names = args[1:] # Models which need to be scaffolded will follow

            model_instances = [ models.get_model(app, x) for x in model_names ]

            # url config
            urls = URL_IMPORTS

            # Generate CRUD urls for each model
            for model_instance in model_instances:
                urls += URL_CRUD_CONFIG % {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name } 

            urls += URL_END

            # write to urls.py
            f = open( os.path.join (PROJECT_ROOT , app, 'urls.py') , 'w')
            f.write(urls)
            f.close()
            
            # append to root urlconf
            f = open( os.path.join (PROJECT_ROOT , 'urls.py') , 'a')
            f.write( "\nurlpatterns += patterns ('',\n (r'^%(app)s/', include('%(app)s.urls')),\n)\n" % {'app': app } )
            f.close()



            # forms
            forms_content = FORMS_IMPORTS
            for model_instance in model_instances:
                forms_content += FORMS_MODELFORM_CONFIG % { 'modelClass' : model_instance._meta.object_name }

            formspath = os.path.join (PROJECT_ROOT, app, 'forms.py')
            f = open( formspath , 'w')
            f.write(forms_content)
            f.close()


            # views
            views_content = VIEWS_IMPORTS

            for model_instance in model_instances:
                views_content += VIEWS_CREATE 
                views_content += VIEWS_LIST
                views_content += VIEWS_VIEW
                views_content += VIEWS_UPDATE
                
                views_content = views_content %  {'model':model_instance._meta.object_name.lower(), 'modelClass': model_instance._meta.object_name, 'app': app } 

            # write to views.py
            viewspath = os.path.join (PROJECT_ROOT, app, 'views.py')
            f = open( viewspath, 'w')
            f.write(views_content)
            f.close()


            # Templates
            
            template_dir = os.path.join(TEMPLATE_DIR, app )
            if not os.path.exists(template_dir):
                os.makedirs(template_dir)
            
            print "Generate base template? [Y/N]?"
            yn = raw_input()
            if yn.lower() == 'y':
                f = open(os.path.join(TEMPLATE_DIR, 'base.html') , 'w')
                f.write(TEMPLATES_BASE)
                f.close()
                
            for model_instance in model_instances:
                f = open(os.path.join( TEMPLATE_DIR, app, 'create_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w')
                f.write( TEMPLATES_CREATE  %  { 'modelClass' : model_instance._meta.object_name } )
                f.close()
                
                f = open(os.path.join( TEMPLATE_DIR, app, 'list_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w')
                f.write( TEMPLATES_LIST  %  { 'modelClass' : model_instance._meta.object_name ,'model' : model_instance._meta.object_name.lower(), 'app' : app} )
                f.close()
                
                f = open(os.path.join( TEMPLATE_DIR, app, 'edit_%s.html' % (model_instance._meta.object_name.lower()) ) ,'w') 
                f.write( TEMPLATES_EDIT  %  { 'modelClass' : model_instance._meta.object_name } )
                f.close()
                
                f = open(os.path.join( TEMPLATE_DIR, app, 'view_%s.html' % (model_instance._meta.object_name.lower()) ) , 'w')
                f.write( TEMPLATES_VIEW  %  { 'modelClass' : model_instance._meta.object_name,  'model' : model_instance._meta.object_name.lower()} )
                f.close()

            # settings
            f = open(os.path.join(PROJECT_ROOT, 'settings.py'), 'a')
            f.write( "\nimport os\nTEMPLATE_DIRS += (os.path.join(  os.path.dirname(__file__), 'templates') ,)\n")
            f.close()
                
        except:
            print "Usage : manage.py groundwork <app> <model>"

