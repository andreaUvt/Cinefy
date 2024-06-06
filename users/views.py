from django.shortcuts import render,redirect
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm

import calendar

from django.db.models import Count,Avg
from django.db.models.functions import ExtractYear,TruncMonth

import plotly.graph_objs as go


from collections import Counter

from cinefy_app.models import Movie, Watched,Watchlist, Profile

from .tokens import account_activation_token
from django.core.mail import EmailMessage
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string

# Create your views here.
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('/')

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, 'Account was created! Please confirm your account on your email!')
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')


def loginUser(request):

    page = 'login'
    if request.user.is_authenticated:
        return redirect('/')
    
    if request.method=='POST':
        username=request.POST['username'].lower()
        password=request.POST['password']

        try:
            user= User.objects.get(username=username)
        except:
            messages.error(request,'Username does not exist')
            return redirect('login')
        
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect(request.GET['next'] if 'next' in request.GET else '/')
        else:
            messages.error(request,'Username OR password is incorrect')
    return render(request, 'users/login_register.html')

def logoutUser(request):
    logout(request)
    messages.info(request, "You logged out!")
    return redirect('login')

def registerUser(request):

    if request.user.is_authenticated:
        return redirect('/')
    page='register'
    form=CustomUserCreationForm
    context={'page': page,'form': form}

    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.is_active=False
            user.save()
            

            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('/')
        else:
            for error in form.errors:
                messages.error(request, f'Error {error}')
                
            
    return render(request,'users/login_register.html',context)



@login_required(login_url='login')
def myAccount(request):
    user = request.user
    profile = user.profile
    watchlist = Watchlist.objects.filter(owner=profile)
    watched = Watched.objects.filter(owner=profile)
    
    watchlist_count = watchlist.count()
    watched_count = watched.count()

    # Calculate total runtime for watchlist and watched movies
    total_watchlist_runtime = sum((item.movie.runtime or 0) for item in watchlist)
    total_watched_runtime = sum((item.movie.runtime or 0) for item in watched)

    for item in watchlist:
        print( item.movie.runtime)

    # Calculate most watched genre
    genres_counter = Counter()
    for item in watched:
        for genre in item.movie.genres.all():
            genres_counter[genre.name] += 1
    print(genres_counter)
    most_watched_genre = genres_counter.most_common(1)[0][0] if genres_counter else None

    # Find the longest and shortest movies watched
    longest_movie = watched.order_by('-movie__runtime').first().movie if watched.exists() else None
    shortest_movie = watched.order_by('movie__runtime').first().movie if watched.exists() else None

    latest_watchlist_movie = watchlist.order_by('-created').first().movie if watchlist.exists() else None

    # Get the latest movie watched
    latest_watched_movie = watched.order_by('-created').first().movie if watched.exists() else None

    watchlist_months = watchlist.annotate(month=TruncMonth('created')).values('month').annotate(count=Count('id'))
    watched_months = watched.annotate(month=TruncMonth('created')).values('month').annotate(count=Count('id'))

    # Get the most active months
    watchlist_active_months = watchlist_months.order_by('-count')[:3]
    watched_active_months = watched_months.order_by('-count')[:3]

    # Convert month numbers to month names
    watchlist_active_months = [(calendar.month_name[month['month'].month], month['count']) for month in watchlist_active_months]
    watched_active_months = [(calendar.month_name[month['month'].month], month['count']) for month in watched_active_months]

    
    genres_counter = Counter()
    for item in watched:
        for genre in item.movie.genres.all():
            genres_counter[genre.name] += 1

    # Get top genres and their counts
    top_genres = [genre[0] for genre in genres_counter.most_common(5)]  # Get top 5 genres
    genre_counts = [genres_counter[genre] for genre in top_genres]

    # Create Plotly bar chart
    data = [
        go.Bar(
            x=genre_counts,
            y=top_genres,
            orientation='h',
        )
    ]
    layout = go.Layout(
        title='Top Genres of Movies Watched',
        xaxis=dict(title='Number of Movies'),
        yaxis=dict(title='Genre'),
        margin=dict(l=150),  # Adjust left margin for genre labels
    )
    fig = go.Figure(data=data, layout=layout)

    context = {
        'username': profile.username,
        'watchlist_count': watchlist_count,
        'watched_count': watched_count,
        'total_watchlist_runtime': total_watchlist_runtime,
        'total_watched_runtime': total_watched_runtime,
        'most_watched_genre': most_watched_genre,
        'longest_movie': longest_movie,
        'shortest_movie': shortest_movie,
        'latest_watchlist_movie': latest_watchlist_movie,
        'latest_watched_movie': latest_watched_movie,
        'watchlist_active_months': watchlist_active_months,
        'watched_active_months': watched_active_months,
        'plot_div': fig.to_html(full_html=False, include_plotlyjs=False),
    }
    return render(request, 'users/myaccount.html', context)