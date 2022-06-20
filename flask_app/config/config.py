import pymysql.cursors

connection = pymysql.connect(host = 'localhost',
                                    user = 'root', 
                                    password = '', 
                                    db = 'nyc',
                                    charset = 'utf8mb4',
                                    cursorclass = pymysql.cursors.DictCursor,
                                    autocommit = True)
        # establish the connection to the database
conn = connection.cursor()