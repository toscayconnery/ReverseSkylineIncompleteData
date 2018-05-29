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

def Insert_Local_Skyline(current_specs, current_bit):
	print("Insert_Local_Skyline : " + str(current_specs))
	global local_skyline
	global shadow_skyline
	global virtual_point

	for i in range(0, len(local_skyline[current_bit])):	#pengulangan sebanyak data yang ada didalam local_skyline, untuk dibandingkan satu persatu dengan data baru
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[current_bit][i][j] != 'null'):
				if(current_specs[j] < local_skyline[current_bit][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[current_bit][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[current_bit][i][-1] = 'delete'
		elif(dominating_local == False and dominated_by_local == True):
			for k in range(0, i+1):
				local_skyline[current_bit][k][-1] = 'ok'
			return False
	dominated = 0
	for i in range(0, len(virtual_point[current_bit])):
		dominating_virtual = False
		dominated_by_virtual = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[current_bit][i][j] != 'null'):
				if(current_specs[j] < virtual_point[current_bit][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[current_bit][i][j]):
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
		local_skyline[current_bit].append(content)
		for i in sorted(local_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				local_skyline[current_bit].remove(i)
		for i in range(0, len(shadow_skyline[current_bit])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[current_bit][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[current_bit][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[current_bit][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[current_bit][i][-1] = 'delete'
		for i in sorted(shadow_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				print(">>> Shadow " + str(i) + " removed")
				shadow_skyline[current_bit].remove(i)
		return True
	elif(dominated == 1):
		n_updated_flag[current_bit] = True
		for i in range(0, len(shadow_skyline[current_bit])):
			dominating_shadow = False
			dominated_by_shadow = False
			for j in range(1, len(current_specs)):
				if(current_specs[j] != 'null' and shadow_skyline[current_bit][i][j] != 'null'):
					if(current_specs[j] < shadow_skyline[current_bit][i][j]):
						dominating_shadow = True
					elif(current_specs[j] > shadow_skyline[current_bit][i][j]):
						dominated_by_shadow = True
			if(dominating_shadow == True and dominated_by_shadow == False):
				shadow_skyline[current_bit][i][-1] = 'delete'
		for i in sorted(shadow_skyline[current_bit], reverse=True):
			if (i[-1] == 'delete'):
				print(">>> Shadow " + str(i) + " removed")
				shadow_skyline[current_bit].remove(i)
		content = list(current_specs)
		content.append('ok');
		shadow_skyline[current_bit].append(content)
		print(">>> Shadow " + str(content)  + " appended, data dominated by virtual")
	return False


def Insert_Candidate_Skyline(current_specs, current_bit):
	print("Insert_Candidate_Skyline : " + str(current_specs))
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
			Insert_Virtual_Point(content, current_bit)
			dominated = 1
	candidate_skyline = [i for i in candidate_skyline if i[-1] == 'ok']
	if(dominated == 0):
		content = list(current_specs)
		content.append(current_bit)
		content.append('ok')
		candidate_skyline.append(content)
		print(">>> Candidate inserted")



def Insert_Virtual_Point(current_specs, current_bit):
	print("Insert_Virtual_Point : " + str(current_specs) + " to " + str(current_bit))
	global local_skyline
	global virtual_point
	global shadow_skyline
	#Move all dominated local_skyline N to shadow_skyline
	for i in range(0, len(local_skyline[current_bit])):
		dominating_local = False
		dominated_by_local = False
		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and local_skyline[current_bit][i][j] != 'null'):
				if(current_specs[j] < local_skyline[current_bit][i][j]):
					dominating_local = True
				elif(current_specs[j] > local_skyline[current_bit][i][j]):
					dominated_by_local = True
		if(dominating_local == True and dominated_by_local == False):
			local_skyline[current_bit][i][-1] = 'delete'

	for i in reversed(local_skyline[current_bit]):
		if (i[-1] == 'delete'):
			print(">>> Local " + str(i) + " moved to shadow")
			shadow_skyline[current_bit].append(i)
			local_skyline[current_bit].remove(i)
			shadow_skyline[current_bit][-1][-1] = 'ok'
	
	#Remove all dominated virtual_point that has same bit
	for i in range(0, len(virtual_point[current_bit])):
		dominating_virtual = False
		dominated_by_virtual = False
		superset_check = 0

		for j in range(1, len(current_specs)):
			if(current_specs[j] != 'null' and virtual_point[current_bit][i][j] != 'null'):
				if(current_specs[j] < virtual_point[current_bit][i][j]):
					dominating_virtual = True
				elif(current_specs[j] > virtual_point[current_bit][i][j]):
					dominated_by_virtual = True
			if(current_specs[j] != 'null'):
				superset_check += 1
			elif(current_specs[j] == 'null' and virtual_point[current_bit][i][j] == 'null'):
				superset_check += 1
		if(dominating_virtual == True and dominated_by_virtual == False and superset_check == len(current_specs)):
			virtual_point[current_bit][i][-1] = 'delete'

	for i in reversed(virtual_point[current_bit]):
		if(i[-1] == 'delete'):
			print(">>> Virtual " + str(i) + " removed")
			virtual_point[current_bit].remove(i)
	content = list(current_specs)
	content.append('ok')
	print(">>> Virtual " + str(content) + " appended")
	virtual_point[current_bit].append(content)


def Update_Global_Skyline():
	print("Update_Global_Skyline")
	global global_skyline
	global candidate_skyline
	global shadow_skyline
	global data_length
	print("EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE")
	print("GLOBAL DATA : " + str(global_skyline))
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
			print(">>> Global " + str(i) + " removed by candidate")
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			print(">>> Candidate " + str(i) + " removed by global")
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
			print(">>> Global " + str(i) + " removed by shadow")
			global_skyline.remove(i)
	for i in reversed(candidate_skyline):
		if(i[-1] == 'delete'):
			print(">>> Candidate " + str(i) + " removed by shadow")
			candidate_skyline.remove(i)
	print("GLOBAL t : " + str(global_skyline))
	print("CANDIDATE : " + str(candidate_skyline))
	for i in candidate_skyline:
		print("i : " + str(i))
		global_skyline.append(i)

	for i in n_updated_flag:
		n_updated_flag[i] == False
	print("GLOBAL DATA : " + str(global_skyline))
	print("XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX")


def Generate_Query_Point():
	query_point.append(6)
	query_point.append(2)
	query_point.append(1)
	query_point.append(3)


def Get_RSL():
	print("")
	print("")
	print("")
	print("Get_RSL()")
	global customer_skyline
	global query_point
	global safe_region
	print("ALL CUSTOMER SKYLINE : " + str(customer_skyline))
	helper = 1
	for dict_index in customer_skyline:		#c is dictionary index
		print("")
		print("")
		print("CUSTOMER SKYLINE INDEX " + str(helper))
		helper += 1
		#mentransformasikan query point untuk kemudian dibandingkan dengan skyline dari customer
		transformed_query = []
		for q in range(0, len(query_point)):
			transformed_value = abs(query_point[q] - customer_skyline[dict_index][-2][q])
			transformed_query.append(transformed_value)
		q_status = True
		for data_index in range(0, len(customer_skyline[dict_index]) - 2):
			#After this, looping for all dimension in data
			dominating_q = False
			dominating_customer = False
			for i in range(1, len(customer_skyline[dict_index][data_index]) - 2):
				if(transformed_query[i - 1] != 'null' and customer_skyline[dict_index][data_index][i] != 'null'):
					if(transformed_query[i - 1] < customer_skyline[dict_index][data_index][i]):
						dominating_customer = True
					elif(transformed_query[i - 1] > customer_skyline[dict_index][data_index][i]):
						dominating_q = True
			if(dominating_q == True and dominating_customer == False): #query_point dominated
				#tell that q is dominated
				# q_status = False
				#hapus customer dari daftar RSL
				customer_skyline[dict_index][-1] = 'not rsl'
				#q tidak perlu dibandingkan dengan customer, proses dilanjutkan untuk user berikutnya ####
				
			elif(dominating_q == False and dominating_customer == True): #query_point_not dominating customer skyline
				customer_skyline[dict_index][data_index][-1] = 'delete'
		if(customer_skyline[dict_index][-1] == 'ok'):
			#data yang statusnya 'not rsl' tidak perlu dihapus demi efisiensi waktu, cukup cari safe region dari data yang statusnya 'ok'
			if(len(safe_region) == 0):
				#Bagian ini hanya menentukan DDR PRIME dari data pertama kemudian memasukkannya ke safe region
				safe_data = []
				for data_index in range(0, len(customer_skyline[dict_index]) - 2):
					if(customer_skyline[dict_index][data_index][-1] == 'ok'):
						projected_value = []
						for i in range(1, len(customer_skyline[dict_index][data_index]) - 2):
							if(customer_skyline[dict_index][data_index][i] == 'null'):
								bottom = 'null'
								top = 'null'
							else:
								bottom = customer_skyline[dict_index][-2][i-1] - customer_skyline[dict_index][data_index][i]
								top = customer_skyline[dict_index][-2][i-1] + customer_skyline[dict_index][data_index][i]
							min_max_value = [bottom, top]
							projected_value.append(min_max_value)
						safe_data.append(projected_value)
						print("this_safe_data : " + str(safe_data))
				safe_region = list(safe_data)
			else:
				#Bagian ini menentukan DDR PRIME dari data yang diperiksa, kemudian membandingkannya dengan safe region
				#Penghitungan DDR PRIME
				safe_data = []
				for data_index in range(0, len(customer_skyline[dict_index]) - 2):
					if(customer_skyline[dict_index][data_index][-1] == 'ok'):
						projected_value = []
						for i in range(1, len(customer_skyline[dict_index][data_index]) - 2):
							if (customer_skyline[dict_index][data_index][i] == 'null'):
								bottom = 'null'
								top = 'null'
							else:
								bottom = customer_skyline[dict_index][-2][i-1] - customer_skyline[dict_index][data_index][i]
								top = customer_skyline[dict_index][-2][i-1] + customer_skyline[dict_index][data_index][i]
							min_max_value = [bottom, top]
							projected_value.append(min_max_value)
						safe_data.append(projected_value)
				print("GELOMBANG DUA   : " + str(safe_data))
				print("PEMBANDINg (SR) : " + str(safe_region))
				#Memperbaharui Safe Region
				new_safe_region = []
				for sr_index in range(0, len(safe_region)):
					for sd_index in range(0, len(safe_data)):
						intersect_status = True
						intersect_data = []
						for i in range(0, len(safe_data[sd_index])):
							#min
							if(safe_data[sd_index][i][0] != 'null' and safe_region[sr_index][i][0] != 'null'):
								min_value = max(safe_data[sd_index][i][0], safe_region[sr_index][i][0])
							elif(safe_data[sd_index][i][0] == 'null' and safe_region[sr_index][i][0] == 'null'):
								min_value = 'null'
							elif(safe_data[sd_index][i][0] == 'null'):
								min_value = safe_region[sr_index][i][0]
							elif(safe_region[sr_index][i][0] == 'null'):
								min_value = safe_data[sd_index][i][0]
							
							#max
							if(safe_data[sd_index][i][1] != 'null' and safe_region[sr_index][i][1] != 'null'):
								max_value = min(safe_data[sd_index][i][1], safe_region[sr_index][i][1])
							elif(safe_data[sd_index][i][1] != 'null' and safe_region[sr_index][i][1] != 'null'):
								max_value = 'null'
							elif(safe_data[sd_index][i][1] == 'null'):
								max_value = safe_region[sr_index][i][1]
							elif(safe_region[sr_index][i][1] == 'null'):
								max_value = safe_data[sd_index][i][1]
							
							if(min_value != 'null' and max_value != 'null'):
								if(min_value > max_value):
									intersect_status = False
							min_max_intersect = [min_value, max_value]
							intersect_data.append(min_max_intersect)
						if(intersect_status == True):
							new_safe_region.append(intersect_data)
				safe_region = list(new_safe_region)

						# 	if(min_value == 'null' and max_value == 'null'):
						# 		pass
						# 	else:
						# 		if(min_value > max_value )
						# 	if(min_value > max_value):
						# 		intersect_status = False
						# 		min_max_value = []
						# 	else:
						# 		min_max_intersect = [min_value, max_value] ######
						# 	intersect_data.append(min_max_intersect) ########
						# if(intersect_status == True):
						# 	new_safe_region.append(intersect_data)
					# 		print("TNY DATA : " + str(safe_data[sd_index][i]))
					# 	print("TOOST : " + str(safe_data[sd_index]))
					# print("TEXST : " + str(safe_region[sr_index]))
				print("new SR : " + str(new_safe_region))
			#safe_region.append(safe_data)
		print("SR : " + str(safe_region))
			# if(len(safe_region) == 0):
			# 	print("safe_region masih kosong YUYUYUYUYUYUYUYUYUY")
			# 	for data_index in range(0, len(customer_skyline[dict_index]) - 2):
			# 		if(customer_skyline[dict_index][data_index][-1] == 'ok'):
			# 			projected_value = []
			# 			for i in range(1, len(customer_skyline[dict_index][data_index]) - 2):
			# 				if(customer_skyline[dict_index][data_index][i] == 'null'): #jika user_preference bisa null, maka harus ditambah pengecekan user preference bisa null:
			# 					bottom = 'null'
			# 					top = 'null'
			# 				else:
			# 					bottom = customer_skyline[dict_index][-2][i-1] - customer_skyline[dict_index][data_index][i]
			# 					top = customer_skyline[dict_index][-2][i-1] + customer_skyline[dict_index][data_index][i]
			# 				min_max_value = [bottom, top]
			# 				projected_value.append(min_max_value)
			# 			safe_data.append(projected_value)
			# 			print("M SAFE REGION : " + str(safe_region))
			# else:
			# 	print("safe_region sudah ada YAYAYAYAYAYAYAYAYAYAY")
			# 	print("TESX : " + str(customer_skyline[dict_index][data_index]))
			# 	print("SAFE DATA : " + str(safe_region))


#product_specs = np.loadtxt('product_specs.txt', skiprows=1, unpack=True)
#user_preference = np.loadtxt('user_preference.txt', skiprows=1, unpack=True)
#current_product = np.loadtxt('current_product.txt', skiprows=1, unpack=True)

fu = open("unlabeled_user_preference.txt")
for list_user in fu:
	temp = [float(x) for x in list_user.split()]
	list_customer.append(temp)


#for x in range(0, len(user_preference[0])):
for x in range(0, len(list_customer)):
	fp = open("random_specs.txt")
	node.clear()
	local_skyline.clear()
	candidate_skyline.clear()
	global_skyline.clear()
	shadow_skyline.clear()
	virtual_point.clear()
	indexhelper = 0
	print("")
	print("")
	print("")
	print("")
	number_of_preference += 1
	print("Processing User Preference No : " + str(number_of_preference))
	for line in fp:
		print("")
		print("")
		current_bit = ""
		current_spec = line.split()
		data = []
		transformed_data = []
		transformed_data.append(current_spec[0])
		data.append(current_spec[0])
		data_length = len(current_spec)
		for i in range(1, data_length):
			if(current_spec[i] == "null"):
				current_bit += "0"
				data.append(current_spec[i])
				transformed_data.append(current_spec[i])
			else:
				current_bit += "1"
				difference = abs(float(current_spec[i]) - list_customer[x][i-1])
				data.append(float(current_spec[i]))
				transformed_data.append(float(difference))
		if current_bit not in node:
			node[current_bit] = []
			node[current_bit].append(data)
			local_skyline[current_bit] = []
			shadow_skyline[current_bit] = []
			virtual_point[current_bit] = []
			n_updated_flag[current_bit] = False
		else:
			node[current_bit].append(data)

		# indexhelper += 1
		# print(indexhelper)
		is_skyline = Insert_Local_Skyline(transformed_data, current_bit)
		if is_skyline == True:
			print(">>> Local inserted")
			Insert_Candidate_Skyline(transformed_data, current_bit)
			if(len(candidate_skyline) > t):
				Update_Global_Skyline()
				candidate_skyline.clear()
		print("**************************************************")
		print("local     : " + str(local_skyline))
		print("candidate : " + str(candidate_skyline))
		print("shadow    : " + str(shadow_skyline))
		print("virtual   : " + str(virtual_point))
		print("**************************************************")
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

Generate_Query_Point()
Get_RSL()

fu.close()