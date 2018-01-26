<?php
// MySQL 데이터베이스 연결
$link = mysqli_connect('localhost', 'root', '1234', 'pidb');
  
// 연결 오류 발생 시 스크립트 종료
if (mysqli_connect_errno()) {
	die('Connect Error: '.mysqli_connect_error());
}

$result_array = array();
// 쿼리문 전송
if ($result = mysqli_query($link, 'SELECT * FROM student')) {
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
// 접속 종료
mysqli_close($link);
