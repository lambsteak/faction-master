# # from app.models import Player
# from math import ceil
#
# # a = {1:[50,20,10,10,10],2:[40,20,20,10,10],3:[10,20,20,20,30],4:[50,20,10,10,10],5:[40,20,20,10,10],6:[50,20,10,10,10],7:[50,20,10,10,10],8:[40,20,0,20,20],9:[0,20,10,60,10],10:[50,20,10,10,10],11:[50,20,10,10,10],12:[50,20,10,10,10],13:[50,20,10,10,10],14:[50,20,10,10,10],15:[0,20,80,0,0],16:[90,0,0,0,10],17:[50,20,10,10,10],18:[50,20,10,10,10],19:[50,20,10,10,10],20:[50,0,0,0,50],21:[20,20,20,20,20],22:[40,20,40,0,0],23:[50,20,10,10,10],24:[50,20,10,10,10],25:[50,20,10,10,10],26:[50,50,0,0,0],27:[40,20,20,10,10],28:[20,20,20,20,20],29:[50,40,10,0,0],30:[50,20,10,10,10],31:[50,0,0,10,40],32:[50,20,10,10,10],33:[30,20,10,30,10],34:[50,20,10,10,10],35:[50,20,10,10,10],36:[50,20,10,10,10],37:[70,0,20,0,10],38:[100,0,0,0,0],39:[50,20,10,10,10],40:[50,20,10,10,10],41:[50,20,10,10,10],42:[50,20,10,10,10],43:[50,20,10,10,10],44:[50,20,10,10,10],45:[50,20,10,10,10],46:[50,20,10,10,10],47:[50,20,10,10,10],48:[50,20,10,10,10],49:[80,20,0,0,0],50:[50,20,10,10,10]}
# factions = [[],[],[],[],[]]
# cutoff = []
# l = [[],[],[],[],[]]
#
# # total = len(Player.query.all())
# total = 18
# print('total: ' + str(total))
# per_faction = ceil(total/5)
# print(per_faction)
#
#
# available = [per_faction] * 5
# clash = []
# def divideIntoFactions(a):
# 	for key in list(a.keys()):
# 		# To find cutoff of all the factions
# 		for i in range(0,5):
# 			l[i].append(a.get(key)[i])
# 	for i in range(0,5):
# 		l[i].sort(reverse = True)
# 		cutoff.append(l[i][per_faction-1]) #Because 10 in each faction
# 	lt = list(a.keys())
# 	for key in lt:
# 		m = max(a.get(key))
# 		ind = a.get(key).index(m)
# 		if available[ind] > 0:
# 			factions[ind].append(key)
# 			available[ind] -= 1
# 			del a[key]
# 		else:
# 			# People with clashing scores need to be dealt with.
# 			clash.append(key)
# 			del a[key]
# 	for i in range(5):
# 		while available[i] > 0:
# 			if not clash:
# 				break
# 			factions[i].append(clash[0])
# 			available[i] -= 1
# 			del clash[0]
# 		# i += 1
# 	# print("Marks", l)
# 	# print("Cutoff",cutoff)
# 	# print("Available",available)
# 	# print("Clash",clash)
# 	return factions
#
#
#
#
#
#
#
#
#
# if __name__ == '__main__':
# 	l = {1: [0.0, 0.0, 0.0, 0.0, 0.0], 2: [19.073569482288843, 16.075156576200406, 7.235142118863039, 15.31322505800463, 12.430939226519348], 3: [0.0, 0.0, 0.0, 0.0, 0.0], 4: [17.16621253405996, 16.49269311064717, 17.054263565891446, 17.169373549883986, 19.613259668508306], 5: [16.89373297002725, 15.866388308977019, 8.52713178294573, 8.352668213457065, 14.640883977900565], 6: [0.0, 0.0, 0.0, 0.0, 0.0], 7: [0.0, 0.0, 0.0, 0.0, 0.0], 8: [0.0, 0.0, 0.0, 0.0, 0.0], 9: [0.0, 0.0, 0.0, 0.0, 0.0], 10: [0.0, 0.0, 0.0, 0.0, 0.0], 11: [0.0, 0.0, 0.0, 0.0, 0.0], 12: [0.0, 0.0, 0.0, 0.0, 0.0], 13: [0.0, 0.0, 0.0, 0.0, 0.0], 14: [0.0, 0.0, 0.0, 0.0, 0.0], 15: [0.0, 0.0, 0.0, 0.0, 0.0], 16: [0.0, 0.0, 0.0, 0.0, 0.0], 17: [0.0, 0.0, 0.0, 0.0, 0.0], 18: [0.0, 0.0, 0.0, 0.0, 0.0]}
#
# 	factions = divideIntoFactions(l)
#
# 	print(factions)



from app.models import Player
from math import ceil

# a = {1:[50,20,10,10,10],2:[40,20,20,10,10],3:[10,20,20,20,30],4:[50,20,10,10,10],5:[40,20,20,10,10],6:[50,20,10,10,10],7:[50,20,10,10,10],8:[40,20,0,20,20],9:[0,20,10,60,10],10:[50,20,10,10,10],11:[50,20,10,10,10],12:[50,20,10,10,10],13:[50,20,10,10,10],14:[50,20,10,10,10],15:[0,20,80,0,0],16:[90,0,0,0,10],17:[50,20,10,10,10],18:[50,20,10,10,10],19:[50,20,10,10,10],20:[50,0,0,0,50],21:[20,20,20,20,20],22:[40,20,40,0,0],23:[50,20,10,10,10],24:[50,20,10,10,10],25:[50,20,10,10,10],26:[50,50,0,0,0],27:[40,20,20,10,10],28:[20,20,20,20,20],29:[50,40,10,0,0],30:[50,20,10,10,10],31:[50,0,0,10,40],32:[50,20,10,10,10],33:[30,20,10,30,10],34:[50,20,10,10,10],35:[50,20,10,10,10],36:[50,20,10,10,10],37:[70,0,20,0,10],38:[100,0,0,0,0],39:[50,20,10,10,10],40:[50,20,10,10,10],41:[50,20,10,10,10],42:[50,20,10,10,10],43:[50,20,10,10,10],44:[50,20,10,10,10],45:[50,20,10,10,10],46:[50,20,10,10,10],47:[50,20,10,10,10],48:[50,20,10,10,10],49:[80,20,0,0,0],50:[50,20,10,10,10]}
factions = [[],[],[],[],[]]
cutoff = []
l = [[],[],[],[],[]]

total = len(Player.query.all())
print('total: ' + str(total))
per_faction = ceil(total/5)
print(per_faction)


available = [per_faction] * 5
clash = []
def divideIntoFactions(a):
	for key in list(a.keys()):
		# To find cutoff of all the factions
		for i in range(0,5):
			l[i].append(a.get(key)[i])
	for i in range(0,5):
		l[i].sort(reverse = True)
		cutoff.append(l[i][per_faction-1]) #Because 10 in each faction
	lt = list(a.keys())
	for key in lt:
		m = max(a.get(key))
		ind = a.get(key).index(m)
		if available[ind] > 0:
			factions[ind].append(key)
			available[ind] -= 1
			del a[key]
		else:
			# People with clashing scores need to be dealt with.
			clash.append(key)
			del a[key]
	for i in range(5):
		while available[i] > 0:
			if not clash:
				break
			factions[i].append(clash[0])
			available[i] -= 1
			del clash[0]
		# i += 1
	# print("Marks", l)
	# print("Cutoff",cutoff)
	# print("Available",available)
	# print("Clash",clash)
	return factions