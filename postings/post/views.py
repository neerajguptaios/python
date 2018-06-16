# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from rest_framework_jwt.settings import api_settings

def jwt_response_payload_handler(token, user=None, request=None):

   return {
       'token': token,
       'user': {
            'email': user.email,
       }
   }