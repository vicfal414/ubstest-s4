<!doctype html>
<html lang="en">
  <head>
    <!-- Required meta tags -->
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

    <!-- Bootstrap CSS -->
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
    <link rel="stylesheet" type="text/css" href="css/style.css">

    <!-- import font -->
    <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">
    
    <title>New Custom Challenge Page 1</title>
  </head>
  <body>
	<!--Navbar-->
  <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #86E49E;">
    <a class="navbar-brand" href="{{ url_for('home') }}"><img src = "static/logo.png" class="img-fluid" width="30" height="30" alt="">(Yo)UB Sustainable</a>	
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('home') }}">Home</a>
        </li>
        <li class="nav-item active">
          <a class="nav-link" href="{{ url_for('chall') }}">Challenges<span class="sr-only">(current)</span></a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('friend') }}">Friends</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('dash') }}">Dashboard</a>
        </li>
      </ul>
      <ul class="nav navbar-nav navbar-right">
        {% if session['logged_in'] == True %}
          <li>
            <a href="{{ url_for('logout') }}" class="btn btn-outline-danger my-2 my-sm-0">Logout</a>
          </li>
                  {% else %}
          <li>
            <a href="{{ url_for('login') }}" class="btn btn-outline-success my-2 my-sm-0">Log In</a>
          </li>
                  {% endif %}
              </ul>
    </div>
  </nav>	
  <!--end of Navbar--> 

 <!-- Start of PHP -->
  <?php
    $dbHost = 'us-cdbr-east-02.cleardb.com';
    $dbUser = 'b2cb10b2b21b72';
    $dbPass = '1b8b9cc5';
    $dbName = 'heroku_318469e412eb0ae'

    //Set DSN
    $dsn = 'mysql:host='. $dbHost .';dbname='. $dbName;

    // Create a PDO instance
    $pdo = new PDO($dsn, $udbUer, $dbPass);
    $pdo->setAttribute(PDO::ATTR_DEFAULT_FETCH_MODE, PDO::FETCH_OBJ);

    // User Input
    $id = 1;
    #PDO Query

    $sql = 'SELECT * FROM challenges WHERE id = :id';
    $stmt = $pdo->prepare($sql);
    $stmt->execute(['id' => $id]);
    $post = $stmt->fetch();
  ?>
  <!-- End of PHP -->

    <!-- PAGE HEADER SECTION CHALLENGE NAME-->
    <div class="container">
      <div class="row">
        <div class="col-1">
        </div>
        <div class="col-6">
          <h1><?php echo post-> name; ?></h1>
        </div> 
      </div>
      <div class="row greenback">
        <h4>
        </h4>
      </div> 
      <div class="row greenback">
        <h4>
        </h4>
      </div>
    </div>
      <br>
    
    <!-- SHORT DESCRIPTION -->
    <div class="container">
      <div class="row">
        <div class="col-1">
        </div>  
        <div class="col-6">
          <p> <?php echo post->decription; ?> </p>
          <div class-"row">
            <!-- first tag - time! -->
            <div class="col-3 ctsize">
              <a href="#" class="btn btn-secondary btnbtm"><?php echo post-> duration; ?></a>
            </div>
            <!-- second tag - Category -->
            <div class="col-3 ctsize">
              <a href="#" class="btn btn-secondary btnbtm"><?php echo post-> category; ?></a>
            </div>
          </div>
        </div> 
        <!--<div class="col-4">
          <img src ="https://upload.wikimedia.org/wikipedia/commons/2/20/Drinking_straws_2_2018-10-16.jpg" class="img-thumbnail">
        </div>-->
      </div>
      <div class="row greenback">
        <h4>
        </h4>
      </div> 
    </div>
      <br>  

    <!-- The Impact Section-->
    <div class="container">
      <div class="row">
        <div class="col-1">
        </div>
        <div class="col-6">
          <h5>The Impact</h5>
          <p><?php echo post-> impact; ?></p>    
        </div> 
      </div>
    </div>
      <br>
    
    <!-- Helpful Suggestions Section-->
    <div class="container">
      <div class="row">
        <div class="col-1">
        </div>
        <div class="col-6">
          <h5>Helpful Suggestions</h5>
          <p><?php echo post-> suggestions; ?></p> 
          <!--<p>- You can buy large packs online!</p>
          <p>- Simple chage in your lifestlye, one in your bag and one at home.</p>  --> 
        </div> 
      </div>
        <br>
      <!--<div class = "row">
        <a href="#" class="btn btn-secondary col-12">SELECT</a>
      </div> -->
    </div>
      <br>

      

    <!-- Optional JavaScript -->
    <!-- jQuery first, then Popper.js, then Bootstrap JS -->
    <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
    <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
    <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
  </body>
</html>