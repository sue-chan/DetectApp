from django.shortcuts import render, HttpResponse
from .forms import PhotoForm
from .models import Photo
from . import detect_and_search
from mysite import settings

base_url = "https://avdetect.herokuapp.com"

# Create your views here.
def index(request):
    if request.method == "GET":
        params = {
            'form': PhotoForm()
        }
        return render(request, 'detect/index.html', params)
    elif request.method == "POST":
        form = PhotoForm(request.POST, request.FILES)
        if not form.is_valid():
            raise ValueError('画像をアップロードしてください')
        photo = Photo()
        photo.image = form.cleaned_data["image"]
        photo.save()
        url = base_url+ photo.image.url
        name, image_url, link = detect_and_search.main(url)
        params = {
            'name': name,
            'image_url': image_url,
            'link': link
        }
        photo.delete()
        return render(request, 'detect/result.html', params)
