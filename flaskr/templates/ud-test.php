<!doctype html>
<html lang="en">
<head>
  <!-- Required meta tags -->
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">

  <!-- Bootstrap CSS -->
  <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/css/bootstrap.min.css" integrity="sha384-JcKb8q3iqJ61gNV9KGb8thSsNjpSL0n8PARn9HuZOnIxN0hoP+VmmDGMN5t9UJ0Z" crossorigin="anonymous">
  <link rel="stylesheet" type="text/css" href={{ url_for('static', filename='style.css') }}>

  <!-- import font -->
  <link href="https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,100;0,300;0,400;0,500;0,700;0,900;1,100;1,300;1,400;1,500;1,700;1,900&display=swap" rel="stylesheet">

  <title>Dashboard</title>
</head>
<body>
  <!--Navbar-->
  <nav class="navbar navbar-expand-lg navbar-light" style="background-color: #86E49E;">
    <a class="navbar-brand" href="{{ url_for('home') }}"><img src ="static/logo.png" class="img-fluid" width="30" height="30" alt="">(Yo)UB Sustainable</a>
    <button class="navbar-toggler" type="button" data-toggle="collapse" data-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
      <span class="navbar-toggler-icon"></span>
    </button>
    <div class="collapse navbar-collapse" id="navbarNav">
      <ul class="navbar-nav mr-auto">
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('home') }}">Home</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('chall') }}">Challenges</a>
        </li>
        <li class="nav-item">
          <a class="nav-link" href="{{ url_for('friend') }}">Friends</a>
        </li>
        <li class="nav-item active">
          <a class="nav-link" href="#">Dashboard<span class="sr-only">(current)</span></a>
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
  <!-- mysql://b2cb10b2b21b72:1b8b9cc5@us-cdbr-east-02.cleardb.com/heroku_318469e412eb0ae?reconnect=true -->
  <?php
  $dbHost = 'us-cdbr-east-02.cleardb.com';
  $dbUser = 'b2cb10b2b21b72';
  $dbPass = '1b8b9cc5';
  $dbName = 'heroku_318469e412eb0ae'

  $conn = new mysqli($dbHost,$dbUser,$dbPass,$dbName);
  if (!$conn) {
    die('Could not connect: ' . mysql_error());
  }

  // SAVED CHALLENGES
  $savedQ = "SELECT saved FROM dash WHERE user='test'";
  $saved = $conn->query($savedQ);
  $rowS = $saved->fetch_assoc();
  $s = $rowS["saved"];
  $sList = explode('|', $s);

  // PROGRESS CHALLENGES
  $progressQ = "SELECT progress FROM dash WHERE user='test'";
  $progress = $conn->query($progressQ);
  $rowP = $progress->fetch_assoc();
  $p = $rowP["progress"];
  $pList = explode('|', $p);

  // COMPLETED CHALLENGES
  $completedQ = "SELECT completed FROM dash WHERE user='test'";
  $completed = $conn->query($completedQ);
  $rowC = $completed->fetch_assoc();
  $c = $rowC["completed"];
  $cList = explode('|', $c);
  ?>

  {% if session['logged_in'] == True %}
  <div class="container">
    <div class="container">
      <div class="row">
        <div class="col-1">
        </div>
        <div class="col-6">
          <h1>{{session.fname}} {{session.lname}}</h1>
          <p> Eco Superstar</p>
          <div class="row">
            <div class="col">
              <h2> <?php echo sizeof($cList) ?> </h2>
              <p>completed</p>
            </div>
            <div class="col">
              <h2> <?php echo sizeof($pList) ?> </h2>
              <p>in progress</p>
            </div>
          </div>
        </div>
        <div class="col-4">
          <img src ="https://via.placeholder.com/200" class="pfp img-thumbnail">
        </div>
        <div class="col-1">
        </div>
      </div>
    </div>
    <br>

    <!-- IN PROGRESS SECTION -->
    <div class="container">
      <div class="row greenback">
        <h3>IN PROGRESS</h3>
      </div>
      <div class="row greenborder">
        <?php foreach ($pList as $i => $pitem): ?>
          <div class="col-4">
            <p> <?php echo $pitem; ?> </p>
          </div><div class="col-8">
            <div class="progress">
              <div class="progress-bar progress-bar-striped progress-bar-animated bg-secondary" role="progressbar" aria-valuenow="75" aria-valuemin="0" aria-valuemax="100" style="width: 75%">
              </div>
            </div>
          </div>
        <?php endforeach; ?>
      </div>
    </div>
    <br>

    <!-- SAVED SECTION -->
    <div class="container">
      <div class="row greenback">
        <h3>SAVED</h3>
      </div>
      <div class="row greenborder">
        <?php foreach ($sList as $i => $sitem): ?>
          <div class="col-3 ctsize">
            <p> <?php echo $sitem; ?> </p>
        <?php endforeach; ?>
      </div>
    </div>
    <br>

    <!-- COMPLETED SECTION -->
    <div class="container">
      <div class="row greenback">
        <h3>COMPLETED</h3>
      </div>
      <div class="row greenborder">
        <?php
        <? php foreach ($cList as $i => $citem): ?>
          <div class="col-3 ctsize">
            <p> <?php echo $citem; ?> </p>
            <svg width="50" height="50" viewBox="0 0 16 16" class="bi bi-star-fill btmspc" fill="gray" xmlns="http://www.w3.org/2000/svg"><path d="M3.612 15.443c-.386.198-.824-.149-.746-.592l.83-4.73L.173 6.765c-.329-.314-.158-.888.283-.95l4.898-.696L7.538.792c.197-.39.73-.39.927 0l2.184 4.327 4.898.696c.441.062.612.636.283.95l-3.523 3.356.83 4.73c.078.443-.36.79-.746.592L8 13.187l-4.389 2.256z"/>
            </svg>
          </div>
        <?php endforeach ?>
      </div>
    </div>

    <br>
    <div class = "row">
      <a href="#" class="btn btn-secondary col-12">Sign Out</a>
    </div>
  </div>

  {% else %}
  <h2>Please log in to view your dashboard!</h2>
  {% endif %}
  <!-- Optional JavaScript -->
  <!-- jQuery first, then Popper.js, then Bootstrap JS -->
  <script src="https://code.jquery.com/jquery-3.5.1.slim.min.js" integrity="sha384-DfXdz2htPH0lsSSs5nCTpuj/zy4C+OGpamoFVy38MVBnE+IbbVYUew+OrCXaRkfj" crossorigin="anonymous"></script>
  <script src="https://cdn.jsdelivr.net/npm/popper.js@1.16.1/dist/umd/popper.min.js" integrity="sha384-9/reFTGAW83EW2RDu2S0VKaIzap3H66lZH81PoYlFhbGU+6BZp6G7niu735Sk7lN" crossorigin="anonymous"></script>
  <script src="https://stackpath.bootstrapcdn.com/bootstrap/4.5.2/js/bootstrap.min.js" integrity="sha384-B4gt1jrGC7Jh4AgTPSdUtOBvfO8shuf57BaghqFfPlYxofvL8/KUEfYiJOMMV+rV" crossorigin="anonymous"></script>
</body>
</html>
