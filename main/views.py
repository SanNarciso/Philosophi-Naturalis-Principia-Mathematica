from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin

from .forms import UserCreationForm, CommentForm, RegisterUserForm
from .models import Video
from .get_video import open_file

from django.contrib import messages


def index(request):
    return render(request, 'home.html')


def view_geo(request):
    return render(request, 'geogebra/geogebra.html')


class Register1(View):
    template_name = 'registration/register.html'

    def get(self, request):
        context = {
            'form': UserCreationForm()
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = UserCreationForm(request.POST)

        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home')
        context = {
            'form': form
        }
        return render(request, self.template_name, context)


def video_list(request):
    videos = Video.objects.all().order_by('-id')
    context = {'videos': videos}
    return render(request, 'videos/video_list.html', context)


def create_video(request):
    if request.method == "POST":
        if "file" in request.FILES:
            file2 = request.FILES["file"]
        else:
            file2 = ' '
        if "image" in request.FILES:
            image2 = request.FILES["image"]
        else:
            image2 = ' '

        if "title" in request.POST:
            title2 = request.POST["title"]
        else:
            title2 = ''
        description2 = request.POST["description"]
        file_format_check = str(file2).split('.')[-1].strip()

        if title2 == '':
            messages.error(request, 'Invalid title')
        elif file2 == ' ':
            messages.error(request, 'Invalid video file')
        elif image2 == ' ':
            messages.error(request, 'Invalid image file')
        elif file_format_check != "mp4":
            messages.error(request, 'Invalid video format. Choose mp4')
        else:
            document = Video.objects.create(file=file2, image=image2, title=title2, description=description2)
            document.save()
            return redirect('video_list')
    return render(request, 'videos/create_video.html')


def get_streaming_video(request, pk: int):
    file, status_code, content_size, full_range = open_file(request, pk)
    response = StreamingHttpResponse(file, status=status_code, content_type='video_storage/mp4')

    response['Accept-Ranges'] = 'bytes'
    response['Content-Length'] = str(content_size)
    response['Cache-Control'] = 'no-cache'
    response['Content-Range'] = full_range
    return response


class video_detail(FormMixin, DetailView):
    model = Video
    template_name = 'videos/video_detail.html'
    context_object_name = 'video'
    form_class = CommentForm

    def get_success_url(self, **kwargs):
        return reverse_lazy('video_detail', kwargs={'pk': self.get_object().id})

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.question = self.get_object()
        self.object.author = self.request.user
        self.object.save()
        return super().form_valid(form)


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
        username = form.cleaned_data.get('username')
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password1')
        user = authenticate(email=email, password=password, username=username)
        login(request, user)
        return redirect('home')