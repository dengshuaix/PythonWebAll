import json

from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.views.decorators.csrf import csrf_exempt

from .models import Plant


# Create your views here.


@csrf_exempt  # csrf 豁免
def plants_view(request):
    if request.method == 'GET':
        plants = list(Plant.objects.all().values())
        return JsonResponse(plants)
    elif request.method == 'POST':
        plant = Plant(**json.loads(request.body))
        plant.save()
        return JsonResponse({"message": "新增成功"})


@csrf_exempt
def plant_view(request, plant_id):
    # 6 , 方法操作。 直接获取模型，根据id
    plant = get_object_or_404(Plant, id=plant_id)

    if request.method == 'GET':
        return JsonResponse({"plant": plant})
    elif request.method == "PUT":
        plant_data = json.loads(request.body)
        Plant.objects.filter(id=plant_id).update(**plant_data)
        return JsonResponse({"message": "更新成功！"})

    elif request.method == "DELETE":
        plant.delete()
        return JsonResponse({"message": "删除成功"})
