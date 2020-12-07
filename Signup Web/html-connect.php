<?php
// connecting to the database.
$con = mysqli_connect('logs.c7xtjtjv8ph3.ap-south-1.rds.amazonaws.com', 'shubh', 'shubh2003','tasker');
// header("Location: ./index.html");
// Retrieving the records.
$name = $_POST['tb_name'];
$email = $_POST['tb_email'];
$instagram = $_POST['tb_instagram'];
$facebook = $_POST['tb_facebook'];
$password = $_POST['password'];

// database insert SQL code, change accordingly.
$sql = "INSERT INTO users VALUES ('$name','$facebook','$instagram','$email','$password');";

// getting the information from database and checking if available.
$check_name = mysqli_query($con, "SELECT name FROM users where name = '$name'");
if(mysqli_num_rows($check_name) != 0){
    echo'<script>alert("Name already exists");window.location.href="./Prodigy.html";</script>';
}
else{
	// insert in database
	$rs = mysqli_query($con, $sql);
    if($rs){
		echo "<script>alert('***Registeration Successfull***Please Accept Instagram Follow Request from _Prodigy_TIM***Cheer!***');
		    window.location.href='./Prodigy.html';</script>";
    }
}
// exit()
?>