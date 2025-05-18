from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from .forms import imgform
import pytesseract
import easyocr
from PIL import Image
from django.conf import settings
import os
# Create your views here.
from django.http import HttpResponse

def index(request):
    text = " "
    if(request.method=="POST"):
        if request.FILES.get('image'):
            image = request.FILES['image']
            image_name = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            # Assurez-vous que le répertoire existe
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            # Enregistrez le fichier image
            with open(image_path, 'wb') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            img = Image.open(image_path).convert("L")
            reader = easyocr.Reader(['en'])  # You can specify the languages you need
            results = reader.readtext(image_path)
            accuracy = 0
            for result in results:
                text +=result[1]
                accuracy += result[2]

            accuracy = accuracy/len(results)
            print(f"the accuracy is {accuracy}")
            #print(text)
        return render(request,"index.html",{"text":text})
    return render(request,"index.html",{"text":text})
def gpt(request):
    return render(request,"test.html")

def landing(request):
    text = "Your OCR result will appear here..."
    if(request.method=="POST"):
        if request.FILES.get('image'):
            image = request.FILES['image']
            image_name = image.name
            image_path = os.path.join(settings.MEDIA_ROOT, image_name)
            # Assurez-vous que le répertoire existe
            os.makedirs(os.path.dirname(image_path), exist_ok=True)
            # Enregistrez le fichier image
            with open(image_path, 'wb') as destination:
                for chunk in image.chunks():
                    destination.write(chunk)
            img = Image.open(image_path).convert("L")
            reader = easyocr.Reader(['en'])  # You can specify the languages you need
            results = reader.readtext(image_path)
            accuracy = 0
            for result in results:
                text +=result[1]
                accuracy += result[2]

            accuracy = accuracy/len(results)
            print(f"the accuracy is {accuracy}")
            #print(text)
        return render(request,"LandingPage/index.html",{"text":text})
    return render(request,"LandingPage/index.html",{"text":text})
    
def ocr_api(request):
    text = ""
    if request.method == "POST" and request.FILES.get("image"):
        image = request.FILES["image"]
        image_name = image.name
        image_path = os.path.join(settings.MEDIA_ROOT, image_name)
        langue = request.POST.get("langue")
        # Assurez-vous que le répertoire existe
        os.makedirs(os.path.dirname(image_path), exist_ok=True)
        # Enregistrez le fichier image
        with open(image_path, 'wb') as destination:
            for chunk in image.chunks():
                destination.write(chunk)
        img = Image.open(image_path).convert("L")
        reader = easyocr.Reader([langue])
        results = reader.readtext(image_path)
        accuracy = 0
        for result in results:
            text +=result[1]
            accuracy += result[2]

        accuracy = accuracy/len(results)
        print(f"the accuracy is {accuracy}")
        return JsonResponse({"text": text,"accuracy":accuracy})

    return JsonResponse({"error": "Invalid request"}, status=400)