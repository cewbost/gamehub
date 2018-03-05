import pdb
from random import shuffle

import ast
from django.db.models import Sum
from django.shortcuts import render, redirect
from django.http import Http404
from django.contrib.auth import login
from django.views.generic.edit import CreateView, UpdateView
from django.views.generic import DetailView
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.contrib import messages
from django.urls import reverse
from django.core import signing
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.views import View
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from gameHub.settings import ImageSizeEnum
from .forms import RegisterForm, GroupChoiceForm, ProfileUpdateForm
from game.models import Game, PaymentDetail, GamePlayed


# Create your views here.

class RegisterView(CreateView):
    """Registration of the user - custom form to include the group selection"""
    model = User
    form_class = RegisterForm
    def post(self, request):
        form = RegisterForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            user.refresh_from_db()  # load the profile instance created by the signal
            tmp_img = form.cleaned_data.get('image')
            if tmp_img is not None:
                user.profile.image = Game.resize_image( tmp_img, tmp_img.name, ImageSizeEnum.PROFILE)
            else:
                user.profile.image = form.cleaned_data.get('image')
            user.profile.description = form.cleaned_data.get('description')
            user.profile.nickname = form.cleaned_data.get('nickname')
            if form.cleaned_data.get('developer'):
                group = Group.objects.get(name='Developer')
                group.user_set.add(user)
            else:
                group = Group.objects.get(name='Player')
                group.user_set.add(user)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            subject = 'Activate your account in GameHub'
            message = render_to_string('accounts/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'token': signing.dumps({'id': user.id}),
                'expiry': settings.ACTIVATION_TIME
            })
            user.email_user(subject, message)
            messages.add_message(request, messages.INFO, 'Activate your account with link in your email!')
            return redirect('accounts:login')
        else:
            return render(request, template_name='accounts/register.html', context={'form': form })
    def get(self, request):
        if self.request.user.is_authenticated:
            return redirect('accounts:home')
        else:
            form = RegisterForm()
            return render(request, template_name='accounts/register.html', context={'form': form})

class ActivationView(View):
    def get(self, request, token):
        try:
            id_dict = signing.loads(token, max_age=settings.ACTIVATION_TIME)
            id = id_dict['id']
            user = User.objects.get(pk=id)
        except:
            user = None
        if user is not None:
            user.is_active = True
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('accounts:home')
        else:
            return render(request, 'accounts/activation_error.html')

class ProfileUpdateView(UpdateView):
    model = User
    form_class = ProfileUpdateForm
    def post(self, request, pk):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            user = form.save(commit=False)
            tmp_img = form.cleaned_data.get('image')
            if tmp_img is not None:
                user.profile.image = Game.resize_image(tmp_img, tmp_img.name, ImageSizeEnum.PROFILE)
            else:
                user.profile.image = form.cleaned_data.get('image')
            user.profile.description = form.cleaned_data.get('description')
            user.profile.nickname = form.cleaned_data.get('nickname')
            user.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect(reverse('accounts:detail', kwargs={'pk':self.request.user.id}))
        else:
            return render(request, template_name='accounts/update.html', context={'form': form })
    def get(self, request, pk):
        if self.request.user.id != pk:
            messages.success(self.request, "Only your account please")
            return redirect(reverse('accounts:update', kwargs={'pk':self.request.user.id}))
        else:
            self.object = self.get_object()
            form_class = self.get_form_class()
            form = self.get_form(form_class)
            form.fields['nickname'].initial = self.object.profile.nickname
            form.fields['description'].initial = self.object.profile.description
            form.fields['image'].initial = self.object.profile.image
            return render(request, template_name='accounts/update.html', context={'form': form})
    def get_object(self):
        return self.request.user

class ProfileDetailView(DetailView):
    model = User
    template_name = "accounts/detail.html"

    def get_context_data(self, **kwargs):
        context = super(ProfileDetailView, self).get_context_data(**kwargs)
        #add what is needed in profiledetails
        developed_games = Game.objects.filter(developer=self.request.user)
        played_games = self.request.user.gameplayed_set.all()
        for played_game in played_games:
            try:
                dictionary=ast.literal_eval(played_game.gameState)
                dictionary = dictionary['gameState']
                played_game.score =  dictionary['score']
                played_game.playedItems = dictionary['playerItems']
                #played_game.score = dictionary['score']
            except TypeError:
                played_game.gameState = 'No Stats'
        for game in developed_games:
            game.total_earn = game.sellcount * game.price
        context['developed_games'] = developed_games
        context['played_games'] = played_games
        return context


class ProfileStatisticsView(View):
    def get(self, request, **args):
        return render(request, template_name='accounts/statistic_details.html', context={'game': Game.objects.get(id=args.get('game'))})


class HomeView(View):
    def get(self, request):
        # Creates a lazy queryset, queryset are evaluated when used (no memory waste)
        games = list(Game.objects.all())
        page = request.GET.get('page', 1)
        # slice the queryset in pages of 12 elements
        paginator = Paginator(games, 12)
        try:
            games = paginator.page(page)
        except PageNotAnInteger:
            games = paginator.page(1)
        except EmptyPage:
            games = paginator.page(paginator.num_pages)
        top_20_games = list(games[:20])
        shuffle(top_20_games) #shuffle the top 20 games
        carousel_games=top_20_games[:3] #choose only three
        return render(request, template_name='gamehub/home.html', context={'carousel_games': carousel_games, 'games':games})


class ChooseGroupView(View):
    """This is view to let social users update their group when creating an account
    And it must be protected with group_missing_required decorators.
    """
    def post(self, request):
        form = GroupChoiceForm(request.POST)
        #any better implementation than this?
        if 'user_group' not in request.session or request.session['user_group'] != 'temp_value':
            raise Http404('Not accessible without social login!')
        if form.is_valid():
            # because of FIELDS_STORED_IN_SESSION, this will get copied
            # to the request dictionary when the pipeline is resumed
            if len(request.user.groups.all()) >= 1:
                messages.add_message(request, messages.INFO, 'You already belong to a group!')
                return redirect('accounts:home')
            request.session['user_group'] = str(form.cleaned_data['group'])
            # once we have the user_group stashed in the session, we can
            # tell the pipeline to resume by using the "complete" endpoint
            return redirect(reverse('social:complete', args=["google-oauth2"]))
        else:
            form = GroupChoiceForm()
            return render(request, "accounts/pick_group.html", context={'form': form})
    def get(self, request):
        form = GroupChoiceForm()
        if 'user_group' in request.session and request.session['user_group'] == 'temp_value':
            return render(request, "accounts/pick_group.html", context={'form': form})
        else:
            raise Http404('Accessible only if you use social login')
