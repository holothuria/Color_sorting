
import time
import glob

from PIL import Image
import numpy as np
import matplotlib.pyplot as plt


from p_info_unit import *
from color_sorting_main import *
from color_sorting_vo import *

# ピクチャ情報の取得
file_list = glob.glob("./sorting_folder/*.*")


# ピクチャ情報リスト作成
p_unit_list = []
for file_path in file_list:
	p_unit_list.append(p_info_unit(file_path))
	
# フォルダ振り分け数の入力
print("\r\n  フォルダの振り分け数を整数で指定してください -> ")
while True:
	try:
		div_folder_input = int(input())
		break
	except Exception as e:
		print("整数で入力してください！ ->")

# value_object作成
cs_vo = color_sorting_vo()
cs_vo.set_p_unit_list(p_unit_list)
cs_vo.set_div_folder_num(div_folder_input)

# メイン処理オブジェクト作成
ga_main = color_sorting_main(cs_vo)


# 30世代繰り返す
for i in range(30):
	
	ga_main.coler_sorting_main()
	time.sleep(0.2)


###
# 最終的な描画

# 振り分け先フォルダごとに遺伝子片を格納
finish_folder_list = tmp_folder().folder_sorting(cs_vo.get_div_folder_num(), ga_main.get_best_fitness_gene().get_p_gene_piece_list())
#finish_gene_piece_list = ga_main.get_best_fitness_gene().get_p_gene_piece_list()

# 描画するfigureの縦横の画像個数設定
subplot_x = 10
subplot_y = cs_vo.get_div_folder_num()

plt.figure(figsize=(12, 6))

# カウントを取得しつつループ。カウントは0から開始
for i, folder in enumerate(finish_folder_list):
#####################################################################################
#	print(str(gene_piece.get_p_unit_num()) + ":" +str(gene_piece.get_sorting_folder()))
#####################################################################################
	
	# folder 内の画像でループ。カウントは1から開始。subplotの数調整
	for j, gene_piece in enumerate(folder.get_gene_piece_list(), 1):
		
		# 配置場所の設定
		plt.subplot(subplot_y, subplot_x, (i * subplot_x) + j)
		
		# 画像の読み込み
		img = Image.open(cs_vo.get_p_unit_list()[gene_piece.get_p_unit_num()].get_file_path())
		
		# 画像に付くx軸とy軸の削除
		plt.tick_params(labelbottom=False, bottom=False)
		plt.tick_params(labelleft=False, left=False)
		
		# 描画用に登録
		plt.imshow(img)
		
	

# 描画
plt.show()



