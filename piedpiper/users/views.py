from rest_framework import viewsets, mixins
from rest_framework.permissions import AllowAny
from .models import User
from .permissions import IsUserOrReadOnly
from .serializers import CreateUserSerializer, UserSerializer

from rest_framework.response import Response
from rest_framework.decorators import action

from onelogin.saml2.auth import OneLogin_Saml2_Auth
from onelogin.saml2.settings import OneLogin_Saml2_Settings
from onelogin.saml2.utils import OneLogin_Saml2_Utils

class UserViewSet(mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,
                  viewsets.GenericViewSet):
    """
    Updates and retrieves user accounts
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUserOrReadOnly,)


class UserCreateViewSet(mixins.CreateModelMixin,
                        viewsets.GenericViewSet):
    """
    Creates user accounts
    """
    queryset = User.objects.all()
    serializer_class = CreateUserSerializer
    permission_classes = (AllowAny,)


class IndexViewset(viewsets.ViewSet):
    
    permission_classes = [AllowAny]

    def list(self, request):
        return Response({ 'message': 'index 1' })


class AttrsViewset(viewsets.ViewSet):
    
    permission_classes = [AllowAny]

    def list(self, request):
        return Response({ 'message': 'attrs 1' })


def init_saml_auth(req):
    auth = OneLogin_Saml2_Auth(req, custom_base_path=settings.SAML_FOLDER)
    return auth


def prepare_django_request(request):
    # If server is behind proxys or balancers use the HTTP_X_FORWARDED fields
    result = {
        'https': 'on' if request.is_secure() else 'off',
        'http_host': request.META['HTTP_HOST'],
        'script_name': request.META['PATH_INFO'],
        'server_port': request.META['SERVER_PORT'],
        'get_data': request.GET.copy(),
        # Uncomment if using ADFS as IdP, https://github.com/onelogin/python-saml/pull/144
        # 'lowercase_urlencoding': True,
        'post_data': request.POST.copy()
    }
    return result


class ACSViewset(viewsets.ViewSet):
    
    permission_classes = [AllowAny]

    @action(url_path='', methods=['post'], detail=False)
    def acs(self, request):
        req = prepare_django_request(request)
        print('\n', '-'*25)
        print('req', req)
        print('\n\n')

        auth = OneLogin_Saml2_Auth(req)
        print('\n', '-'*25)
        print('auth', auth)
        print('\n\n')


        auth.process_response()
        errors = auth.get_errors()
        print('\n', '-'*25)
        print('errors', errors)
        print('\n\n')


        if not errors:
            print('\n', '-'*25)
            print('auth.is_authenticated()', auth.is_authenticated())
            print('\n\n')

            if auth.is_authenticated():
                print('\n', '-'*25)
                print('auth.get_attributes()', auth.get_attributes())
                print('\n\n')
                
                request.session['samlUserdata'] = auth.get_attributes()
                
                print('\n', '-'*25)
                print('req[post_data]', req['post_data'])
                print('\n\n')

                print('\n', '-'*25)
                print('OneLogin_Saml2_Utils.get_self_url(req)', OneLogin_Saml2_Utils.get_self_url(req))
                print('\n\n')

                if 'RelayState' in req['post_data'] and OneLogin_Saml2_Utils.get_self_url(req) != req['post_data']['RelayState']:
                    auth.redirect_to(req['post_data']['RelayState'])
                else:
                    for attr_name in request.session['samlUserdata'].keys():
                        print('%s ==> %s' % (attr_name, '|| '.join(request.session['samlUserdata'][attr_name])))
            else:
                print('Not authenticated')
        else:
            print("Error when processing SAML Response: %s" % (', '.join(errors)))

        return Response({ 'message': 'ACS' })