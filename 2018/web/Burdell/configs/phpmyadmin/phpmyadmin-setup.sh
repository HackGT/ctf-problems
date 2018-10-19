#!/bin/bash

# Start MySQL
/usr/bin/mysqld_safe > /dev/null 2>&1 &

# Wait until the MySQL server is available.
sleep 5

# Create the phpmyadmin storage configuration database.
mysql -uroot -psuperlongpasswordxdddddddd -e "CREATE DATABASE phpmyadmin; GRANT ALL PRIVILEGES ON phpmyadmin.* TO 'root'@'localhost' IDENTIFIED BY 'root'; FLUSH PRIVILEGES;"
#!/bin/bash
mysql -uroot -psuperlongpasswordxdddddddd -e "CREATE DATABASE user"
mysql -uroot -psuperlongpasswordxdddddddd -e "USE user; CREATE TABLE users(username VARCHAR (20), password VARCHAR (20),asdf1 VARCHAR (20),asdf2 VARCHAR (20),asdf3 VARCHAR (20), PRIMARY KEY (username));"
mysql -uroot -psuperlongpasswordxdddddddd -e "USE user; SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO'; DELETE FROM users; INSERT INTO users VALUES ('administrator', SHA1('asdfhunter2'),'asdf','asdf','asdf')"
mysql -uroot -psuperlongpasswordxdddddddd -e "USE user; SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO'; INSERT INTO users VALUES ('burdell', SHA1('Hfoiwa92hJELnwp2Owj5t'), 'i', 'am', 'glorious');"
mysql -uroot -psuperlongpasswordxdddddddd -e "USE user; SET SQL_MODE = 'NO_AUTO_VALUE_ON_ZERO';"

# Import the configuration storage database.
gunzip < /usr/share/doc/phpmyadmin/examples/create_tables.sql.gz | mysql -uroot -psuperlongpasswordxdddddddd phpmyadmin
# Shutdown the server.
mysqladmin -uroot -psuperlongpasswordxdddddddd shutdown
