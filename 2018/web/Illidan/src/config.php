<?php
   try {
        $db_host = 'localhost';
        $db_user = 'root';
        $db_password = 'superlongpasswordxdddddddd';
        $db_name = 'user';
    } catch (PDOException $e) {
        echo "Couldn't connect to DB! https://i.imgur.com/6NfmQ.jpg";
        die($e);
    }

    error_reporting(0);
?>