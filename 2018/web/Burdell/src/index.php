 <?php 

include("config.php");

$username = isset($_POST["username"]) ? $_POST["username"]: "" ;
$password = isset($_POST["password"]) ? $_POST["password"]: "" ;


if (!$link = mysql_connect($db_host, $db_user, $db_password)) 
    die('<pre>Could not connect to mysql</pre>');    


if (!mysql_select_db($db_name, $link))
    die('<pre>Could not select database</pre>');

$sql = "SELECT * FROM users WHERE username = '".$username."' and password = '".$password."'";

if($result = mysql_query($sql, $link)) {
    if($row = mysql_fetch_row($result)){   
        if ($row[0] === "burdell"){
            echo "FLAG: ".$flag;
        } else {
			die("welcome ".$row[0]."! <br>");
			die("srry but this page is for burdell only");
        }
    } else if(isset($_POST["username"]) && isset($_POST["password"]))
        die("invalid login");
} else if(isset($_POST["username"]) && isset($_POST["password"])){
    die("error.. thx alot<br>");
  }
mysql_free_result($result);

?>
<html lang="en">
  <head>
      <title>HackGT | HackGT Login</title>
    <meta http-equiv="refresh" content="3595" />
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
      
      
      
      
          <link rel="stylesheet" type="text/css" href="./responsive.css">
      
      <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />

      <link rel="icon" href="/cas/favicon.ico" type="image/x-icon" />

  </head>
  <body id="cas" class="fl-theme-iphone">
  
  
  
    <div id="prefooter">
      <header>
        <div id="identity">
          <h1 id="gt-logo">
            <a title="HackGT" rel="home" href="/">
              <img src="logo-gt-cropped.png" alt="HackGT" />
           </a>
          </h1>
          <h2 id="site-title">
            HackGT Login Service
          </h2>
        </div>
        <section id="primary-menus"> </section>
      </header>

      <section id="main">
        <div class="content">





  <form id="fm1" class="fm-v clearfix" action="index.php" method="post">
    
    <div class="box fl-panel" id="login">
            <h2><span class="enter">Enter your HackGT Account and Password</span></h2>
            
            
            
            
            
            
            
            <div class="requested_by">Login requested by: <b>hackgt.gatech.edu</b></div>
            
            
                    <div class="row fl-controls-left">
                        <label for="username" class="fl-label"><span class="accesskey">G</span>T Account:</label>
            <input id="username" name="username" class="required" tabindex="1" accesskey="n" type="text" value="" size="25" autocomplete="false"/>
            
                    </div>
                    <div class="row fl-controls-left">
                        <label for="password" class="fl-label"><span class="accesskey">P</span>assword:</label>
            <input id="password" name="password" class="required" tabindex="2" accesskey="p" type="password" value="" size="25" autocomplete="off"/>
                    </div>
                    <div class="buttons row btn-row">

                        <input class="button btn-submit" name="submit" accesskey="l" value="LOGIN" tabindex="4" type="submit" />
                    </div>
          </div>
        </form>



        </div>
      </section>
    </div>
  
      <section id="superfooter">
        <div id="superfooter-content">&nbsp;</div>
      </section>
      <footer id="footer">
        <div id="footer-content">

          <p>
        
        
        &copy;
        2018 HackGT

          </p>
        </div>
      </footer>

    
    </body>
</html>



