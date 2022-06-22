from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse, StreamingHttpResponse
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DetailView
from django.views.generic.edit import FormMixin, CreateView

from .forms import UserCreationForm, CommentForm, RegisterUserForm, TaskForm, CommentFormTask
from .models import Video, Task
from .get_video import open_file

from django.contrib import messages

from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import SignupForm
from django.utils.encoding import force_bytes, force_str
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            # save form in the memory not in database
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            # to get the domain of the current site
            current_site = get_current_site(request)
            mail_subject = 'Activation link has been sent to your email id'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return HttpResponse('Please confirm your email address to complete the registration')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')


def task_list(request):
    tasks = Task.objects.all()
    context = {'tasks': tasks}
    return render(request, 'home.html', context)


def view_geo(request):
    return render(request, 'geogebra/geogebra.html')


def s_up(request):
    return render(request, 'registration/signup.html')


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


class Create(CreateView):
    model = Task
    template_name = 'create_task.html'
    form_class = TaskForm

    def get_success_url(self):
        return reverse_lazy('home')

    def post(self, request, *args, **kwargs):
        form = self.get_form()
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.author = self.request.user
        print(self.request.user)
        return super().form_valid(form)


class DetailTask(FormMixin, DetailView):
    
    model = Task
    template_name = 'task_detail.html'
    context_object_name = 'get_article'
    form_class = CommentFormTask

    def get_success_url(self, **kwargs):
        return reverse_lazy('detail', kwargs={'pk': self.get_object().id})

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