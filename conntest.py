import psycopg2

conn = psycopg2.connect(dbname="there_n_back", user="postgres", password="postgres",port=5432)
conn.close()