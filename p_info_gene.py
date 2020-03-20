
import random


from p_info_gene_piece import *

# p_info_unit のリストに対応した、フォルダーのリスト　= 遺伝子
# RGBそれぞれでの最小値、最大値
# 適応度


class p_info_gene():
	
	
	def get_fitness(self):
		return self.fitness
	
	
	def __init__(self, cs_vo):
		
		# voの共有
		self.cs_vo = cs_vo
		
		# 遺伝子片のリスト
		self.p_gene_piece_list = []
		
		# 適応度。高いほど良い
		self.fitness = 0
		
		# 初回生成の呼び出し
		self.first_create()
		
	
	########
	# ゲッター
	def get_p_gene_piece_list(self):
		return self.p_gene_piece_list
	
	
	
	########
	# 初回生成メソッド
	def first_create(self):
		tmp_p_unit_list = self.cs_vo.get_p_unit_list()
		tmp_div_folder_num = self.cs_vo.get_div_folder_num()
		
		for p_unit_num in range(len(tmp_p_unit_list)):
			
			# 遺伝子1欠片を作成
			gene_piece = p_info_gene_piece(p_unit_num)
			
			# ランダムなフォルダーを割り当て
			gene_piece.set_sorting_folder(random.randrange(tmp_div_folder_num))
			
			# 遺伝子1欠片の格納
			self.p_gene_piece_list.append(gene_piece)
			
		
	
	
	########
	# 適応度算出メソッド
	def fitness_calc(self):
		
		# 振り分け先フォルダごとに遺伝子片を格納
		folder_list = tmp_folder().folder_sorting(self.cs_vo.get_div_folder_num(), self.p_gene_piece_list)
		
		# 最大値算出呼び出し
		self.find_max_value(folder_list)
		
		# 最小値算出呼び出し
		self.find_min_value(folder_list)
		
		######################################
		### それぞれを比較して適応度を算出 ###
		######################################
		
		# 一時適応度変数作成
		tmp_fitness = 0
		
		# RGB文字列の定数のリスト作成
		RGB_LIST = ["R", "G", "B"]
		
		### フォルダ間での比較 #####
		# フォルダ数-1でフォルダ数を比較
		for now_folder_num in range(self.cs_vo.get_div_folder_num() - 1):
			
			# RGBそれぞれの適応度を算出し、良いほど加算していく。状況パターンに応じて、適応度に重み付けして算出
			for i in range(3):
				# 一時重み変数作成
				tmp_weight = 1
				
				# 現在の最大値と次の最小値の差の絶対値を一時適応度に追加
				tmp_fitness += abs((folder_list[now_folder_num + 1].get_RGB_min_value(RGB_LIST[i])
					- folder_list[now_folder_num].get_RGB_max_value(RGB_LIST[i])) * tmp_weight)
				
				# 現在の最大値と次の最大値の差を一時適応度に格納。これは上回ってたらダメなのでペナルティ重め
				tmp_weight *= 2
				tmp_fitness += (folder_list[now_folder_num + 1].get_RGB_max_value(RGB_LIST[i])
					- folder_list[now_folder_num].get_RGB_max_value(RGB_LIST[i])) * tmp_weight
				
				# 現在の最小値と次の最小値の差を一時適応度に格納。これは下回ってたらダメ
				tmp_fitness -= (folder_list[now_folder_num + 1].get_RGB_min_value(RGB_LIST[i])
					- folder_list[now_folder_num].get_RGB_min_value(RGB_LIST[i])) * tmp_weight
				
				
				
		### フォルダ内で比較 #####
		# フォルダ内で、色が離れているほど減点……にしたい。計算式が難しい。とりあえず色々試して、重み100が良いっぽかった
		for now_folder_num in range(self.cs_vo.get_div_folder_num()):
			# RGBごとに適応度に重み付けして算出
			for i in range(3):
				# 一時重み変数作成
				tmp_weight = 100
				
				# 現在の最大値と現在の最小値の差の絶対値を一時適応度から減算
				tmp_fitness -= abs((folder_list[now_folder_num].get_RGB_max_value(RGB_LIST[i])
					- folder_list[now_folder_num].get_RGB_min_value(RGB_LIST[i])) * tmp_weight)
				
			
		
		# 一時適応度を正式な適応度に格納
		self.fitness = tmp_fitness
		
	
	
	
	########
	# フォルダごとの最大値算出・格納メソッド
	def find_max_value(self, folder_list):
		tmp_p_unit_list = self.cs_vo.get_p_unit_list()
		
		# 最大リスト。R、G、Bがそれぞれ最大のunitの、リスト位置を格納
		for tmp_folder in folder_list:
			for gene_piece in tmp_folder.get_gene_piece_list():
				
				# 対象画像のRGB値の取得
				color_RGB = tmp_p_unit_list[gene_piece.get_p_unit_num()].get_main_color()
				
				# RGB文字列の定数リスト作成
				RGB_LIST = ["R", "G", "B"]
				
				# RGBそれぞれで、最大値を比較して、今までの最大値より大きければ、値をセットし直す
				for i in range(3):
					if tmp_folder.get_RGB_max_value(RGB_LIST[i]) < color_RGB[i]:
						tmp_folder.set_RGB_max_value(RGB_LIST[i], color_RGB[i])
					
				
			
		
	
	
	
	########
	# フォルダごとの最小値算出・格納メソッド
	def find_min_value(self, folder_list):
		tmp_p_unit_list = self.cs_vo.get_p_unit_list()
		
		# 最小リスト。R、G、Bがそれぞれ最小のunitの、リスト位置を格納
		for tmp_folder in folder_list:
			for gene_piece in tmp_folder.get_gene_piece_list():
				
				# 対象画像のRGB値の取得
				color_RGB = tmp_p_unit_list[gene_piece.get_p_unit_num()].get_main_color()
				
				# RGB文字列の定数リスト作成
				RGB_LIST = ["R", "G", "B"]
				
				# RGBそれぞれで、最小値を比較して、今までの最小値より大きければ、値をセットし直す
				for i in range(3):
					if color_RGB[i] < tmp_folder.get_RGB_min_value(RGB_LIST[i]):
						tmp_folder.set_RGB_min_value(RGB_LIST[i], color_RGB[i])
					
				
			
		
	





class tmp_folder():
	
	def __init__(self):
		self.RGB_max_value = {"R":0, "G":0, "B":0}
		self.RGB_min_value = {"R":999, "G":999, "B":999}
		self.gene_piece_list = []
	
	def add_gene_piece_list(self, gene_piece):
		self.gene_piece_list.append(gene_piece)
	
	def get_gene_piece_list(self):
		return self.gene_piece_list
	
	def folder_sorting(self, div_folder_num, p_gene_piece_list):
		# 分割数分の要素数で、フォルダごとに格納するためのリスト作成
		folder_list = [tmp_folder() for i in range(div_folder_num)]
		
		# 振り分け先フォルダごとに遺伝子片を格納
		for gene_piece in p_gene_piece_list:
			folder_list[gene_piece.get_sorting_folder()].add_gene_piece_list(gene_piece)
		
		return folder_list
	
	
	########
	# セッター。引数で指定された、最大値マップのキーに、値を格納する
	def set_RGB_max_value(self, color_key, color_value):
		self.RGB_max_value[color_key] = color_value
	
	########
	# ゲッター。最大値マップから、引数で渡されたキーに格納されている値を返す
	def get_RGB_max_value(self, color_key):
		return self.RGB_max_value[color_key]
	
	########
	# セッター。引数で指定された、最小値マップのキーに、値を格納する
	def set_RGB_min_value(self, color_key, color_value):
		self.RGB_min_value[color_key] = color_value
	
	########
	# ゲッター。最小値マップから、引数で渡されたキーに格納されている値を返す
	def get_RGB_min_value(self, color_key):
		return self.RGB_min_value[color_key]
	



