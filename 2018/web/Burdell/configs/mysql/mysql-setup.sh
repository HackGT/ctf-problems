#!/bin/bash

# Start MySQL
/usr/bin/mysqld_safe > /dev/null 2>&1 &

# Wait until the MySQL server is available.
sleep 5

# Change the MySQL root password
mysqladmin -uroot -proot password superlongpasswordxdddddddd

#!/bin/bash


# Shutdown the server.
mysqladmin -uroot -psuperlongpasswordxdddddddd shutdown
