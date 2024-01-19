# 先跑 python zjuscore.py -dn 或 -u
import json
import os


def main(xuenian=""):
    if os.path.exists("scores-浙大钉.txt"):
        scores = json.load(open("scores-浙大钉.txt", "r", encoding="utf-8"))
    else:
        scores = json.load(open("userscore.json", "r", encoding="utf-8"))
        scores = [
            [i["kcmc"], i["xf"], i["xn"], i["xq"], i["jd"], i["cj"]]
            for i in scores.values()
        ]
    (
        totalJiDianZJU,
        totalJiDianFDU,
        totalJiDianSJTU,
        totalJiDianUSTC,
        totalJiDianNJU,
        totalXueFen,
    ) = (0, 0, 0, 0, 0, 0)
    for score in scores:
        if xuenian not in score[2]:
            continue
        xuefen = float(score[1])
        totalXueFen += xuefen
        baifen = int(score[5])

        # ZJU
        totalJiDianZJU += float(score[4]) * xuefen

        # FDU
        jiDianFDU = 0.0
        if 90 <= baifen <= 100:
            jiDianFDU = 4.0
        elif 85 <= baifen <= 89:
            jiDianFDU = 3.7
        elif 82 <= baifen <= 84:
            jiDianFDU = 3.3
        elif 78 <= baifen <= 81:
            jiDianFDU = 3.0
        elif 75 <= baifen <= 77:
            jiDianFDU = 2.7
        elif 71 <= baifen <= 74:
            jiDianFDU = 2.3
        elif 66 <= baifen <= 70:
            jiDianFDU = 2.0
        elif 62 <= baifen <= 65:
            jiDianFDU = 1.7
        elif 60 <= baifen <= 61:
            jiDianFDU = 1.3
        totalJiDianFDU += jiDianFDU * xuefen

        # SJTU
        jiDianSJTU = 0.0
        if 95 <= baifen <= 100:
            jiDianSJTU = 4.3
        elif 90 <= baifen <= 94:
            jiDianSJTU = 4.0
        elif 85 <= baifen <= 89:
            jiDianSJTU = 3.7
        elif 80 <= baifen <= 84:
            jiDianSJTU = 3.3
        elif 75 <= baifen <= 79:
            jiDianSJTU = 3.0
        elif 70 <= baifen <= 74:
            jiDianSJTU = 2.7
        elif 67 <= baifen <= 69:
            jiDianSJTU = 2.3
        elif 65 <= baifen <= 66:
            jiDianSJTU = 2.0
        elif 62 <= baifen <= 64:
            jiDianSJTU = 1.7
        elif 60 <= baifen <= 61:
            jiDianSJTU = 1.0
        totalJiDianSJTU += jiDianSJTU * xuefen

        # SJTU
        jiDianUSTC = 0.0
        if 95 <= baifen <= 100:
            jiDianUSTC = 4.3
        elif 90 <= baifen <= 94:
            jiDianUSTC = 4.0
        elif 85 <= baifen <= 89:
            jiDianUSTC = 3.7
        elif 82 <= baifen <= 84:
            jiDianUSTC = 3.3
        elif 78 <= baifen <= 81:
            jiDianUSTC = 3.0
        elif 77 <= baifen <= 75:
            jiDianUSTC = 2.7
        elif 72 <= baifen <= 74:
            jiDianUSTC = 2.3
        elif 68 <= baifen <= 71:
            jiDianUSTC = 2.0
        elif 65 <= baifen <= 67:
            jiDianUSTC = 1.7
        elif 64 == baifen:
            jiDianUSTC = 1.5
        elif 61 <= baifen <= 63:
            jiDianUSTC = 1.3
        elif baifen == 60:
            jiDianUSTC = 1.0
        totalJiDianUSTC += jiDianUSTC * xuefen

        # NJU
        totalJiDianNJU += baifen / 20.0 * xuefen

    if totalXueFen == 0.0:
        return
    print(f"学年: {xuenian if xuenian else '全部'}")
    for i in ["ZJU", "FDU", "SJTU", "USTC", "NJU"]:
        print(f"你在{i}的绩点为 {eval(f'totalJiDian{i}') / totalXueFen : .2f}", end=", ")
    print("\n")


if __name__ == "__main__":
    main("2020-2021")
    main("2021-2022")
    main("2022-2023")
    main("2023-2024")
    main()
