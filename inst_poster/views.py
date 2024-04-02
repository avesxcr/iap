from django.shortcuts import render
from .models import *
from scripts.poster import Poster
import random


def poster(request):
    if request.method == 'POST':
        inst_account = request.POST.get('inst_account')
        inst_photo_category = request.POST.get('inst_photo_category')
        inst_photos = int(request.POST.get('inst_photos'))
        inst_caption = request.POST.get('inst_caption')

        data_pass = DataCredentials.objects.get(login_inst=inst_account)
        inst_category = Category.objects.get(title=inst_photo_category)
        data_inst_caption = Captions.objects.get(category=inst_category)
        data_inst_photo_category = InstPhotos.objects.filter(category=inst_category)
        random_values = []
        if inst_caption:
            captions = data_inst_caption.caption.split('\n')
            captions = [item.replace('\r', '') for item in captions]
            random_values = random.choices(captions, k=inst_photos)
        photo_and_caption_list = []

        count = 0
        for i in data_inst_photo_category:
            if count >= inst_photos:
                break
            photo_and_caption_list.append({
                f'{i.get_absolute_url()}': f'{random_values[count] if len(random_values) !=0 else ""}'
            })
            count += 1
        print(photo_and_caption_list)
        inst_password = data_pass.pass_inst
        bot = Poster()
        bot.main(inst_account, inst_password, photo_and_caption_list)
    all_accounts = DataCredentials.objects.all()
    all_categories = Category.objects.all()
    data = {
        'accounts': all_accounts,
        'categories': all_categories
    }
    return render(request, template_name='upload/upload.html', context=data)
