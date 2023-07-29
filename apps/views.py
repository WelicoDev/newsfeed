from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import TemplateView, ListView, UpdateView, DeleteView, CreateView
from hitcount.utils import get_hitcount_model

from .models import News, Category, Comment
from .forms import ContactForm, CommentForm
from config.custom_permissions import OnlySuperUser
from hitcount.views import HitCountDetailView, HitCountMixin


def LandingPage(request):
    news_list = News.published.all()
    context = {
        "news_list": news_list,
    }
    return render(request, 'news/landing_page.html', context)


def DetailPage(request, news):
    news = get_object_or_404(News, content=news, status=News.Status.Published)
    context = {
        "news": news,
    }
    return render(request, 'news/detail.html', context)


# def Home(request):
#     category = Category.objects.all()
#     news = News.published.all().order_by("-publish_time")
#
#     uzbekistan_news = News.published.all().filter(category__slug='uzbekistan').order_by("-publish_time")
#     jahon_news = News.published.all().filter(category__slug='jahon').order_by("-publish_time")
#     iqtisodiyot_news = News.published.all().filter(category__slug='iqtisodiyot').order_by("-publish_time")
#     sport_news = News.published.all().filter(category__slug='sport').order_by("-publish_time")
#     texnologiya_news = News.published.all().filter(category__slug='texnologiya').order_by("-publish_time")
#
#     context = {
#         "news":news,
#         'category':category,
#         'uzbekistan_news':uzbekistan_news,
#         'jahon_news': jahon_news,
#         'iqtisodiyot_news': iqtisodiyot_news,
#         'sport_news': sport_news,
#         'texnologiya_news': texnologiya_news,
#     }
#     return render(request, 'pages/index.html', context)
class Home(ListView):
    model = News
    template_name = 'pages/index.html'
    context_object_name = 'news'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = Category.objects.all()
        context['news'] = News.published.all().order_by("-publish_time")
        context['uzbekistan_news'] = News.published.all().filter(category__slug_ctg='uzbekistan').order_by(
            "-publish_time")
        context['jahon_news'] = News.published.all().filter(category__slug_ctg='jahon').order_by("-publish_time")
        context['iqtisodiyot_news'] = News.published.all().filter(category__slug_ctg='iqtisodiyot').order_by(
            "-publish_time")
        context['sport_news'] = News.published.all().filter(category__slug_ctg='sport').order_by("-publish_time")
        context['texnologiya_news'] = News.published.all().filter(category__slug_ctg='texnologiya').order_by(
            "-publish_time")

        return context


class ContactPage(TemplateView):
    template_name = 'pages/contact.html'

    def get(self, request, *args, **kwargs):
        form = ContactForm()
        context = {
            "form": form,
        }
        return render(request, 'pages/contact.html', context)

    def post(self, request, *args, **kwargs):
        form = ContactForm(request.POST)
        if request.method == "POST" and form.is_valid():
            form.save()
            return HttpResponse("<h2>Biz bilan bog'langaningiz uchun tashakkur !</h2>")
        context = {
            "form": form,
        }
        return render(request, 'pages/contact.html', context)

class PostCountHitDetailView(HitCountDetailView):
    model = News
    count_hit = True

def Views(request, news):
    news = get_object_or_404(News, slug = news, status=News.Status.Published)
    context = {}
    hit_count = get_hitcount_model().objects.get_for_object(news)
    hits = hit_count.hits
    hitcontext = context['hitcount'] = {'pk': hit_count.pk}
    hit_count_response = HitCountMixin.hit_count(request , hit_count)
    if hit_count_response.hit_counted:
        hits = hits + 1
        hitcontext['hit_counted']= hit_count_response.hit_counted
        hitcontext['hit_message']=hit_count_response.hit_message
        hitcontext['total_hits'] = hits


    news_list = News.published.all()
    category = Category.objects.all()
    comments = news.comments.filter(active=True)
    comments_count = comments.count()
    new_comment = None
    if request.method == "POST":
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.news = news
            new_comment.user = request.user
            new_comment.save()
            comment_form = CommentForm()
    else:
        comment_form = CommentForm()

    context = {
        "news": news,
        "news_list": news_list,
        'category': category,
        'comments': comments,
        'new_comment': new_comment,
        'comment_form': comment_form,
        'comments_count':comments_count,
    }
    return render(request, 'pages/single_page.html', context)


def ErrorPage(request):
    category = Category.objects.all()
    news = News.published.all().order_by("-publish_time")
    context = {
        "news": news,
        'category': category,
    }
    return render(request, 'pages/404.html', context)


class Uzbekistan(ListView):
    model = News
    template_name = 'pages/uzbekistan.html'
    context_object_name = 'uzbekistan_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__slug_ctg='uzbekistan')

        return news


class Iqtisodiyot(ListView):
    model = News
    template_name = 'pages/iqtisodiyot.html'
    context_object_name = 'iqtisodiyot_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__slug_ctg='iqtisodiyot')

        return news


class Jahon(ListView):
    model = News
    template_name = 'pages/jahon.html'
    context_object_name = 'jahon_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__slug_ctg='jahon')

        return news


class Texnologiya(ListView):
    model = News
    template_name = 'pages/texnologiya.html'
    context_object_name = 'texnologiya_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__slug_ctg='texnologiya')

        return news


class Sport(ListView):
    model = News
    template_name = 'pages/sport.html'
    context_object_name = 'sport_news'

    def get_queryset(self):
        news = self.model.published.all().filter(category__slug_ctg='sport')

        return news


class NewsUpdate(OnlySuperUser, UpdateView):
    model = News
    slug_field = 'slug'
    fields = ('title', 'content', 'image', 'body', 'category', 'status',)
    template_name = 'crud/update.html'


class NewsCreate(CreateView, OnlySuperUser):
    model = News
    template_name = 'crud/create.html'
    prepopulated_fields = {'slug': ('content',)}
    fields = ('title', 'content', 'slug', 'image', 'body', 'category', 'status',)


class NewsDelete(OnlySuperUser, DeleteView):
    model = News
    slug_field = 'slug'
    template_name = 'crud/delete.html'
    success_url = reverse_lazy('home')


@login_required
@user_passes_test(lambda u: u.is_superuser)
def AdminPage(request):
    admin_users = User.objects.filter(is_superuser=True)
    context = {
        "admin_users": admin_users
    }

    return render(request, 'account/admin.html', context)

class SearchResult(ListView):
    model = News
    template_name = 'pages/search.html'
    context_object_name = 'search_results'

    def get_queryset(self):
        query = self.request.GET.get('q')
        return News.objects.filter(
            Q(title__icontains = query) | Q(content__icontains=query) | Q(body__icontains = query)
        )

