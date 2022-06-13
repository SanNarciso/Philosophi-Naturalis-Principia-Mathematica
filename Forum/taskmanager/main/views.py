from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import CreateView

from .models import Article
from .forms import ArticleForm, UserCreationForm, RegisterUserForm, CommentForm
from django.views import View
from django.shortcuts import render
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin


def index(reguest):
    return render(reguest, 'main/index.html')


def index(request):
    news = Article.objects.all()
    return render(request, 'main/index.html', {'news': news})


class NewsDetailView(FormMixin, DetailView):
    model = Article
    template_name = 'main/details_view.html'
    context_object_name = 'article'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('news-detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.article = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


def create(request):
    error = ''
    if request.method == "POST":
        form = ArticleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
        else:
            error = 'Форма заполнена неверно!'

    form = ArticleForm()

    data = {
        'form': form,
        'error': error
    }
    return render(request, 'main/create.html', data)


def view_profile(request):
    return render(request, 'main/profile.html', {'user': request.user})


class Register(View):
    form_class = RegisterUserForm
    template_name = 'registration/register.html'

    def get(self, request):
        context = dict(form=RegisterUserForm())
        return render(request, self.template_name, context)

    def post(self, request):
        form = RegisterUserForm(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, dict(form=form))

        form.save()
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password)
        login(request, user)
        return redirect('home')
