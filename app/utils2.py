from app.models import Player

total = len(Player.query.all())

per_faction = 3

factions = [[], [], [], [], []]
avails = [per_faction] * 5
# print(avails)
def get_max_key(scores):
    arr = []
    p = 0
    for k in scores:
        b = [p, k]
        arr.append(b)
        p += 1
    sorted_arr = sorted(arr, key=lambda x:x[1], reverse=True)
    new_sorted = [x[0] for x in sorted_arr]
    return new_sorted


def divide_into_factions(a):
    # al = []
    keys = []
    for i in a.keys():
        keys.append(i)
    keys.sort()
    for key in keys:
        scores = a[key]
        c = 0
        while True:
            max_key_list = get_max_key(scores)
            # print(max_key_list[c])
            if avails[max_key_list[c]] > 0:
                factions[max_key_list[c]].append(key)
                avails[max_key_list[c]] -= 1
                break
            c += 1
    return factions

a = {
    2: [1,2,3,4,5],
    1: [5,3,2,1,4],
}
a = {1:[50,20,10,10,10],2:[10,20,20,10,40],3:[10,20,20,20,30],4:[50,20,10,10,10],5:[40,20,20,10,10],6:[50,20,10,10,10],7:[50,20,10,10,10],8:[40,20,0,20,20],9:[0,20,10,60,10],10:[50,20,10,10,10],11:[50,20,10,10,10],12:[50,20,10,10,10],13:[50,20,10,10,10]}

res = divide_into_factions(a)
print(res)