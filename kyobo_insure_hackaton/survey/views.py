from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from keras.models import Sequential, load_model
from keras.layers.core import Dense, Activation
from keras.optimizers import SGD
from copy import deepcopy
import numpy as np
import json

# import numpy as np

MODELS = {"1": {}, "2": {}}
for sex in ["1", "2"]:
    for age in range(5, 19):
        MODELS[sex][str(age)] = load_model("models/%s_%s_model.h5" % (sex, age))
        print("loaded %s %s" % (sex, age))

'''APIJP002'''
products = [("(무)교보프리미어종신보험Ⅲ", (211400, 10000)),
            ("(무)교보미리미리CI보험 _ 필수특약有", (144240, 5000))]


def translate(value, leftMin, leftMax, rightMin, rightMax):
    leftSpan = leftMax - leftMin
    rightSpan = rightMax - rightMin

    valueScaled = float(value - leftMin) / float(leftSpan)

    return rightMin + (valueScaled * rightSpan)


def scale(value, maxValue, minValue=0):
    if value >= maxValue:
        return 1
    return translate(value, minValue, maxValue, 0, 1)


def make_item(item):
    item[0] = scale(item[0], 200)
    item[1] = scale(item[1], 120)
    item[2] = scale(item[2], 100)
    item[3] = scale(item[3], 2.5)
    item[4] = scale(item[4], 2.5)
    item[5] = scale(item[5], 2)
    item[6] = scale(item[6], 2)
    item[7] = scale(item[7], 140, 60)
    item[8] = scale(item[8], 100, 40)
    item[9] = scale(item[9], 16, 10)
    item[10] = scale(item[10], 3, 1)
    return item


@csrf_exempt
def check_answer(requests):
    sex = requests.POST.get("sex")
    age = requests.POST.get("age")
    height = float(requests.POST.get("height"))
    weight = float(requests.POST.get("weight"))
    waist = float(requests.POST.get("waist"))
    sight_left = float(requests.POST.get("sight_left"))
    sight_right = float(requests.POST.get("sight_right"))
    hear_left = float(requests.POST.get("hear_left"))
    hear_right = float(requests.POST.get("hear_right"))
    bp_high = float(requests.POST.get("bp_high"))
    bp_lwst = float(requests.POST.get("bp_lwst"))
    hmg = float(requests.POST.get("hmg", "16.00"))
    smk_stat_type_cd = float(requests.POST.get("smk_stat_type_cd"))
    drk_yn = float(requests.POST.get("drk_yn"))
    quality = MODELS[sex][age].predict(np.asarray([
        make_item([height, weight, waist, sight_left, sight_right, hear_left, hear_right, bp_high, bp_lwst, hmg,
                   smk_stat_type_cd, drk_yn])]))[0]
    # TODO connect to model
    quality = quality - 0.8
    personal_product = []
    for product in products:
        p = deepcopy(product)
        p[0][1] = p[0][1] + (p[0][1] / 10.0) * quality
        personal_product.append(p)

    return HttpResponse(json.dumps({"product": personal_product, "quality": quality}))


# def TODO API 어떻게 쓸까요오오오오ㅗ

def XORExample(request):
    val1 = float(request.GET.get("val1", "0"))
    val2 = float(request.GET.get("val2", "1"))
    test_X = np.array([[val1, val2]], "float32")
    X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], "float32")
    y = np.array([[0], [1], [1], [0]], "float32")

    model = Sequential()
    model.add(Dense(2, input_dim=2))
    model.add(Activation('sigmoid'))
    model.add(Dense(1))
    model.add(Activation('sigmoid'))
    sgd = SGD(lr=0.1, decay=1e-6, momentum=0.9, nesterov=True)
    model.compile(loss='mean_squared_error', optimizer=sgd, class_mode="binary")
    model.fit(X, y, nb_epoch=1000, batch_size=1)
    return HttpResponse(
        str(val1) + " ^ " + str(val2) + " = " + ("1" if model.predict_proba(test_X)[0][0] > 0.5 else "0"))
