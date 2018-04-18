from django.contrib.auth import login, authenticate
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect

# Create your views here.
from django.views.generic import TemplateView


class AuthView(TemplateView):
    template_name = 'auth.html'

    def post(self, request: HttpRequest) -> HttpResponse:
        user = authenticate(username=request.POST['login'], password=request.POST['password'])
        if user is not None:
            # the password verified for the user
            if user.is_active:
                login(request, user )
                return redirect('/main/', permanent=True)
            else:
                return redirect('/auth/', permanent=True)
        else:
            # the authentication system was unable to verify the username and password
            return redirect('/auth/', permanent=True)


class IndexView(TemplateView):
    template_name = 'index.html'

    def get(self, request: HttpRequest, **kwargs) -> HttpResponse:
        if request.user.is_active:
            return redirect('/main/', permanent=True)
        else:
            return redirect('/auth/', permanent=True)


class RegView(TemplateView):
    template_name = 'reg.html'


class MainView(TemplateView):
    template_name = 'main.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_active:
            return self.render_to_response({})
            #user = User.objects.filter(id=request.user.id)
            #references = Reference.objects.filter(user=user[0]).all()
            #return self.render_to_response({'references': references, user: user, })
        else:
            return redirect('/main/', permanent=True)
