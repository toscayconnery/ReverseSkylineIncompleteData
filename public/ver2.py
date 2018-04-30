#!/usr/bin/python

import sys
import time
import numpy as np

marker = 1
node = {}
local_skyline = {}
candidate_skyline = []
global_skyline = {}
shadow_skyline = {}
virtual_point = {}
why_not_points = {}
n_updated_flag = {}
t = 5

def Insert_Local_Skyline(current_specs, current_bit):
	global local_skyline
	global shadow_skyline
	global virtual_point
	global node
	print("#########################################")
	print("data    : " + str(current_specs))
	print("#########################################")
	print("local   : " + str(local_skyline))
	print("shadow  : " + str(shadow_skyline))
	print("virtual : " + str(virtual_point))
	print("-----------------------------------------")
	dominated_by_local = 0
	dominated_by_virtual = 0
	local_skyline_node_dominated = []
	virtual_point_node_dominated = []
	shadow_skyline_node_dominated = []
	
	for i in range(0, len(local_skyline[current_bit])):	#pengulangan sebanyak data yang ada didalam local_skyline, untuk dibandingkan satu persatu dengan data baru
		bit_dominated_by_local = 0
		local_greater_flag = 0
		bit_dominating_local = 0
		local_smaller_flag = 0
		print("FFF comparing C" + str(current_specs) +  " with L"  + str(local_skyline[current_bit][i]) )
		for j in range(0, len(current_specs)):
			#print("vvv comparing C" + str(current_specs[j]) + " with L" + str(local_skyline[current_bit][i][j]))
			if(local_skyline[current_bit][i][j] == 'null' or current_specs[j] == 'null'):
				bit_dominating_local += 1
				bit_dominated_by_local += 1
				#print("OOO comparing n" + str(current_specs[j]) + " > n" + str(local_skyline[current_bit][i][j]))
			else:
				if(local_skyline[current_bit][i][j] >= current_specs[j]):
					bit_dominated_by_local += 1
					if(local_skyline[current_bit][i][j] > current_specs[j]):
						local_greater_flag = 1
				if(current_specs[j] >= local_skyline[current_bit][i][j]):
					bit_dominating_local += 1
					#print("OOO comparing C" + str(current_specs[j]) + " > L" + str(local_skyline[current_bit][i][j]))
					if(current_specs[j] > local_skyline[current_bit][i][j]):
						local_smaller_flag = 1
		if(bit_dominated_by_local == len(current_specs) and local_greater_flag == 1):
			dominated_by_local = 1					#####################PRUNING MAY APPLY
		if(bit_dominating_local == len(current_specs) and local_smaller_flag == 1):
			#print("#### bit dominating local : " + str(bit_dominating_local))
			local_skyline_node_dominated.append(local_skyline[current_bit][i])	#######
			local_skyline[current_bit][i][4] = "delete"
	print("local_dominated : " + str(local_skyline_node_dominated))				#######

	if(dominated_by_local == 0):		#P is not dominated by any points on local_skyline list of N
		#if p is dominated only by virtual_point
			#Insert P to shadow_skyline
			#N.updated_flag = True
			#Delete all dominated shadow_skyline
		#else
			#Delete all dominated local_skyline
			#Insert P to local_skyline
			#Delete all dominated shadow_skyline
		#insert P into local_skyline list of N
		for i in range(0, len(virtual_point[current_bit])):
			bit_dominated_by_virtual = 0
			virtual_greater_flag = 0
			for j in range(0, len(current_specs)):
				if((virtual_point[current_bit][i][j] == 'null') or (current_specs[j] == 'null')):
					bit_dominated_by_virtual += 1
				else:
					if(virtual_point[current_bit][i][j] >= current_specs[j]):
						bit_dominated_by_virtual += 1
						if(virtual_point[current_bit][i][j] >= current_specs[j]):
							virtual_greater_flag = 1
			if(bit_dominated_by_virtual == len(current_specs) and virtual_greater_flag == 1):
				dominated_by_virtual = 1

		if(dominated_by_virtual == 1):
			content = list(current_specs)
			content.append("ok")
			shadow_skyline[current_bit].append(content)
			n_updated_flag[current_bit] = True
			for i in range(0, len(shadow_skyline[current_bit])):
				bit_dominating_shadow = 0
				shadow_smaller_flag = 0
				for j in range(0, len(current_specs)):
					if(current_specs[j] >= shadow_skyline[current_bit][i][j]):
						bit_dominating_shadow += 1
						if(current_specs[j] > shadow_skyline[current_bit][i][j]):
							shadow_smaller_flag = 1
				if(bit_dominating_shadow == len(current_specs) and shadow_smaller_flag == 1):
					shadow_skyline_node_dominated.append(shadow_skyline[current_bit][i])		#######
					shadow_skyline[current_bit][i][4] = 'delete'
			for i in sorted(shadow_skyline[current_bit], reverse=True):
				if (i[4] == 'delete'):
					shadow_skyline[current_bit].remove(i)
		elif(dominated_by_virtual == 0):
			for i in sorted(local_skyline[current_bit], reverse=True):
				if (i[4] == 'delete'):
					local_skyline[current_bit].remove(i)
			content = list(current_specs)
			content.append("ok")
			local_skyline[current_bit].append(content)
			for i in range(0, len(shadow_skyline[current_bit])):
				bit_dominating_shadow = 0
				shadow_smaller_flag = 0
				for j in range(0, len(current_specs)):
					if(current_specs[j] >= shadow_skyline[current_bit][i][j]):
						bit_dominating_shadow += 1
						if(current_specs[j] > shadow_skyline[current_bit][i][j]):
							shadow_smaller_flag = 1
				if(bit_dominating_shadow == len(current_specs) and shadow_smaller_flag == 1):
					shadow_skyline_node_dominated.append(shadow_skyline[current_bit][i])		#######
					shadow_skyline[current_bit][i][4] = 'delete'
			for i in sorted(shadow_skyline[current_bit], reverse=True):
				if (i[4] == 'delete'):
					shadow_skyline[current_bit].remove(i)
			return True



		# content = list(current_specs)
		# content.append("ok")
		# local_skyline[current_bit].append(content)

		#delete all dominated local_skyline 
		# for i in sorted(local_skyline[current_bit], reverse=True):
		# 	if (i[4] == 'delete'):
		# 		local_skyline[current_bit].remove(i)

		#check the shadow skyline
		# for i in range(0, len(shadow_skyline[current_bit])):	#iterating through all shadow skyline N
		# 	bit_dominating_shadow = 0
		# 	shadow_smaller_flag = 0
		# 	for j in range(0, len(current_specs)):
		# 		if(current_specs[j] >= shadow_skyline[current_bit][i][j]):
		# 			bit_dominating_shadow += 1
		# 			if(current_specs[j] > shadow_skyline[current_bit][i][j]):
		# 				shadow_smaller_flag = 1
		# 	if(bit_dominating_shadow == len(current_specs) and shadow_smaller_flag == 1):
		# 		shadow_skyline_node_dominated.append(shadow_skyline[current_bit][i])		#######
		# 		shadow_skyline[current_bit][i][4] = 'delete'
		# #deleting all dominated shadow_skyline
		# for i in sorted(shadow_skyline[current_bit], reverse=True):
		# 	if (i[4] == 'delete'):
		# 		shadow_skyline[current_bit].remove(i)
	
	#else:


	#Membandingkan dengan tiap virtual point di node N
	# for i in range(0, len(virtual_point[current_bit])):
	# 	bit_dominated_by_virtual = 0
	# 	virtual_greater_flag = 0
	# 	bit_dominating_virtual = 0
	# 	virtual_smaller_flag = 0
	# 	for j in range(0, len(current_specs)):
	# 		if(virtual_point[current_bit][i][j] >= current_specs[j]):
	# 			bit_dominated_by_virtual += 1
	# 			if(virtual_point[current_bit][i][j] >= current_specs[j]):
	# 				virtual_greater_flag = 1
	# 		if(current_specs[j] >= virtual_point[current_bit][i][j]):
	# 			bit_dominating_virtual += 1
	# 			if(current_specs[j] > virtual_point[current_bit][i][j]):
	# 				virtual_smaller_flag = 1
	# 	if(bit_dominated_by_virtual == len(current_specs) and virtual_greater_flag == 1):
	# 		dominated_by_virtual = 1
	# 	if(bit_dominating_virtual == len(current_specs) and virtual_smaller_flag == 1):
	# 		virtual_point_node_dominated.append(virtual_point[current_bit][i])
	

	#Hanya mencari shadow skyline yang didominasi oleh P
	# for i in range(0, len(shadow_skyline[current_bit])):
	# 	bit_dominating_shadow = 0
	# 	shadow_smaller_flag = 0
	# 	for j in range(0, len(current_specs)):
	# 		if(current_specs[j] >= shadow_skyline[current_bit][i][j]):
	# 			bit_dominating_shadow += 1
	# 			if(current_specs[j] > shadow_skyline[current_bit][i][j]):
	# 				shadow_smaller_flag = 1
	# 	if(bit_dominating_shadow == len(current_specs) and shadow_smaller_flag == 1):
	# 		shadow_skyline_node_dominated.append(shadow_skyline[current_bit][i])
	

	# if(dominated_by_local == 0 and dominated_by_virtual == 0):		#P is not dominated by any points on local_skyline list of N
	# 	content = list(current_specs)
	# 	content.append("ok")
	# 	local_skyline[current_bit].append(content)
	# 	for i in sorted(local_skyline[current_bit], reverse=True):
	# 		if (i[4] == 'delete'):
	# 			local_skyline[current_bit].remove(i)
	# 	for i in shadow_skyline_node_dominated:
	# 		shadow_skyline[current_bit][i].clear()
	# 	return True
	

	# else:																	#P is dominated
	# 	if(dominated_by_virtual == 1):
	# 		shadow_skyline[current_bit].append(current_specs)
	# 		n_updated_flag[current_bit] = True
	# 		for i in shadow_skyline_node_dominated:
	# 			shadow_skyline[current_bit].clear()
	return False


def Insert_Candidate_Skyline(current_specs, current_bit):
	global candidate_skyline
	global virtual_point
	global local_skyline
	dominated = 0
	# print("yyyyy")
	# print(candidate_skyline)
	# print("xxxxx")
	for i in candidate_skyline:
		greater_flag = 0
		smaller_flag = 0
		dominating_bit = 0
		dominated_bit = 0
		current_candidate_bit = i[-1]
		for j in range(0, len(current_specs)):
			if(current_specs[j] != 'null' ):	#and candidate_skyline[j][i] != 'null'
				pass
				# if(current_specs[j] >= candidate_skyline[i][j]):
				# 	dominating_bit += 1
				# 	if(current_specs[j] > candidate_skyline[i][j]):
				# 		greater_flag = 1
				# elif(candidate_skyline[i][j] >= current_specs[j]):
				# 	dominated_bit += 1
				# 	if(candidate_skyline[i][j] > current_specs[j]):
				# 		smaller_flag = 1
		if(dominating_bit > 0 and dominated_bit == 0 and greater_flag == 1):	#if P dominating candidate_skyline
			candidate_skyline.remove(i)
			Insert_Virtual_Point(current_specs, current_candidate_bit)
			virtual_point[bit_x].append(current_specs)
		elif(dominated_bit > 0 and dominating_bit == 0 and smaller_flag == 1):	#if P dominated by candidate_skyline
			virtual_content = i[0:-1]
			Insert_Virtual_Point(virtual_content, current_bit)
			dominated = 1
	if(dominated == 0):
		#if P is not dominated by any point, insert P into candidate skyline list		
		content = list(current_specs)
		content.append(current_bit)
		candidate_skyline.append(content)


def Insert_Virtual_Point(content, current_bit):
	global virtual_point
	if current_bit in virtual_point:
		virtual_point[current_bit].append(content)
	else:
		virtual_point[current_bit] = []
		virtual_point[current_bit].append(content)

product_specs = np.loadtxt('product_specs.txt', skiprows=1, unpack=True)
user_preference = np.loadtxt('user_preference.txt', skiprows=1, unpack=True)

for x in range(0, len(user_preference[0])):	#pengulangan sebanyak user preference
	fp = open("all_product.txt")
	node.clear()
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	for line in fp:
		current_bit = ""
		current_specs = line.split()
		for i in range(0, len(current_specs)):
			if(current_specs[i] == "null"):
				current_bit += "0"
			else:
				current_bit += "1"
				current_specs[i] = abs(int(current_specs[i]) - user_preference[i][x])
		if current_bit not in node:
			node[current_bit] = []
			node[current_bit].append(current_specs)
			local_skyline[current_bit] = []
			shadow_skyline[current_bit] = []
			virtual_point[current_bit] = []
			n_updated_flag[current_bit] = False
		else:
			node[current_bit].append(current_specs)
		is_skyline = Insert_Local_Skyline(current_specs, current_bit)
		print("after ins loc_s : " + str(local_skyline))
		if is_skyline == True:
			Insert_Candidate_Skyline(current_specs, current_bit)
		print("")
	fp.close()
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
	print(local_skyline)
	print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAa")
	print("NEW")