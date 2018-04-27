<?php
// MySQL 데이터베이스 연결
$link = mysqli_connect('localhost', 'root', 'doraemon', 'doraemon');
  
// 연결 오류 발생 시 스크립트 종료
if (mysqli_connect_errno()) {
	die('Connect Error: '.mysqli_connect_error());
}

$result_array = array();
$id 	= $_POST["id"];


$query ="SELECT CAR_NAME FROM car WHERE USR_ID = '$id';";
// 쿼리문 전송
if ($result = mysqli_query($link, $query)) 
{

	// 레코드 출력
	while ($row = mysqli_fetch_object($result))
	{
		$result_array[] = $row;
	}
	//json
//	echo $result_array;
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

