# 专业核心课程
lessons = [
    "261C0060",
    "26120450",
    "261C0080",
    "2614N001",
    "26120580",
    "26120610",
    "26120620",
    "26120041",
    "061B0270",
    "061B0280",
    "26120480",
    "26120270",
]

import json


all_lessons = json.load(open("dingscore.json", "r", encoding="utf-8"))
zhuxiu_lessons = json.load(open("zhuxiu.json", "r", encoding="utf-8"))
zhuxiu = []
for le in zhuxiu_lessons:
    if le["xdbjmc"] == "已修":
        zhuxiu.append(le["kcdm"])

totcredits = 0
totgp = 0
for lesson in all_lessons:
    kcdm = lesson.split("-")[3]
    if all_lessons[lesson]["score"] in ["合格", "不合格", "弃修", "A"]:
        continue
    if kcdm in lessons:
        print(all_lessons[lesson])
        all_lessons[lesson]["gp"] = float(all_lessons[lesson]["gp"]) * 1.2
    totgp += float(all_lessons[lesson]["gp"]) * float(all_lessons[lesson]["credit"])
    totcredits += float(all_lessons[lesson]["credit"])

gpa = totgp / totcredits

zhuxiu_credits = 0
zhuxiu_gp = 0
for lesson in all_lessons:
    kcdm = lesson.split("-")[3]
    if kcdm not in zhuxiu:
        continue
    if all_lessons[lesson]["score"] in ["合格", "不合格", "弃修", "A"]:
        continue
    zhuxiu_gp += float(all_lessons[lesson]["gp"]) * float(all_lessons[lesson]["credit"])
    zhuxiu_credits += float(all_lessons[lesson]["credit"])

zhuxiu_gpa = zhuxiu_gp / zhuxiu_credits

print(totcredits, gpa, zhuxiu_credits, zhuxiu_gpa)

print(gpa * 0.2 + zhuxiu_gpa * 0.8)