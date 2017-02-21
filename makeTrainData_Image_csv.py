#!/usr/bin/env python
# -*- coding: utf-8 -*-

####
# 파노라마 이미지와 라벨링 한 csv파일을 가지고
# faster rcnn을 수행할 수 있도록
# 파노라마 이미지를 argumentation하여 crop을 수행
####

import sys, os
import csv
from os import listdir
from os.path import isfile, join
from PIL import Image, ImageDraw
from random import randint

data_dir = "./"

# 디렉토리 안의 csv 파일 목록들 가져오기
#          >> data_dir 안의 목록을 f로 하나씩 가져옴<<   >>가져온 f가 파일이고 그리고 확장자가 csv면 리스트에 추가<<
csvfiles = [f for f in listdir(data_dir) if isfile(join(data_dir, f)) and f.split('.')[-1] == 'csv']

# 각 csv 파일을 열어 한줄씩 가져와 5개씩 argumentation 수행
n = int(0); #저장할 파일 이름 카운트
# 리스트레 들어있는 csv파일들을 하나씩 접근
for csv_name in csvfiles:
	print(csv_name)
	items = []
	# csv파일을 open함
	with open(csv_name, 'rb') as myfile: # with as 문법을 사용하면 close를 해주지 않아도 with구문이 끝나면 자동으로 해줌
	    reader = csv.reader(myfile)
	    for filename, x, y, w, h, label in reader:
	    	items.append([filename, x, y, w, h, label])

	# csv파일을 open함
	with open(csv_name, 'rb') as myfile: # with as 문법을 사용하면 close를 해주지 않아도 with구문이 끝나면 자동으로 해줌
	    reader = csv.reader(myfile)
	    #csv파일 안에서 한줄씩 가져옴
	    for filename, x, y, w, h, label in reader:
	    	print(filename, x, y, w, h, label)
	    	# 한줄에 대한 아규먼테이션을 수행
	    	for i in range(5):
	    		img = Image.open(filename)
	    		img_w, img_h = img.size
	    		x = int(x)
	    		y = int(y)
	    		w = int(w)
	    		h = int(h)
	    		save_imgname = './%05d.jpg' % n

	    		# >> 여기부터 이미지 크롭해서 저장하는 부분
	    		# get center point
	    		center_x = x+w/2
	    		center_y = y+h/2

	    		# 800 x 800 image crop
	    		crop_size = 800
	    		crop_size_from_center = crop_size / 2

	    		max_w = max([0, crop_size_from_center - w/2]) # 마이너스가 나올수 있으므로 0 max 함..
	    		max_h = max([0, crop_size_from_center - h/2])
	    		min_w = min([max_w, x, img_w - (x + w)])
	    		min_h = min([max_h, y, img_h - (y + h)])

	    		# crop position을 object size와 crop size를 고려해 랜덤으로 뽑음.
	    		rand_w = crop_size_from_center - randint(0 , min_w)
	    		rand_h = crop_size_from_center - randint(0 , min_h)

	    		x1 = center_x - rand_w
	    		y1 = center_y - rand_h
	    		x2 = center_x - rand_w + crop_size
	    		y2 = center_y - rand_h + crop_size
	    		img = img.crop( (x1,  # x1
		    					y1,   # y1 
		    					x2,   # x2
		    					y2 	  # y2
	    					) )
	    		draw = ImageDraw.Draw(img)
				

	    		# << 여기까지는 이미지 크롭해서 저장하는 부분

	    		#새로 이미지를 크롭해서 저장했으면 저장한 이미지에 대한 csv도 만들어야 함.
	    		threshold = 50
	    		savename = './%05d.csv' % n
	    		with open(savename, 'wb') as csvfile:
	    			writer = csv.writer(csvfile)
	    			for filename, new_x, new_y, new_w, new_h, label in items:	    				
	    				new_x = int(new_x)
			    		new_y = int(new_y)
			    		new_w = int(new_w)
			    		new_h = int(new_h)
			    		if (x1 > new_x+new_w or x2 < new_x) and (y1 < new_y+new_h or y2 > new_y):
			    			obj_size_from_crop_img = 0
			    		else:
				    		crop_x1 = max([0, new_x -  x1])
				    		crop_y1 = max([0, new_y+new_h - y1])
				    		crop_x2 = min([crop_size, new_x+new_w - x1])
				    		crop_y2 = min([crop_size, new_y - y1])
				    		# 크롭된 이미지에서의 오브젝트 사이즈
		    				obj_size_from_crop_img = abs((crop_x2 - crop_x1) * (crop_y2 - crop_y1))
		    				draw.rectangle((( crop_x1, crop_y1), ( crop_x2, crop_y2)), outline='red')

	    				# 원본 이미지에서의 이미지 사이즈
	    				obj_size_from_orig_img = new_w * new_h
 
	    				
	    				# 두 사이즈간 얼마나 겹치는지 확인해서 일정 threshold 만족하면 csv에 저장
	    				overlab_percentage = (obj_size_from_orig_img - obj_size_from_crop_img) * 100 / obj_size_from_orig_img
	    				overlab_percentage = 100 - overlab_percentage
	    				if overlab_percentage > threshold:
	    					writer.writerow(([filename, new_x, new_y, new_w, new_h, label]))
			    			print("yes")
	    		print("=======")
	    		n = n + 1	    		
	    		img.save(save_imgname)
















	    