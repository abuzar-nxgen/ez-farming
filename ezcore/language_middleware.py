from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from django.conf import settings
from .models import User



class LanguageMiddleware(MiddlewareMixin):
    """
    Middleware to set the language based on user preferences or request headers.
    """
    
    def process_request(self, request):
        """
        Process the request and set the language based on:
        1. Language parameter in the request
        2. User's preferred language (if authenticated)
        3. Accept-Language header
        4. Default language from settings
        """
        # Check for language parameter in the request
        language = request.GET.get('lang')
        
        # If no language parameter, check authenticated user's preference
        if not language and request.user.is_authenticated:
            try:
                language = request.user.preferred_language
            except AttributeError:
                pass
        
        # If still no language, use the default
        if not language:
            language = settings.LANGUAGE_CODE
        
        # Ensure the language is supported
        if language not in [lang_code for lang_code, lang_name in settings.LANGUAGES]:
            language = settings.LANGUAGE_CODE
        
        # Set the language for this request
        translation.activate(language)
        request.LANGUAGE_CODE = language
        
        return None
    
    def process_response(self, request, response):
        """
        Add Content-Language header to the response.
        """
        response['Content-Language'] = translation.get_language()
        return response
