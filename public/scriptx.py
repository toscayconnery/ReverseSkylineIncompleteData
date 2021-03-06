#!/usr/bin/python

import sys
import time
import numpy as np

marker = 1
node = {}
local_skyline = {}
candidate_skyline = []
global_skyline = []
shadow_skyline = {}
virtual_point = {}
why_not_points = {}
n_updated_flag = {}
data_length = 0
t = 5
rsl = []
safe_region = []
number_of_preference = 0
customer_skyline = {}
customer_index = 0
query_point = []
list_customer = []
ct = []
product_list = "random_specs.txt"
intersection = []
ct_cost = []
q_cost = []

def Insert_Local_Skyline(current_specs, bitmap):
	global local_skyline
	global shadow_skyline
	global virtual_point

	for i in range(0, len(local_skyline[bitmap])):	#pengulangan sebanyak data yang ada didalam local_skyline, untuk dibandingkan satu persatu dengan data baru
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[bitmap][i][j] != 'null'):
				if(current_specs[j] < local_skyline[bitmap][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[bitmap][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[bitmap][i][-1] = 'delete'
		elif(dominating_local == False and dominated_by_local == True):
			for k in range(0, i+1):
				local_skyline[bitmap][k][-1] = 'ok'
			return False
	dominated = 0
	for i in range(0, len(virtual_point[bitmap])):
		dominating_virtual = False
		dominated_by_virtual = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[bitmap][i][j] != 'null'):
				if(current_specs[j] < virtual_point[bitmap][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[bitmap][i][j]):
					dominated_by_virtual = True
		if(dominating_virtual == False and dominated_by_virtual == True):
			dominated = 1
			break
	#if p is dominated only by virtual_point
		#Insert P to shadow_skyline
		#N.updated_flag = True
		#Delete all dominated shadow_skyline
	#else
		#Delete all dominated local_skyline
		#Insert P to local_skyline
		#Delete all dominated shadow_skyline
	#inser
	if(dominated == 0):
		content = list(current_specs)
		content.append('ok')
		local_skyline[bitmap].append(content)
		for i in sorted(local_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				local_skyline[bitmap].remove(i)
		for i in range(0, len(shadow_skyline[bitmap])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[bitmap][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[bitmap][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[bitmap][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[bitmap][i][-1] = 'delete'
		for i in sorted(shadow_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				shadow_skyline[bitmap].remove(i)
		return True
	elif(dominated == 1):
		n_updated_flag[bitmap] = True
		for i in range(0, len(shadow_skyline[bitmap])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[bitmap][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[bitmap][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[bitmap][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[bitmap][i][-1] = 'delete'
		for i in sorted(shadow_skyline[bitmap], reverse=True):
			if (i[-1] == 'delete'):
				shadow_skyline[bitmap].remove(i)
		content = list(current_specs)
		content.append('ok');
		shadow_skyline[bitmap].append(content)
	return False


def Insert_Candidate_Skyline(current_specs, bitmap):
	global candidate_skyline
	list_bit_inserted = []
	dominated = 0

	for i in range(0, len(candidate_skyline)):
		dominating_candidate = False
		dominated_by_candidate = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and candidate_skyline[i][j] != 'null'):
				if(current_specs[j] < candidate_skyline[i][j]):
					dominating_candidate = True
				elif(current_specs[j] > candidate_skyline[i][j]):
					dominated_by_candidate = True
		if(dominating_candidate == True and dominated_by_candidate == False):
			candidate_skyline[i][-1] = 'delete'
			if(candidate_skyline[i][-2] not in list_bit_inserted):
				Insert_Virtual_Point(current_specs, candidate_skyline[i][-2])
				list_bit_inserted.append(candidate_skyline[i][-2])
		elif(dominating_candidate == False and dominated_by_candidate == True):
			content = list(candidate_skyline[i][:-2])
			Insert_Virtual_Point(content, bitmap)
			dominated = 1
	candidate_skyline = [i for i in candidate_skyline if i[-1] == 'ok']
	if(dominated == 0):
		content = list(current_specs)
		content.append(bitmap)
		content.append('ok')
		candidate_skyline.append(content)



def Insert_Virtual_Point(current_specs, bitmap):
	global local_skyline
	global virtual_point
	global shadow_skyline
	#MEMBANDINGKAN DENGAN LOCAL SKYLINE
	#Move all dominated local_skyline N to shadow_skyline
	for i in range(0, len(local_skyline[bitmap])):
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[bitmap][i][j] != 'null'):
				if(current_specs[j] < local_skyline[bitmap][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[bitmap][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[bitmap][i][-1] = 'delete'
	for i in reversed(local_skyline[bitmap]):
		if (i[-1] == 'delete'):
			shadow_skyline[bitmap].append(i)
			local_skyline[bitmap].remove(i)
			shadow_skyline[bitmap][-1][-1] = 'ok'
	
	#MEMBANDINGKAN DENGAN VIRTUAL POINT
	#Remove all dominated virtual_point that has same bit
	for i in range(0, len(virtual_point[bitmap])):
		dominating_virtual = False
		dominated_by_virtual = False
		superset_check = 0

		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[bitmap][i][j] != 'null'):
				if(current_specs[j] < virtual_point[bitmap][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[bitmap][i][j]):
					dominated_by_virtual = True
			if(current_specs[j] != 'null'):
				superset_check += 1
			elif(current_specs[j] == 'null' and virtual_point[bitmap][i][j] == 'null'):
				superset_check += 1
		if(dominating_virtual == True and dominated_by_virtual == False and superset_check == len(current_specs)):
			virtual_point[bitmap][i][-1] = 'delete'

	for i in reversed(virtual_point[bitmap]):
		if(i[-1] == 'delete'):
			virtual_point[bitmap].remove(i)
	content = list(current_specs)
	content.append('ok')
	virtual_point[bitmap].append(content)


def Update_Global_Skyline():
	global global_skyline
	global candidate_skyline
	global shadow_skyline
	global data_length
	for c in range(0, len(candidate_skyline)):
		for g in range(0, len(global_skyline)):
			dominating_global = False
			dominating_candidate = False
			for i in range(1, data_length):
				if(candidate_skyline[c][i] != 'null' and global_skyline[g][i] != 'null'):
					if(candidate_skyline[c][i] < global_skyline[g][i]):
						dominating_global = True
					elif(candidate_skyline[c][i] > global_skyline[g][i]):
						dominating_candidate = True
			if(dominating_global == True and dominating_candidate == False):
				global_skyline[g][-1] = 'delete'
			elif(dominating_global == False and dominating_candidate == True):
				candidate_skyline[c][-1] = 'delete'

	for i in reversed(global_skyline):
		if(i[-1] == 'delete'):
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			candidate_skyline.remove(i)
	for g in range(0, len(global_skyline)):
		for i in n_updated_flag:
			if (n_updated_flag[i] == True):
				for s in range(0, len(shadow_skyline[i])):
					dominating_global = False
					dominating_shadow = False
					for j in range(1, data_length):
						if(global_skyline[g][j] != 'null' and shadow_skyline[i][s][j] != 'null' ):
							if(global_skyline[g][j] < shadow_skyline[i][s][j]):
								dominating_shadow = True
							elif(global_skyline[g][j] > shadow_skyline[i][s][j]): 
								dominating_global = True
					if(dominating_global == True and dominating_shadow == False):
						global_skyline[g][-1] == 'delete'

	for c in range(0, len(candidate_skyline)):
		for i in node:
			for s in range(0, len(shadow_skyline[i])):
				dominating_candidate = False
				dominating_shadow = False
				for j in range(1, data_length):
					if(candidate_skyline[c][j] != 'null' and shadow_skyline[i][s][j] != 'null'):
						if(candidate_skyline[c][j] < shadow_skyline[i][s][j]):
							dominating_shadow = True
						elif(candidate_skyline[c][j] > shadow_skyline[i][s][j]):
							dominating_candidate = True
				if(dominating_candidate == True and dominating_shadow == False):
					candidate_skyline[c][-1] = 'delete'

	for i in reversed(global_skyline):
		if(i[-1] == 'delete'):
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			candidate_skyline.remove(i)
	for i in candidate_skyline:
		global_skyline.append(i)

	for i in n_updated_flag:
		n_updated_flag[i] == False


# def Generate_Query_Point(): #OLD
# 	global query_point
# 	query_point.append(6)
# 	query_point.append(2)
# 	query_point.append(1)
# 	query_point.append(3)

def Generate_Query_Point(): #NEW
	global query_point
	query_point = "QP 6 2 1 3"		#SR(q) DAN DDR(ct) berpotongan
	#query_point = "QP 7 5 7 8"		#SR(q) DAN DDR(ct) tidak berpotongan -> KARENA TIDAK ADA SR
	#query_point = "QP 15 15 15 15"	#base
	#query_point = "QP 4 6 8 4"

def Generate_Ct():
	global ct
	ct.append(2)
	ct.append(2)
	ct.append(2)
	ct.append(2)
	# ct.append(2)
	# ct.append(5)
	# ct.append(8)
	# ct.append(2)

def Generate_Cost():
	global ct_cost
	global q_cost
	ct_cost.append(3)
	ct_cost.append(3)
	ct_cost.append(3)
	ct_cost.append(2)
	q_cost.append(4)
	q_cost.append(3)
	q_cost.append(2)
	q_cost.append(3)

def Calculate_RSL_Q(customer_skyline, query_point):
	### - MENGHAPUS SEMUA SKYLINE DARI 'customer_skyline' YANG BUKAN RSL DARI Q, SEHINGGA HANYA TERSISA RSL Q
	### - PASTIKAN NILAI YANG DIPROSES ADALAH HASIL TRANSFORMASI DARI ASLINYA TERHADAP DATA POINT KONSUMEN

	for dict_index in customer_skyline:
		transformed_query = []
		for q in range(0, len(customer_skyline[dict_index][-2])):
			transformed_value = abs(float(query_point[q+1]) - customer_skyline[dict_index][-2][q])
			transformed_query.append(transformed_value)
		for data_index in range(0, len(customer_skyline[dict_index]) - 2):
			dominating_q = False
			dominating_customer = False
			for i in range(1, len(customer_skyline[dict_index][-2])):
				if(customer_skyline[dict_index][data_index][i] != 'null'):
					if(customer_skyline[dict_index][data_index][i] < transformed_query[i]):
						dominating_q = True
					elif(customer_skyline[dict_index][data_index][i] > transformed_query[i]):
						dominating_customer = True
			if(dominating_q == True and dominating_customer == False):
				customer_skyline[dict_index][-1] = 'delete'
			elif(dominating_q == False and dominating_customer == True):
				customer_skyline[dict_index][data_index][-1] = 'delete'
		if(customer_skyline[dict_index][-1] == 'ok'):
			for i in range(len(customer_skyline[dict_index]) - 3, -1, -1):
				if(customer_skyline[dict_index][i][-1] == 'delete'):
					customer_skyline[dict_index].remove(customer_skyline[dict_index][i])
	return customer_skyline




def Generate_Safe_Region_Q():
	### - SEMUA CUSTOMER SKYLINE HANYA YANG JADI RSL DARI Q, (PANGGIL FUNGSI GET RSL Q TERLEBIH DAHULU)
	#This function calculate all safe region areas from every DDR Prime of customer data
	global customer_skyline
	global query_point
	global safe_region

	query_point = query_point.split()
	Calculate_RSL_Q(customer_skyline, query_point)

	safe_region = []
	###PERULANGAN UNTUK SETIAP SKYLINE DARI DATA KONSUMEN
	for dict_index in customer_skyline:		#c is dictionary index
		if(customer_skyline[dict_index][-1] == 'ok'):
			#AAAA -> AT THIS PART, THE CUSTOMER SKYLINE SHOULD BE SORTED BY I'TH DIMENSIONS.
			#SORTING : 

			temp = list(customer_skyline[dict_index][:-2])
			sorted_data = list(sorted(temp, key=lambda newlist: newlist[1]))

			ddr_prime = []

			for data_index in range(0, len(sorted_data)-1):
				data = []
				for i in range(0, len(customer_skyline[dict_index][-2])):
					if(sorted_data[data_index][i+1] == 'null' and sorted_data[data_index+1][i+1] == 'null'):
						top = 'null'
						bottom = 'null'
					elif(sorted_data[data_index][i+1] == 'null'):
						top = customer_skyline[dict_index][-2][i] + sorted_data[data_index+1][i+1]
						bottom = customer_skyline[dict_index][-2][i] - sorted_data[data_index+1][i+1]
					elif(sorted_data[data_index+1][i+1] == 'null'):
						top = customer_skyline[dict_index][-2][i] + sorted_data[data_index][i+1]
						bottom = customer_skyline[dict_index][-2][i] - sorted_data[data_index][i+1]
					else:
						top = max((customer_skyline[dict_index][-2][i] + sorted_data[data_index][i+1]), (customer_skyline[dict_index][-2][i] + sorted_data[data_index+1][i+1]))
						bottom = min((customer_skyline[dict_index][-2][i] - sorted_data[data_index][i+1]), (customer_skyline[dict_index][-2][i] - sorted_data[data_index+1][i+1]))
					max_min_value = [top, bottom]
					data.append(max_min_value)
				ddr_prime.append(data)

			##NEED ADJUSTMENT AT THE END AND BEGINNING OF THE DATA ON DDR PRIME

			if(len(safe_region) == 0):
				safe_region = list(ddr_prime)
			else:
				#checking intersection
				new_safe_region = []
				for safe_index in range(0, len(safe_region)):
					for ddr_index in range(0, len(ddr_prime)):
						intersect_status = True
						intersect_data = []
						#perulangan sebanyak dimensi
						for i in range(0, len(customer_skyline[dict_index][-2])):
							#top
							if(ddr_prime[ddr_index][i][0] == 'null' and safe_region[safe_index][i][0] == 'null'):
									top = 'null'
							elif(ddr_prime[ddr_index][i][0] == 'null'):
								top = safe_region[safe_index][i][0]
							elif(safe_region[safe_index][i][0] == 'null'):
								top = ddr_prime[ddr_index][i][0]
							else:
								top = min(ddr_prime[ddr_index][i][0], safe_region[safe_index][i][0])

							#bottom
							if(ddr_prime[ddr_index][i][1] == 'null' and safe_region[safe_index][i][1] == 'null'):
								bottom = 'null'
							elif(ddr_prime[ddr_index][i][1] == 'null'):
								bottom = safe_region[safe_index][i][1]
							elif(safe_region[safe_index][i][1] == 'null'):
								bottom = ddr_prime[ddr_index][i][1]
							else:
								bottom = max(ddr_prime[ddr_index][i][1], safe_region[safe_index][i][1])

							if(top != 'null' and bottom != 'null'):
								if(bottom > top):
									intersect_status = False
							max_min_value = [top, bottom]
							intersect_data.append(max_min_value)
						if(intersect_status == True):
							new_safe_region.append(intersect_data)
				safe_region = list(new_safe_region)
	return safe_region




def Generate_DDR_Prime_Ct(ct):
	#This function will check if query_point is included to ct's skyline
	#It will return Ct DDR Prime and status of query point
	global product_list
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point
	global bitmap
	global query_point
	global t
	#global safe_region 		#

	fp = open(product_list)
	#Harusnya disini menggunakan variabel global_skyline yang berbeda. (Karena nilai global disimpan dalam variabel lain, sepertinya boleh untuk dihapus)
	#Variabel local_skyline, candidate_skyline, shadow_skyline, dan virtual point harus diinisialisasi ulang
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	node.clear()
	for line in fp:
		bitmap = ""
		transformed_data = Prepare_Data(line, ct)
		is_skyline = Insert_Local_Skyline(transformed_data, bitmap)
		if(is_skyline == True):
			Insert_Candidate_Skyline(transformed_data, bitmap)
			if(len(candidate_skyline) > t):
				Update_Global_Skyline()
				candidate_skyline.clear()
	Update_Global_Skyline()
	candidate_skyline.clear()
	fp.close()

	#check if the QUERY POINT is part of DSL(ct)
	Generate_Query_Point()	#The query point exist from here
	bitmap = ""
	transformed_query_point = Prepare_Data(query_point, ct)
	q_is_local_skyline = Insert_Local_Skyline(transformed_query_point, bitmap)
	if(q_is_local_skyline == True):
		Insert_Candidate_Skyline(transformed_query_point, bitmap)
		Update_Global_Skyline()
		candidate_skyline.clear()

	q_is_dsl = False
	for i in range(0, len(global_skyline)):
		if(global_skyline[i][0] == "QP"):
			q_is_dsl = True
	if(q_is_dsl == True):
		#HENTIKAN PROGRAM
		print("Tidak perlu dilakukan penyesuaian")
		change_status = 0
		exit()
	else:
		#create ddr prime of ct
		sorted_data = list(sorted(global_skyline, key=lambda newlist: newlist[1]))

		ddr_prime_ct = []
		for data_index in range(0, len(sorted_data)-1):
			data = []
			for i in range(0, len(ct)):
				if(sorted_data[data_index][i+1] == 'null' and sorted_data[data_index+1][i+1] == 'null'):
					top = 'null'
					bottom = 'null'
				elif(sorted_data[data_index][i+1] == 'null'):
					top = ct[i] + sorted_data[data_index+1][i+1]
					bottom = ct[i] - sorted_data[data_index+1][i+1]
				elif(sorted_data[data_index+1][i+1] == 'null'):
					top = ct[i] + sorted_data[data_index][i+1]
					bottom = ct[i] - sorted_data[data_index][i+1]
				else:
					top = max((ct[i] + sorted_data[data_index][i+1]), (ct[i] + sorted_data[data_index+1][i+1]))
					bottom = min((ct[i] - sorted_data[data_index][i+1]), (ct[i] - sorted_data[data_index+1][i+1]))
				max_min_value = [top, bottom]
				data.append(max_min_value)
			ddr_prime_ct.append(data)

	return ddr_prime_ct




def Check_Intersection(safe_region, ddr_prime_ct):
	global intersection
	intersection = []
	for safe_index in range(0, len(safe_region)):
		for ddr_index in range(0, len(ddr_prime_ct)):
			intersect_data = []
			intersect_status = True
			for i in range(0, len(safe_region[safe_index])):
				#top
				if(safe_region[safe_index][i][0] == 'null' and ddr_prime_ct[ddr_index][i][0] == 'null'):
					top = 'null'
				elif(safe_region[safe_index][i][0] == 'null'):
					top = ddr_prime_ct[ddr_index][i][0]
				elif(ddr_prime_ct[ddr_index][i][0] == 'null'):
					top = safe_region[safe_index][i][0]
				else:
					top = min(safe_region[safe_index][i][0], ddr_prime_ct[ddr_index][i][0])

				#bottom
				if(safe_region[safe_index][i][1] == 'null' and ddr_prime_ct[ddr_index][i][1] == 'null'):
					bottom = 'null'
				elif(safe_region[safe_index][i][1] == 'null'):
					bottom = ddr_prime_ct[ddr_index][i][1]
				elif(ddr_prime_ct[ddr_index][i][1] == 'null'):
					bottom = safe_region[safe_index][i][1]
				else:
					bottom = max(safe_region[safe_index][i][1], ddr_prime_ct[ddr_index][i][1])

				max_min_value = [top, bottom]
				intersect_data.append(max_min_value)

				if(top != 'null' and bottom != 'null'):
					if(bottom > top):
						intersect_status = False

			if(intersect_status == True):
				intersection.append(intersect_data)
	if(len(intersection) > 0):
		return True
	else:
		return False

def Move_Query_Point():
	global intersection
	global query_point
	global ct_cost
	distance_value = []
	modified_value = []
	for data_index in range(0, len(intersection)):
		nearest_distance = []
		nearest_point = []
		for i in range(0, len(intersection[data_index])):
			a = abs(float(query_point[i+1]) - intersection[data_index][i][0])
			b = abs(float(query_point[i+1]) - intersection[data_index][i][1])
			minimal_distance = min(a,b)
			if(b < a):
				nearest_point.append(intersection[data_index][i][1])
				nearest_distance.append(b)
			else:
				nearest_point.append(intersection[data_index][i][0])
				nearest_distance.append(a)
		distance_value.append(nearest_distance)
		modified_value.append(nearest_point)
	#done, tinggal return kedua nilai ini untuk di analisa
	#atau, langsung olah disini, cari yang mana yang paling efisien

	#Mencari yang paling efisien:
	cheapest_index = None
	current_cost = 99999999999
	for data_index in range(0, len(distance_value)):
		total_cost = 0
		for i in range(0, len(distance_value[data_index])):
			total_cost += (distance_value[data_index][i] * q_cost[i])
		if(total_cost < current_cost):
			cheapest_index = data_index
	recommendation = modified_value[cheapest_index]
	print(recommendation)

def Move_Why_Not_And_Query_Point():
	global safe_region
	global query_point
	global ct
	global product_list
	global ct_cost
	global q_cost

	#Find edge of SR(q)
	#Transform all point, ct is center
	#Remove all data point that dominated by each edge of SR(q)
	#Find frontier
	#Find cheapest modification

	#Find edge of SR(q)
	safe_edge = []
	for data_index in range(0, len(safe_region)):
		nearest = []
		cost = 0
		for i in range(0, len(safe_region[data_index])):
			top_diff = abs(safe_region[data_index][i][0] - float(ct[i]))
			bottom_diff = abs(safe_region[data_index][i][1] - float(ct[i]))
			if(top_diff < bottom_diff):
				nearest.append(safe_region[data_index][i][0])
				cost += (top_diff * q_cost[i])
			elif(top_diff > bottom_diff):
				nearest.append(safe_region[data_index][i][1])
				cost += (bottom_diff * q_cost[i])
			else:	#jika jarak top dan bottom saama, pilih yang top karena data ditransformasikan ke atas
				nearest.append(safe_region[data_index][i][0])
		nearest.append(cost)
		safe_edge.append(nearest)

	print("SAFE EDGE         : " + str(safe_edge))
	#Transform all point, ct is center, SEKALIAN : #Remove all data point that dominated by each edge of SR(q)
	#Cari pasangan tansformasi dan safe_edge dimana hasil transformasi tidak mendominasi safe_edge (dominasi lebih besar yg mendominasi)
	transformed_space = []
	for data_index in range(0, len(safe_edge)):
		print("masuk")
		fp = open(product_list)
		for line in fp:
			product = line.split()
			greater = False		#harus dibawah safe edge
			smaller = False
			transformed_data = []
			for i in range(0, len(product) - 1):
				if(product[i+1] != 'null'):
					transformed_value = float(ct[i]) + abs(float(ct[i]) - float(product[i+1]))
					transformed_data.append(transformed_value)
					if(safe_edge[data_index][i] > transformed_value):
						greater = True
					elif(safe_edge[data_index][i] < transformed_value):
						smaller = True
				else:
					transformed_value = 'null'
					transformed_data.append(transformed_value)
			transformed_data.append(data_index)
			if(greater == True and smaller == False):
				print("appended")
				transformed_space.append(transformed_data)
		fp.close()

	print("TRANSFORMED SPACE : " + str(transformed_space))

	#Find frontier
	#BANDINGKAN SEMUA DATA HASIL SEBELUMNYA
	frontier = list(transformed_space)
	print("frontier init : " + str(frontier))
	for data_index in range(0, len(frontier)):
		#BRUTEFORCE, data disini lebih sedikit, kecuali datanya sama rata
		for data_index_2 in range(0, len(frontier)):
			greater = False
			smaller = False
			for i in range(0, len(frontier[data_index])-1):
				#bandingkan
				if(frontier[data_index][i] != 'null' and frontier[data_index_2][i] != 'null'):
					if(frontier[data_index][i] > frontier[data_index_2][i]):
						greater = True
					elif(frontier[data_index][i] < frontier[data_index_2][i]):
						smaller = True
			if(greater == True and smaller == False):
				frontier[data_index_2][-1] = 'delete'
	eliminated = 0
	for data_index in range(0, len(frontier)):
		if(frontier[data_index][-1] == 'delete'):
			eliminated += 1
	#jika tidak ada skyline
	if(eliminated == len(frontier)):
		frontier = list(transformed_space)
	print("frontier : " + str(frontier))

	#dapatkan titik yang lebih dekat ke edge of safe point, setengah dari jarak (edge of safe point[i] - frontier[i])
	cheapest_index = None
	current_cost = 9999999999
	for data_index in range(0, len(frontier)):
		print('masuk frontier')
		if(frontier[data_index][-1] != 'delete'):
			total_cost = safe_edge[frontier[data_index][-1]][-1]
			safe_index = frontier[data_index][-1]
			for i in range(0, len(frontier[data_index])-1):
				if(frontier[data_index][i] != 'null'):
					origin_point = frontier[data_index][i]
					frontier[data_index][i] += ((safe_edge[safe_index][i] - frontier[data_index][i]) * 0.5)
					difference = abs(origin_point - frontier[data_index][i])
					total_cost += difference * q_cost[i]
			if(total_cost < current_cost):
				cheapest_index = data_index
				current_cost = total_cost
	recommendation = list(frontier[cheapest_index][:-1])
	print("///PERUBAHAN///")
	print("frontier : " + str(frontier))
	print("Q  : " + str(safe_edge[frontier[cheapest_index][-1]]))
	print("CT : " + str(recommendation))



def Prepare_Data(line, customer):
	global bitmap
	global node
	global local_skyline
	global candidate_skyline
	global global_skyline
	global shadow_skyline
	global virtual_point
	global n_updated_flag
	global data_length

	current_spec = line.split()
	data = []
	transformed_data = []
	transformed_data.append(current_spec[0])
	data.append(current_spec[0])
	data_length = len(current_spec)
	for i in range(1, data_length):
		if(current_spec[i] == "null"):
			bitmap += "0"
			data.append(current_spec[i])
			transformed_data.append(current_spec[i])
		else:
			bitmap += "1"
			difference = abs(float(current_spec[i]) - customer[i-1])
			data.append(float(current_spec[i]))
			transformed_data.append(float(difference))
	if bitmap not in node:
		node[bitmap] = []
		node[bitmap].append(data)
		local_skyline[bitmap] = []
		shadow_skyline[bitmap] = []
		virtual_point[bitmap] = []
		n_updated_flag[bitmap] = False
	else:
		node[bitmap].append(data)
	return transformed_data


#PREPROCESSING
#THIS INITIAL PROGRAM WILL CALLED function Generate_All_Dynamic_Skyline
user_preference = "unlabeled_user_preference2.txt"
fu = open(user_preference)
for list_user in fu:
	temp = [float(x) for x in list_user.split()]
	list_customer.append(temp)


for x in range(0, len(list_customer)):
	fp = open(product_list)
	node.clear()
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	number_of_preference += 1
	for line in fp:
		bitmap = ""
		transformed_data = Prepare_Data(line, list_customer[x])
		is_skyline = Insert_Local_Skyline(transformed_data, bitmap)
		if is_skyline == True:
			Insert_Candidate_Skyline(transformed_data, bitmap)
			if(len(candidate_skyline) > t):
				Update_Global_Skyline()
				candidate_skyline.clear()
	fp.close()
	Update_Global_Skyline()

	#Menyimpan semua skyline untuk tiap user
	#sisipkan nilai asli customer preference di akhir list untuk digunakan pada fungsi pembandingan q
	# print("test : " + str(list_customer[x]))
	# temp = list(global_skyline)
	customer_skyline[str(customer_index)] = list(global_skyline)
	customer_skyline[str(customer_index)].append(list(list_customer[x]))
	customer_skyline[str(customer_index)].append("ok")
	customer_index += 1

#Generate_Query_Point()		#Dihapus jika di fungsi Generate_DDR_Prime_Ct() telah berhasil digenerate
#Generate_Safe_Region_Q()

Generate_Ct()
ddr_prime_ct = Generate_DDR_Prime_Ct(ct)

safe_region = Generate_Safe_Region_Q()

Generate_Cost()

intersection_status = Check_Intersection(safe_region, ddr_prime_ct)
if(intersection_status == True):
	print("OPTION 1")
	recommendation = Move_Query_Point()
	print("Need to move query point : ")
else:
	print("OPTION 2")
	print("Need to move why-not and query point : ")
	recommendation =  Move_Why_Not_And_Query_Point()
#print(recommendation)
fu.close()