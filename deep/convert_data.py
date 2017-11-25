import pickle

fname = "NHIS_OPEN_GJ_2015.CSV"

with open(fname) as f:
    datas = list(map(lambda x: x.split(","),f.read().split("\n")))


c = {"sex": 2, "age": 3, "height": 5, "weight": 6, "waist": 7, "sight_left": 8, "sight_right": 9, "hear_left": 10, "hear_right": 11, "bp_high": 12, "bp_lwst": 13, "blds": 14, "tot_chole": 15, "triglyceride": 16, "hdl_chole": 17, "ldl_chole": 18, "hmg": 19, "olig_prote_cd": 20, "creatinine": 21, "sgot_ast": 22, "sgpt_alt": 23, "gamma_gtp": 24, "smk_stat_type_cd": 25, "drk_yn": 26, "hchk_oeinspec_yn": 27, "crs_yn": 28, "ttr_yn": 29}

DATA = {"1": {}, "2":{}}
for i in range(1, 25):
    DATA["1"][str(i)] = []
    DATA["2"][str(i)] = []

idx = 0
total = len(datas)

for data in datas[1:-1]:
    idx += 1
    if idx % 10000 == 0:
        print("(%d/%d)"%(idx, total))

    sex = data[c["sex"]]
    age = data[c["age"]]
    x = [data[c["height"]], data[c["weight"]], data[c["waist"]], data[c["sight_left"]], data[c["sight_right"]], data[c["hear_left"]], data[c["hear_right"]], data[c["bp_high"]], data[c["bp_lwst"]], data[c["hmg"]], data[c["smk_stat_type_cd"]], data[c["drk_yn"]]]
    y = 0
    try:
        if not (150 <= float(data[c["tot_chole"]]) <= 250):
            y += 1
    except ValueError:
        pass
    try:
        if not (30 <= float(data[c["triglyceride"]]) <= 135):
            y += 1
    except ValueError:
        pass
    try:
        if not (30 <= float(data[c["hdl_chole"]]) <= 65):
            y += 1
    except ValueError:
        pass
    try:
        if 170 <= float(data[c["ldl_chole"]]):
            y += 1
    except ValueError:
        pass
    try:
        y += float(data[c["olig_prote_cd"]]) - 1
    except ValueError:
        pass
    try:
        if not (0.8 <= float(data[c["creatinine"]]) <= 1.7):
            y += 1
    except ValueError:
        pass
    try:
        if not (0 <= float(data[c["sgot_ast"]]) <= 40):
            y += 1
    except ValueError:
        pass
    try:
        if not (0 <= float(data[c["sgpt_alt"]]) <= 40):
            y += 1
    except ValueError:
        pass
    try:
        if sex == "1":
            if not (11 <= float(data[c["gamma_gtp"]]) <= 63):
                y += 1
        elif sex == "2":
            if not (8 <= float(data[c["gamma_gtp"]]) <= 35):
                y += 1
    except ValueError:
        pass

    DATA[sex][age].append((x,y))

f = open("sex_age.data", "wb")
pickle.dump(DATA, f)
f.close()
