import xlrd
import sqlite3

con=sqlite3.connect('C:/Users/昊/Desktop/leetcode/Django/myweb/movie.sqlite3')
data=xlrd.open_workbook('Data_movie_3.xls')
table=data.sheet_by_name('sheet1')
for i in range(1,table.nrows):
	x=table.row_values(i)
	x.append(x[3])   #数据库表单顺序问题。。。
	x.pop(3)
	x.insert(0,i)
	con.execute("insert into show_movie values (?,?,?,?,?,?,?)", x)
con.commit()