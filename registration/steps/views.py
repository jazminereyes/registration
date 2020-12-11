from braces.views import AjaxResponseMixin, JSONResponseMixin
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render, reverse
from django.views.generic import CreateView, FormView, TemplateView, View
from .models import UserState

# Create your views here.
class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'registration/register.html'
    url_name = 'register'

    def get_success_url(self):
        return reverse('home')
    
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect(self.get_success_url())


class StepView(LoginRequiredMixin, FormView):
    form_class = UserCreationForm
    template_name = 'step.html'
    url_name = 'step'

    def dispatch(self, request, *args, **kwargs):
        step = self.kwargs.get('step', None)
        if step and step > 3:
            return redirect(reverse('home'))
        return super().dispatch(request, *args, **kwargs)

    def get_object(self):
        user = self.request.user
        return user
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        state = UserState.objects.get(user=self.get_object())

        step = state.step
        if self.kwargs.get('step'):
            step = self.kwargs.get('step')

        buttons = []
        for i in range(1, 4):
            disabled = True
            active = False
            if i <= step:
                disabled = False
                active = True if i == step else False
            buttons.append({
                'disabled': disabled,
                'active': active,
                'step': i
            })
        
        context.update({
            'form': self.get_form(),
            'state': state,
            'buttons': buttons,
            'step': step,
        })
        return context


class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'

    def dispatch(self, request, *args, **kwargs):
        user = request.user
        state, created = UserState.objects.get_or_create(
            user=user
        )

        if not state.is_finished:
            return redirect(reverse('step'))
        else:
            return super().dispatch(request, *args, **kwargs)


class StepAjaxView(
    JSONResponseMixin,
    AjaxResponseMixin,
    View
):

    def post_ajax(self, request, *args, **kwargs):
        step = int(request.POST.get('step'))
        form_value = request.POST.get('form_value')
        user = request.user
        user_state = UserState.objects.get(user=user)

        finished = False
        is_null = False
        if step==1:
            if not user.first_name:
                is_null = True
            user.first_name = form_value
        elif step==2:
            if not user.last_name:
                is_null = True
            user.last_name = form_value
        elif step==3:
            finished = True
            user.email = form_value
        
        user.save()

        if finished:
            user_state.is_finished = True
        else:
            if is_null:
                user_state.step = step + 1
        user_state.save()

        return self.render_json_response({
            'success': 'OK',
            'step': user_state.step,
        })