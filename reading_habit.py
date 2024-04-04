import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkcalendar import DateEntry
import sqlite3
from lib_arao import BookSearch_in_AraoLib
import lib_list


#プルダウンの中身
EVALUATION_STAR = ("－", "★☆☆☆☆", "★★☆☆☆", "★★★☆☆", "★★★★☆", "★★★★★")
STATUS_VALUE = ("0:欲しい", "1:購入済、未読", "2:読書中", "3:読了", "4:積読","5:処分")

class MainWindow(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master.title("Reading Habit")

        # データベースとの接続
        self.db = DatabaseSession()

        # Bookのインスタンス化
        self.book = Book()

        # ウィンドウを閉じられたときに処理を実行
        #self.master.protocol("WM_DELETE_WINDOW", self.close_window)

        self.set_widget()

    def set_widget(self):
    #1行目
    # アプリタイトル
        label_title = ttk.Label(self.master, text="読書習慣アプリ", font=24,anchor=tk.CENTER)
        label_title.grid(row=0, column=0, columnspan=3,
                     ipadx=20, ipady=5, pady=10)

    # 2行目
    # 追加ボタン
        btn_add = tk.Button(self.master, text="追加",font=14, bg="#7d66b3",fg="white")
        btn_add.grid(row=1, column=0)
        btn_add.config(command=self.add)
    # 更新ボタン
        btn_update = tk.Button(self.master, text="更新",font=14, bg="#7d66b3",fg="white")
        btn_update.grid(row=1, column=1)
        btn_update.config(command=self.update)
    # 削除ボタン
        btn_delete = tk.Button(self.master, text="削除",font=14, bg="#7d66b3",fg="white")
        btn_delete.grid(row=1, column=2)
        btn_delete.config(command=self.delete)

    # ==================== 3行目
    # フレーム
        frame = tk.Frame(self.master, width=700, height=200)
        frame.grid_propagate(False)
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        frame.grid(row=2, column=0, columnspan=3,
               padx=5, pady=5, ipadx=5, ipady=5)
    #表
        columns=("id","name","auther","evaluation","status",
                "startdate","enddate","pages","url","comment")
        self.table_books=ttk.Treeview(frame,columns=columns,height = 20,
                                     selectmode="browse",show="headings")
        self.table_books.grid(row = 0,column =0 ,sticky=tk.N+tk.S+tk.E+tk.W)
        
    # ヘッダ行の設定
        self.table_books.heading("id", text="id", anchor="center")
        self.table_books.heading("name", text="書籍名", anchor="center")
        self.table_books.heading("auther", text="著者", anchor="center")
        self.table_books.heading("evaluation", text="評価", anchor="center")
        self.table_books.heading("status", text="ステータス", anchor="center")
        self.table_books.heading("startdate", text="開始日", anchor="center")
        self.table_books.heading("enddate", text="読了日", anchor="center")
        self.table_books.heading("pages", text="ページ数", anchor="center")
        self.table_books.heading("url", text="URL", anchor="center")
        self.table_books.heading("comment", text="コメント", anchor="center")

    # ヘッダーのスタイルを定義
        style = ttk.Style()
        style.configure("Treeview.Heading", font=13,)

    # ダミーデータ
        self.table_books.insert(parent="", index="end", iid=0, values=(
            0, "プリンシプル　オブ　プログラミング", "上田勉", "－", "", "2023/12/01", "2023/12/02", "2023/12/25",
            999, "https://www.shuwasystem.co.jp/book/9784798046143.html", "コメント"))
        self.id = -1
        
    #縦スクロールバー
        vscrollbar = ttk.Scrollbar(frame,orient=tk.VERTICAL)
        vscrollbar.grid(row = 0, column = 1, sticky=tk.NS)
        vscrollbar.config(command=self.table_books.yview)
        self.table_books.config(yscrollcommand=vscrollbar.set)

    #横スクロールバー
        hscrollbar = ttk.Scrollbar(frame,orient=tk.HORIZONTAL)
        hscrollbar.grid(row = 1, column = 0, sticky=tk.EW)
        hscrollbar.config(command=self.table_books.xview)
        self.table_books.config(xscrollcommand=hscrollbar.set)

    #4行目 福岡図書館一覧
        btn_FukLib_list = tk.Button(self.master, text="福岡図書館一覧",font=12, bg="#a492d3",fg="purple")
        btn_FukLib_list.grid(row=4, column=0,pady=5)
        #btn_FukLib_list.config(command=self.)

    #地図
        btn_FukLib_Map = tk.Button(self.master, text="地図",font=12, bg="#a492d3",fg="purple")
        btn_FukLib_Map.grid(row=4, column=1,pady=5)
        #btn_FukLib_Map.config(command=self.)

    #荒尾図書館
        def botton_clicked_a():
            BookSearch_in_AraoLib()
        btn_Arao_lib = tk.Button(self.master, text="荒尾図書館",font=12, bg="#a492d3",fg="purple",command=botton_clicked_a)
        btn_Arao_lib.grid(row=4, column=2,pady=5)
       


        
        #btn_Arao_lib.config(command=button_clicked.BookSearch_in_AraoLib)
        
    
    #スタイルの適用
        style=ttk.Style()
        style.theme_use("classic")

    def add(self):
        # サブウィンドウの表示
        sub_window = SubWindow(self, "add")
    
    def update(self):
        # リストが選択されている場合にサブウィンドウを表示
        sub_window = SubWindow(self, "update")

    def delete(self):
    # リストが選択されている場合に確認メッセージを表示
        if self.id != -1:
            confirm = messagebox.askyesno("削除確認", "削除して良いですか？")
            if confirm:
            # 「はい」が押されてたら削除
                self.book.delete(self.db, self.id)
            # リストを再描画
                self.display_list()

    
    def select_record(self, e):
        # 選択行の取得
        selected_id = self.table_books.focus()
        if selected_id != "":
        # 選択行のレコードの値を取得
            values = self.table_books.item(selected_id, "values")
            self.id = values[0]

    def display_list(self):
    # 既存レコードの削除
        for row in self.table_books.get_children():
            self.table_books.delete(row)

    # 検索
        books = self.book.select_all(self.db)

    # レコードの追加
        for index, book in enumerate(books):
            self.table_books.insert(
                parent="", index="end", iid=index,
                values=(book.id,
                        book.name,
                        book.auther,
                        book.evaluation,
                        book.status,
                        book.start_date,
                        book.end_date,
                        book.pages,
                        book.url,
                        book.comment))

    # リスト選択のID値を初期化(未選択状態)
        self.id = -1

    # 再描画
        self.master.update()

class SubWindow: 
    def __init__(self, master, mode):
        # パラメ-タの受け取り
        self.master = master
        self.mode = mode
        self.db = master.db
        self.id = master.id
        self.book = master.book

        # サブウィンドウの表示
        #sub_window = SubWindow(self, "add")

        # サブウィンドウの描画
        self.sub_window = tk.Toplevel()
        self.sub_window.title("詳細画面")
        self.sub_window.grab_set()

        if mode == "add":
            self.book_info = Book()
        else:
            self.book_info = self.book.select(self.db, self.id)

        # ウィンドウを閉じられたときに処理を実行
        self.sub_window.protocol("WM_DELETE_WINDOW", self.close_window)

        # 全ウィジェットの描画
        self.set_widget()

    def close_window(self):
        # リストの再描画
        self.master.display_list()

        # サブウィンドウを閉じる
        self.sub_window.destroy()

    def set_widget(self):
        # 1行目
        # 書籍名ラベル
        label_book_title = tk.Label(self.sub_window, text="書籍名：",font=14)
        label_book_title.grid(row=0, column=0, padx=5, pady=5, sticky=tk.E)
        # 書籍名入力欄
        self.str_book_title = tk.StringVar()
        text_book_title = ttk.Entry(self.sub_window, width=50)
        text_book_title.grid(row=0, column=1, columnspan=2, sticky=tk.W)
        text_book_title.config(textvariable=self.str_book_title)
        self.str_book_title.set(self.book_info.name)

        # 著者ラベル
        label_author = ttk.Label(self.sub_window, text="著者：")
        label_author.grid(row=0, column=3, padx=5, pady=5, sticky=tk.E)
        # 著者入力欄
        self.str_auther = tk.StringVar()
        text_author = ttk.Entry(self.sub_window, width=20)
        text_author.grid(row=0, column=4, columnspan=2, sticky=tk.W)
        text_author.config(textvariable=self.str_auther)
        self.str_auther.set(self.book_info.auther)

        # 2行目
        # 評価ラベル
        label_evaluation = ttk.Label(self.sub_window, text="評価：")
        label_evaluation.grid(row=1, column=0, padx=5, pady=5, sticky=tk.E)
        # 評価ドロップダウンリスト
        self.str_evaluation = tk.StringVar()
        combo_evaluation = ttk.Combobox(
            self.sub_window, values=EVALUATION_STAR, state="readonly")
        combo_evaluation.grid(row=1, column=1, columnspan=2, sticky=tk.W)
        combo_evaluation.config(textvariable=self.str_evaluation)
        combo_evaluation.set(self.book_info.evaluation)

        # ステータスラベル
        label_status = ttk.Label(self.sub_window, text="ステータス：")
        label_status.grid(row=1, column=3, padx=5, pady=5, sticky=tk.E)
        # ステータスドロップダウンリスト
        self.str_status = tk.StringVar()
        combo_status = ttk.Combobox(
            self.sub_window, values=STATUS_VALUE, state="readonly")
        combo_status.grid(row=1, column=4, columnspan=2, sticky=tk.W)
        combo_status.config(textvariable=self.str_status)
        combo_status.set(self.book_info.status)

        # 3行
        # 開始日ラベル
        label_start_date = ttk.Label(self.sub_window, text="開始日：")
        label_start_date.grid(row=2, column=3, padx=5, sticky=tk.E)
        # 開始日カレンダ
        self.str_start_date = tk.StringVar()
        self.date_start = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_start.grid(row=2, column=4, sticky=tk.W)
        self.date_start.config(textvariable=self.str_start_date)
        self.str_start_date.set(self.book_info.start_date)
        # 開始日クリアボタン
        btn_clear_start = ttk.Button(self.sub_window, text="Clear")
        btn_clear_start.grid(row=2, column=5, sticky=tk.W)
        btn_clear_start.config(
            command=lambda: self.date_start.delete(0, "end"))

        # 4行目
        # 読了日ラベル
        label_finish_date = ttk.Label(self.sub_window, text="読了日：")
        label_finish_date.grid(row=3, column=0, padx=5, pady=5, sticky=tk.E)
        # 読了日カレンダ
        self.str_end_date = tk.StringVar()
        self.date_end = DateEntry(self.sub_window, showweeknumbers=False)
        self.date_end.grid(row=3, column=1, sticky=tk.W)
        self.date_end.config(textvariable=self.str_end_date)
        self.str_end_date.set(self.book_info.end_date)
        # 読了日クリアボタン
        btn_clear_end = ttk.Button(self.sub_window, text="Clear")
        btn_clear_end.grid(row=3, column=2, sticky=tk.W)
        btn_clear_end.config(command=lambda: self.date_end.delete(0, "end"))

        # 総ページ数ラベル
        label_total_page = ttk.Label(self.sub_window, text="総ページ数：")
        label_total_page.grid(row=3, column=3, padx=5, sticky=tk.E)
        # 総ページ数入力欄
        self.str_pages = tk.StringVar()
        text_total_page = ttk.Entry(self.sub_window, width=10)
        text_total_page.grid(row=3, column=4, columnspan=2, sticky=tk.W)
        text_total_page.config(textvariable=self.str_pages)
        self.str_pages.set(self.book_info.pages)

        # ==================== 5行目
        # URLラベル
        label_url = ttk.Label(self.sub_window, text="URL：")
        label_url.grid(row=4, column=0, padx=5, pady=5, sticky=tk.E)
        # URL入力欄
        self.str_url = tk.StringVar()
        text_url = ttk.Entry(self.sub_window, width=100)
        text_url.grid(row=4, column=1, columnspan=5, sticky=tk.W)
        text_url.config(textvariable=self.str_url)
        self.str_url.set(self.book_info.url)

        # ==================== 6行目
        # コメントラベル
        label_comment = ttk.Label(self.sub_window, text="コメント：")
        label_comment.grid(row=5, column=0, padx=5, pady=5, sticky=tk.E)

        # フレーム
        frame = ttk.Frame(self.sub_window)
        frame.grid(row=5, column=1, columnspan=5, padx=5, pady=5, sticky=tk.W)

        # コメント入力欄
        self.text_comment = tk.Text(frame, width=100, height=5)
        self.text_comment.pack(side=tk.LEFT)
        self.text_comment.insert(tk.END, self.book_info.comment)

        # 縦スクロールバー
        vscrollbar = ttk.Scrollbar(frame, orient=tk.VERTICAL)
        vscrollbar.pack(side=tk.LEFT, fill=tk.Y)
        vscrollbar.config(command=self.text_comment.yview)
        self.text_comment.config(yscrollcommand=vscrollbar.set)

        # 7行目
        if self.mode == "add":
            btn_add = ttk.Button(self.sub_window, text="追加")
            btn_add.grid(row=6, column=1, padx=5, pady=5, sticky=tk.E)
            btn_add.config(command=self.add)
        else:
            btn_update = ttk.Button(self.sub_window, text="更新")
            btn_update.grid(row=6, column=4, padx=5, pady=5, sticky=tk.E)
            btn_update.config(command=self.update)

    def get_input_data(self):
        self.book_info.name = self.str_book_title.get()
        self.book_info.auther = self.str_auther.get()
        self.book_info.evaluation = self.str_evaluation.get()
        self.book_info.status = self.str_status.get()
        self.book_info.start_date = self.str_start_date.get()
        self.book_info.end_date = self.str_end_date.get()
        self.book_info.pages = self.str_pages.get()
        self.book_info.url = self.str_url.get()
        self.book_info.comment = self.text_comment.get("1.0", "end")

    def add(self):
        # 入力値の取り出し
        self.get_input_data()

        # insert実行
        self.book_info.insert(self.db)

        # リストの再描画
        self.master.display_list()

        # サブウィンドウを閉じる
        self.sub_window.destroy()

    def update(self):
        # 入力値の取り出し
        self.get_input_data()

        # update実行
        self.book_info.update(self.db)
        
        
        # リストの再描画
        self.master.display_list()

        # サブウィンドウを閉じる
        self.sub_window.destroy()

class Book:
    def __init__(self):
        self.id = -1
        self.name= ""
        self.auther = ""
        self.evaluation = EVALUATION_STAR[0]
        self.status = STATUS_VALUE[1]
        self.start_date = ""
        self.end_date = ""
        self.pages = 0
        self.url = ""
        self.comment = ""

    def select_all(self, db):
        db.cursor.execute("select * from books order by id desc")
        books = []
        for row in db.cursor:
            book = Book()
            book.id = row[0]
            book.name = row[1]
            book.auther = row[2]
            book.evaluation = row[3]
            book.status = row[4]
            book.start_date = row[5]
            book.end_date = row[6]
            book.pages = row[7]
            book.url = row[8]
            book.comment = row[9]

            books.append(book)
        return books

    def select(self, db, id):
        db.cursor.execute(f"select * from books where id={id}")
        result = db.cursor.fetchone()
        book = Book()
        self.book.id = result[0]
        book.name = result[1]
        book.auther = result[2]
        book.evaluation = result[3]
        book.status = result[4]
        book.start_date = result[5]
        book.end_date = result[6]
        book.pages = result[7]
        book.url = result[8]
        book.comment = result[9]

        return book
        

    def insert(self, db):
        db.cursor.execute(f"insert into books (name, auther, evaluation, status,start_date, end_date, pages, url, comment) "
                          f"values ('{self.name}',"
                          f"'{self.auther}',"
                          f"'{self.evaluation}',"
                          f"'{self.status}',"
                          f"'{self.start_date}',"
                          f"'{self.end_date}',"
                          f"{self.pages},"
                          f"'{self.url}',"
                          f"'{self.comment}')")
        db.conn.commit()

    def update(self, db):
        db.cursor.execute(f"update books "
                          f"set name='{self.name}',"
                          f"auther='{self.auther}',"
                          f"evaluation='{self.evaluation}',"
                          f"status='{self.status}',"
                          f"start_date='{self.start_date}',"
                          f"end_date='{self.end_date}',"
                          f"pages={self.pages},"
                          f"url='{self.url}',"
                          f"comment='{self.comment}' "
                          f"where id={self.id}")
        db.conn.commit()

    def delete(self, db, id):
        db.cursor.execute(f"delete from books where id={id}")
        db.conn.commit()

class DatabaseSession:
    def __init__(self):
        self.conn = sqlite3.connect("./db/Books.db")
        print("connected")
        self.cursor = self.conn.cursor()

    def disconnect(self):
        self.connect.close()
        print("disconnected")

if __name__ == "__main__":
    root = tk.Tk()
    root.configure(bg="#e7d6ff")
    mainWindow = MainWindow(master=root)
    mainWindow.mainloop()
    




        


    
