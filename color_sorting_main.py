

import copy

# p_info_unit を保持するためのリスト
# 移行先のフォルダパス名も保持

from p_info_gene import *



class color_sorting_main():
	
	cs_vo = None
	p_unit_list = []
	p_gene_list = []
	div_folder_num = 0
	
	best_fitness_gene = None
	
	def __init__(self, cs_vo):
		self.cs_vo = cs_vo
		self.p_unit_list = cs_vo.get_p_unit_list()
		self.div_folder_num = cs_vo.get_div_folder_num()
		
		self.best_fitness_gene = None
		
		for i in range(100):
			# 色情報遺伝子リストを作成
			self.p_gene_list.append(p_info_gene(cs_vo))
	
	
	
	# ゲッター
	def get_best_fitness_gene(self):
		return self.best_fitness_gene
	
	
	# メイン処理
	def coler_sorting_main(self):
		
		# 適応度計算呼び出し
		for p_gene in self.p_gene_list:
			p_gene.fitness_calc()
			
			if self.best_fitness_gene is None:
				self.best_fitness_gene = copy.deepcopy(p_gene)
			elif self.best_fitness_gene.get_fitness() < p_gene.get_fitness():
				self.best_fitness_gene = copy.deepcopy(p_gene)
			
		
		# 選択メソッドの呼び出し
		self.selection()
		
		
		
##################################################################
		print(self.best_fitness_gene.get_fitness())
##################################################################
		
	
	
	
	# 選出するメソッド
	def selection(self):
		selecter_gene_list = []
		top_gene = None
		
		# 現在の遺伝子数分、新たなる遺伝子を作成
		for i in range(len(self.p_gene_list)):
			selection_gene_list = []
			
			# 無作為に10個体選出
			for j in range(10):
				selection_gene_list.append(self.p_gene_list[random.randint(0, len(self.p_gene_list) - 1)])
				
			
			# 抽出した中の最優秀を確定
			top_gene = selection_gene_list.pop(len(selection_gene_list) - 1)
			for now_gene in selection_gene_list:
				if top_gene.get_fitness() < now_gene.get_fitness():
					top_gene = now_gene
			
			# 新個体群に追加
			selecter_gene_list.append(copy.deepcopy(top_gene))
			
		
		gene_ark = []
		
		# 選出された個体群がいる限り突然変異ループ
		while 0 < len(selecter_gene_list):
			
			gene_pair = []
			
			# 末尾の個体を取り出す。選出段階で無作為なので、ここは素直に取り出していく
			gene_pair.append(selecter_gene_list.pop(len(selecter_gene_list) - 1))
			
			if 0 < len(selecter_gene_list):
				# まだ1個体以上いるなら取り出して処理
				gene_pair.append(selecter_gene_list.pop(len(selecter_gene_list) - 1))
			
				# 2体を突然変異させる
				for result_gene in self.crossover(gene_pair):
					gene_ark.append(result_gene)
			
			else:
				# ペアになれなかったので、単体で突然変異
				gene_ark.append(self.mutation(gene_pair[0]))
			
			
		
		
		# 新個体群を確定する
		self.p_gene_list = gene_ark
		
		
	
	
	# 交叉メソッド
	def crossover(self, gene_pair):
		
		# 交叉
		
		
		# 突然変異もする
		for now_gene in gene_pair:
			self.mutation(now_gene)
		
		
		return gene_pair
		
	
	
	
	# 突然変異メソッド
	def mutation(self, now_gene):
		
		tmp_piece_list = now_gene.get_p_gene_piece_list()
		
		# 遺伝子片の3分の1の数だけ変異する。変えるかも？
		for i in range(len(tmp_piece_list) // 3):
			new_folder = random.randint(0, self.cs_vo.get_div_folder_num() - 1)
			tmp_piece_list[random.randint(0, len(tmp_piece_list) - 1)].set_sorting_folder(new_folder)
			
		
		return now_gene
		
	
	
	
	



