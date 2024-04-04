import sqlite3

conn = sqlite3.connect("./DB/Books.db")
cur = conn.cursor()
conn.text_factory=str

cur.execute("create table books("
"id integer primary key autoincrement,"
"name text,"
"auther text,"
"evaluation text,"
"status text,"
"start_date text,"
"end_date text, "
"pages integer,"
"url text,"
"comment text)")

cur.execute("insert into books ("
"name,"
"auther,"
"evaluation,"
"status,"
"start_date,"
"end_date,"
"pages,"
"url,"
"comment"
") values ("
"'プログラマー脳',"
"'Felienne Hermans',"
"'★★★★★7',"
"'3:読了',"
"'2024/02/20',"
"'2024/03/20',"
"260,"
"'',"
"'秀逸')"
)

conn.commit()
conn.close()
