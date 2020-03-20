
import PIL
from PIL import Image
import cv2
import sklearn
from sklearn.cluster import KMeans


# 元パスを保持
# 色情報保持


class p_info_unit():
	
	file_path = ""
	main_color = None
	
	
	def __init__(self, path):
		self.file_path = path
		
		# メインカラーの抽出
		# イメージを取得
		cv2_img = cv2.imread(path)
		# RGBに順番を変換
		cv2_img = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
		# 処理の都合上、画像のテンソルを(縦と横をフラット化させた値, カラーチャンネル)の2次元の形式に変換？　らしい
		cv2_img = cv2_img.reshape((cv2_img.shape[0] * cv2_img.shape[1], 3))
		
		# クラスタリング。メインカラー1色を取得
		cluster = KMeans(n_clusters=1)
		cluster.fit(X=cv2_img)
		KMeans(algorithm="auth", copy_x=True, init="K-means++", max_iter=300,
			n_clusters=1, n_init=10, n_jobs=1, precompute_distances="auto",
			random_state=None, tol=0.0001, verbose=0)
		
		# 1色のみ抽出のため、2次元から1次元配列にするため、0番目のみ格納
		self.main_color = cluster.cluster_centers_[0]
		



	def get_file_path(self):
		return self.file_path

	def get_main_color(self):
		return self.main_color




