from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views import View
from .models import Profile
from .forms import LoginForm , RegistrationForm , UserEdit , ProfileEdit
from django.views.generic import CreateView

# Create your views here.
def Login(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            user = authenticate(request,
                                username=data['username'],
                                password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request ,user)
                    return HttpResponse("Muvaffaqiyatli login amalga oshirildi !")
                else:
                    return HttpResponse("Sizning profilingiz faol holatda emas !")

            else:
                return HttpResponse("Login yoki parolda xatolik bor !")
    else:
        form = LoginForm()

    return render(request , 'registration/login.html', {"form":form,})
@login_required
def dashboard(request):
    user = request.user
    profile = Profile.objects.get(user=user)
    context = {
        "user":user,
        'profile':profile,
    }
    return render(request , 'pages/dashboard.html' , context)

def Register(request):
    if request.method == "POST":
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit = False)
            new_user.set_password(
                user_form.cleaned_data["password"]
            )
            new_user.save()
            Profile.objects.create(user=new_user)
            context = {
                "new_user":new_user
            }
            return render(request , 'registration/register_done.html' ,context )
    else:
        user_form = RegistrationForm()
        context = {
            "user_form":user_form,
        }
        return render(request , 'registration/register.html' ,context )

class SignUp(CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/register.html'

# class SignUp(View):
#     def get(self , request):
#         user_form = RegistrationForm()
#         context = {
#             "user_form": user_form,
#         }
#         return render(request, 'registration/register.html', context)
#     def post(self, request):
#         user_form = RegistrationForm(request.POST)
#         if user_form.is_valid():
#             new_user = user_form.save(commit=False)
#             new_user.set_password(
#                 user_form.cleaned_data["password"]
#             )
#             new_user.save()
#             context = {
#                 "new_user": new_user
#             }
#             return render(request, 'registration/register_done.html', context)
@login_required
def EditUser(request):
    if request.method == "POST":
        user_form = UserEdit(instance=request.user , data=request.POST)
        profile_form = ProfileEdit(instance=request.user.profile , data=request.POST , files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserEdit(instance=request.user)
        profile_form = ProfileEdit(instance=request.user.profile)
    context = {
        "user_form":user_form,
        "profile_form":profile_form,
    }

    return render(request , 'account/profile_edit.html' ,context )

class EditUserView(LoginRequiredMixin , View):
    def post(self , request):
        user_form = UserEdit(instance=request.user, data=request.POST)
        profile_form = ProfileEdit(instance=request.user.profile, data=request.POST, files=request.FILES)

        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
        context = {
            "user_form": user_form,
            "profile_form": profile_form,
        }

        return render(request, 'account/profile_edit.html', context)
    def get(self , request):
        user_form = UserEdit(instance=request.user)
        profile_form = ProfileEdit(instance=request.user.profile)

        context = {
            "user_form": user_form,
            "profile_form": profile_form,
        }
        return render(request, 'account/profile_edit.html', context)