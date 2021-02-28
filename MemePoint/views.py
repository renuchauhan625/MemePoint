import random, string, requests, json

from django.contrib.auth.models import User
from django.contrib.auth.views import LoginView, TemplateView
from django.shortcuts import render
from accounts.models import UserProfile
    
def display_cookie(request):
    cookie_value = request.COOKIES['my_cookie']
    
    response = requests.get('https://api.imgflip.com/get_memes')
    memes_arr = random.sample([ meme['url'] for meme in json.loads(response.text)['data']['memes'] ],5)
    username = request.user.username
    UserProfile.objects.get_or_create(user=request.user)
    user = User.objects.get(username=username)
    consent_obj = user.profile
    consent_obj.consent = True
    
    user.save()
    consent_obj.save()
    return render(request, 'home.html',{'cookie_value':cookie_value, 'memes_url':memes_arr, 'hide_consent': True})

class LoginUser(LoginView):
    template_name = 'login.html'


class HomeView(TemplateView):
    template_name = 'home.html'
        
    def get(self, request):
        response = render(request, 'home.html')
        cookie_string = ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(16))
        response.set_cookie('my_cookie', cookie_string)    
        return response
    
    
    