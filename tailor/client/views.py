import pickle
import inspect
import urllib2
import sys
import imp
import os

from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings as djangosettings
from django.views.decorators.csrf import csrf_exempt
from django.utils import simplejson

from fabric.api import *

from fabric.main import load_fabfile, _task_names

def schema(request):
    """
    Parses the project fabfile and returns API listing
    the available commands.  Commands are made available by
    adding the @tailored decorator to a fabric function.
    """

    if request.REQUEST.get('key'):
        if request.REQUEST.get('key') in djangosettings.TAILOR_API_KEYS.values():
            fabfile_directory = os.path.dirname(djangosettings.TAILOR_FABFILE_PATH)

            # Custom importer
            importer = lambda _: imp.load_source('fabfile', os.path.join())

            sys.path.insert(0, fabfile_directory)
            os.chdir(fabfile_directory)
            _, task_map, _ = load_fabfile('/fabfile.py',
                                          importer)

            task_list = _task_names(task_map)

            fab_dict['tasks'] {
                'map'    : task_map,
                'folded' : task_list

            response = simplejson.dumps(fab_dict)
            return HttpResponse(response, mimetype='application/json', status=200)

        else:
            return HttpResponse("API Key Not Recognized", status=403)
    else:
        return HttpResponse("API Key Required", status=403)
