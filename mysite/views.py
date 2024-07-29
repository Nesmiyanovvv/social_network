from django.contrib import messages
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.shortcuts import redirect, render
from django.views.generic import TemplateView
from django.contrib.auth import logout, authenticate, login
from django.views import View
from mysite.forms import RegisterForm, ProfileForm, PostForm
from mysite.models import Profile, Post, Comment


class HomeView(TemplateView):
    template_name = "home.html"
    timeline_template_name = "timeline.html"

    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            return render(request, self.template_name)

        if request.method == 'POST':
            form = PostForm(request.POST, request.FILES)
            if form.is_valid():
                form.instance.author = request.user
                form.save()

                return redirect("home")

        context = {
            'posts': Post.objects.all()
        }
        return render(request, self.timeline_template_name, context)


class RegisterView(TemplateView):
    template_name = "registration/register.html"

    def dispatch(self, request, *args, **kwargs):
        form = RegisterForm()

        if request.method == 'POST':
            form = RegisterForm(request.POST)

            if form.is_valid():
                self.create_new_user(form)
                messages.success(request, "Вы успешно зарегистрировались!")
                return redirect("login")

        context = {
            'form': form
        }
        return render(request, self.template_name, context)

    def create_new_user(self, form: RegisterForm):
        User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data.get("email"),
            password=form.cleaned_data['password'],
            first_name=form.cleaned_data.get('first_name'),
            last_name=form.cleaned_data.get('last_name'),
        )


class LoginView(TemplateView):
    template_name = "registration/login.html"

    def dispatch(self, request, *args, **kwargs):
        if request.method == 'GET':
            return render(request, self.template_name)
        if request.method == 'POST':
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(request, username=username, password=password)
            if user is None:
                messages.error(request, "Логин или пароль неправильные")
                return render(request, self.template_name)

            login(request, user)
            return redirect("profile")


class LogoutView(View):
    def dispatch(self, request, *args, **kwargs):
        logout(request)
        return redirect("/")


class ProfileView(TemplateView):
    template_name = "registration/profile.html"

    def dispatch(self, request, *args, **kwargs):
        if not Profile.objects.filter(user=request.user).exists():
            return redirect("edit_profile")

        context = {
            'selected_user': request.user
        }
        return render(request, self.template_name, context)


class EditProfileView(TemplateView):
    template_name = "registration/edit_profile.html"

    def dispatch(self, request, *args, **kwargs):
        form = ProfileForm(instance=self.get_profile(request.user))

        if request.method == 'POST':
            form = ProfileForm(request.POST, request.FILES, instance=self.get_profile(request.user))
            if form.is_valid():
                form.instance.user = request.user
                form.save()

                messages.success(request, "Профиль успешно обновлен!")
                return redirect("profile")

        return render(request, self.template_name, {'form': form})

    def get_profile(self, user: User):
        if not Profile.objects.filter(user=user).exists():
            return None

        return user.profile


class PostCommentView(View):
    def dispatch(self, request, *args, **kwargs):
        post_id = request.GET.get("post_id")
        comment = request.GET.get("comment")

        if comment and post_id:
            post = Post.objects.get(pk=post_id)

            comment = Comment(text=comment, post=post, author=request.user)
            comment.save()

            return render(request, "blocks/comment.html", {'comment': comment})

        return HttpResponse(status=400)