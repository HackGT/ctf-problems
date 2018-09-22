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

    $flag = 'hackgt{tupl3_m1ght_b3_f4ke_but_burdells_n0t}';

    error_reporting(0);
?>