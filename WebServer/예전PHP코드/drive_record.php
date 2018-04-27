<?php
// MySQL 데이터베이스 연결
$link = mysqli_connect('localhost', 'root', 'doraemon', 'doraemon');
  
// 연결 오류 발생 시 스크립트 종료
if (mysqli_connect_errno()) {
	die('Connect Error: '.mysqli_connect_error());
}

$result_array = array();
$usr_id 	= $_POST["usr_id"];
$start_time = $_POST["start_time"];
$end_time 	= $_POST["end_time"];

$query ="SELECT * FROM car,record WHERE USR_ID='$usr_id' and START_TIME between '$start_time 00:00:00' and '$end_time 23:59:59';";
// 쿼리문 전송
if ($result = mysqli_query($link, $query)) 
{
	// 레코드 출력
	while ($row = mysqli_fetch_object($result))
	{
		$result_array[] = $row;
	}
	//json
	echo json_encode($result_array);
	// 메모리 정리
	mysqli_free_result($result);
}
else
{
	echo "-1";
}
// 접속 종료
mysqli_close($link);

