


# 遺伝子の中身


class p_info_gene_piece():
	
	# どの画像かの配列番号を保持
	p_unit_num = 0
	
	# 振り分け先フォルダ
	sorting_folder = 0
	
	
	def __init__(self, p_unit_num):
		self.p_unit_num = p_unit_num
	
	
	def get_p_unit_num(self):
		return self.p_unit_num
		
	
	def set_sorting_folder(self, sorting_folder):
		self.sorting_folder = sorting_folder
		
	def get_sorting_folder(self):
		return self.sorting_folder
		
	
	




