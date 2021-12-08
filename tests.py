angles = [0, 0.5, 1.0, 1.57, 2.0]
angles_list = []

for a in angles:
    for b in angles:
        for c in angles:
            for d in angles:
                for e in angles:
                    angles_list.append([a, b, c, d, e])

for i in angles_list:
    print(i)