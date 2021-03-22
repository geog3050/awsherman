def  Thermotropism(myString, myList):
	aList=[]
	n="" 
	if myString=="Tropical":
		for i in myList:
			if i <= 30:
				n="F"
				aList.append(n)
			else:
				n="U"
				aList.append(n)
		return aList
	elif myString=="Continental":
		for i in myList:
			if i <= 25:
				n="F"
				aList.append(n)
			else:
				n="U"
				aList.append(n)
		return aList
	else:
		for i in myList:
			if i <= 18:
				n="F"
				aList.append(n)
			else:
				n="U"
				aList.append(n)
		return aList