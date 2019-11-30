# -*- coding: utf-8 -*-
# Context processors

__author__ = 'Flavien-hugs <contact@unsta.ci>'
__version__= '0.0.1'
__copyright__ = '© 2019 unsta'

from blogging import settings
from blog.models import Categorie

def blogging(request):
    return {
        'site_name': settings.SITE_NAME,
        'site_desc': settings.SITE_DECRIPTION,
        'meta_keywords': settings.META_KEYWORDS,
        'meta_description': settings.META_DESCRIPTION,
        'request': request
    }
