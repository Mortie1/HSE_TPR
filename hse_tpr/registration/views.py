from django.conf import settings
from django.contrib import messages
from django.contrib.auth import authenticate, login, REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LogoutView, PasswordChangeView
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.crypto import get_random_string
from django.utils.decorators import method_decorator
from django.utils.http import url_has_allowed_host_and_scheme as is_safe_url
from django.utils.translation import gettext_lazy as _
from django.views.decorators.cache import never_cache
from django.views.decorators.csrf import csrf_protect
from django.views.decorators.debug import sensitive_post_parameters
from django.core.mail import send_mail


from django.views.generic import FormView, TemplateView, View

from .forms import *
#TODO from .models import Activation
#TODO from .utils import send_activation_email, send_forgot_pass_email

from datetime import date

class GuestOnlyView(View):
    def dispatch(self, request, *args, **kwargs):
        # Redirect to the index page if the user already authenticated
        if request.user.is_authenticated:
            return redirect('profile')

        return super().dispatch(request, *args, **kwargs)
    

class IndexView(TemplateView):
    template_name = 'registration/index.html'

class RegistrationView(FormView):
    template_name = 'registration/registration.html'
    form_class = RegistrationForm
        
    
    def form_valid(self, form):
        request = self.request
        user = form.save(commit=False)
        user.save()
        user.username = f'user_{user.id}'

        if settings.ENABLE_USER_ACTIVATION:
            user.is_active = False

        user.save()

        if settings.ENABLE_USER_ACTIVATION:
            code = get_random_string(20)

            #TODO: act = Activation()
            #act.activation_code = code
            #act.user = user
            #act.save()

            #TODO: send_activation_email(request, user.email, code)

            # raw_password = form.cleaned_data['password1']

            # user = authenticate(username=user.username, password=raw_password)
            # login(request, user)

            messages.success(
                request, 'Вы успешно зарегистрировались. Для активации аккаунта перейдите по ссылке в электронном письме.')
        else:
            raw_password = form.cleaned_data['password1']

            user = authenticate(username=user.username, password=raw_password)
            login(request, user)

            # messages.success(request, 'Вы успешно зарегистрировались!')
            
        return redirect(reverse_lazy('repository'))
    
    
    
class LoginView(GuestOnlyView, FormView):
    template_name = 'registration/login.html'
    form_class = LoginViaEmailForm
    
    
    @method_decorator(sensitive_post_parameters('password'))
    @method_decorator(csrf_protect)
    @method_decorator(never_cache)
    def dispatch(self, request, *args, **kwargs):
        # Sets a test cookie to make sure the user has cookies enabled
        request.session.set_test_cookie()

        return super().dispatch(request, *args, **kwargs)
    
    def form_valid(self, form):
        request = self.request

        # If the test cookie worked, go ahead and delete it since its no longer needed
        if request.session.test_cookie_worked():
            request.session.delete_test_cookie()

        # The default Django's "remember me" lifetime is 2 weeks and can be changed by modifying
        # the SESSION_COOKIE_AGE settings' option.class
        if settings.USE_REMEMBER_ME:
            if not form.cleaned_data['remember_me']:
                request.session.set_expiry(0)

        login(request, form.user_cache)

        # redirect_to = request.POST.get(REDIRECT_FIELD_NAME, request.GET.get(REDIRECT_FIELD_NAME))
        # url_is_safe = is_safe_url(redirect_to, allowed_hosts=request.get_host(), require_https=request.is_secure())

        # if url_is_safe:
        #     return redirect(redirect_to)
        
        return redirect('profile')
    

class LogoutView(LogoutView):
    login_url = '/login'
    
    def get(self, request, *args, **kwargs):
        super().get(request, *args, **kwargs)
        return redirect(reverse_lazy('index'))