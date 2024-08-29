import os,sys
import tkinter as tk
from tkinter import filedialog
from tkinter import StringVar
from tkinter import messagebox as messagebox
import cv2
import shutil
import glob
import os

# ウィジェットの作成
class Application(tk.Frame):
	def __init__(self,root = None):
		super().__init__(root,width = 420,height = 320,borderwidth = 4,relief = 'groove')

		self.root = root

		# 位置・サイズの指定
		self.pack()
		self.pack_propagate(0)

		# オブジェクトの呼び出し
		self.create_widgets()

	# オブジェクトの作成
	def create_widgets(self):
		# アプリの終了ボタン
		quit_btn = tk.Button(self)
		quit_btn['text'] = '閉じる'
		quit_btn['command'] = self.root.destroy
		quit_btn.pack(side = 'bottom')

		# # テキストボックス
		# self.text_box = tk.Entry(self)
		# self.text_box['width'] = 10
		# self.text_box.pack()

		# ================================================
		# 解析対象の格納場所
		# ================================================
		# 「フォルダ参照」ラベルの作成
		IDirLabel = tk.Label(self, text = "解析対象のフォルダ＞＞", padx = 5, pady = 2)
		IDirLabel.pack()

		# 「フォルダ参照」エントリーの作成
		self.entry1 = StringVar()
		self.IDirEntry = tk.Entry(self, textvariable = self.entry1, width = 30)
		self.IDirEntry.pack()

		# 「フォルダ参照」ボタンの作成
		IDirButton = tk.Button(self, text = "参照", command = self.folder_path)
		IDirButton.pack()
	    # ================================================


	    # ================================================
		# 解析後の格納場所
		# ================================================
		# 「フォルダ参照」ラベルの作成
		IDirLabel2 = tk.Label(self, text = "解析結果のフォルダ＞＞", padx = 5, pady = 2)
		IDirLabel2.pack()

		# 「フォルダ参照」エントリーの作成
		self.entry2 = StringVar()
		self.IDirEntry2 = tk.Entry(self, textvariable = self.entry2, width = 30)
		self.IDirEntry2.pack()

		# 「フォルダ参照」ボタンの作成
		IDirButton2 = tk.Button(self, text = "参照2", command = self.folder_path2)
		IDirButton2.pack()
	    # ================================================


		# ================================================
		# xml格納場所
		# ================================================
		# 「ファイル参照」ラベルの作成
		# IFileLabel = tk.Label(self, text = "ファイル参照＞＞",  padx = 5, pady = 2)
		# IFileLabel.pack()

		# # 「ファイル参照」エントリーの作成
		# self.entry3 = StringVar()
		# self.IFileEntry = tk.Entry(self, textvariable = self.entry3, width = 30)
		# self.IFileEntry.pack()

		# # 「ファイル参照」ボタンの作成
		# IFileButton = tk.Button(self, text="参照", command = self.file_path)
		# IFileButton.pack()
		# ================================================

		# 実行ボタン
		submit_button = tk.Button(self)
		submit_button['text'] = '実行'
		submit_button['command'] = self.face_recognition
		submit_button.pack()

		# メッセージ出力
		# self.message = tk.Message(self)
		# self.message['width'] = 400
		# self.message.pack()

	#文字の読み取り 
	# def input_handler(self):
	# 	text = self.IDirEntry.get()
	# 	self.message['text'] = text

	# 参照フォルダのパス指定
	def folder_path(self):
		# 解析対象のフォルダ
		iDir = os.path.abspath(os.path.dirname(__file__))
		iDirPath = filedialog.askdirectory(initialdir = iDir)
		self.entry1.set(iDirPath)

	# 解析結果のフォルダのパス指定
	def folder_path2(self):
		iDir = os.path.abspath(os.path.dirname(__file__))
		iDirPath = filedialog.askdirectory(initialdir = iDir)
		self.entry2.set(iDirPath)

	# def file_path(self):
	# 	fTyp = [("", "*")]
	# 	iFile = os.path.abspath(os.path.dirname(__file__))
	# 	iFilePath = filedialog.askopenfilename(filetypes = fTyp, initialdir = iFile)
	# 	self.entry3.set(iFilePath)


	# 顔認識のプログラム
	def face_recognition(self):
		# 解析対象の格納先
		folder = self.IDirEntry.get()
		# 解析結果の格納先
		output = self.IDirEntry2.get()
		# xmlファイルの格納先
		# xml = self.IFileEntry.get()

		# 画像のファイル名を取得
		images = glob.glob(folder + '/*')

		for i in images:
		    # 画像を読み込む
			image = cv2.imread(i)

			image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

			# face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + xml)
			face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

			face = face_cascade.detectMultiScale(image_gray)

			# 顔の周りに線を描画
			for x, y, w, h in face:
			    cv2.rectangle(image, (x, y), (x + w, y + h), (255, 0 ,0), 2)

			# 画像を保存
			file_name = os.path.splitext(os.path.basename(i)) 
			path = file_name[0]  + '_after' + file_name[1]

			cv2.imwrite(path , image)

			# img_afterに画像を移動
			new_path = shutil.move(path, output)

		# 処理完了後のダイアログ
		messagebox.showinfo('メッセージ', '解析が完了しました。')

		self.root.destroy
		sys.exit()
		

root = tk.Tk()
root.title('顔認識アプリ')
root.geometry('450x350')
app = Application(root = root)

# アプリの起動
app.mainloop()
