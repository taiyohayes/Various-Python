import sqlite3 as sl

db = "minimum-wage.db"
def create(fn):
    f = open(fn, "r")
    header = f.readline().strip().split(",")
    header = header[:7]
    for i in range(len(header)):
        header[i] = "\'" + header[i] + "\'"
    header = ", ".join(header)
    f.close()
    print(header)
    conn = sl.connect(db)
    curs = conn.cursor()
    stmt = "CREATE TABLE min_wage (" + header + ")"
    curs.execute(stmt)
    conn.commit()

    stmts = ["SELECT name FROM sqlite_master WHERE type='table'",
             "pragma table_info(min_wage)"
             ]
    for s in stmts:
        result = curs.execute(s)
        for item in result:
            print(item)

    conn.close()

def store_data(fn, table):
    conn = sl.connect(db)
    curs = conn.cursor()

    f = open(fn, "r")
    header = f.readline().strip().split(",")
    n = 0
    for line in f:
        line = line.strip().split(",")
        line = line[:7]
        newLine = "'" + line[1] + "'"
        line[1] = newLine
        line = ','.join(line)
        print(n, line)
        stmt = "INSERT INTO " + table + " VALUES (" + line + ")"  # combine with DML statment
        curs.execute(stmt)
        n += 1

    f.close()
    conn.commit()
    conn.close()

def main():
    create("Minimum Wage Data.csv")
    store_data("Minimum Wage Data.csv", "min_wage")


if __name__ == "__main__":
    main()
