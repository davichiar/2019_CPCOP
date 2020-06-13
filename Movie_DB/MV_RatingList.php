<?php 
    $con = mysqli_connect("localhost", "davichiar1", "a1b1c1**", "davichiar1");
    mysqli_query($con, "SET NAMES utf8");

    $result = mysqli_query($con, "SELECT * FROM MV_RATING");
    $response = array();
    while($row = mysqli_fetch_array($result))
      array_push($response, array("ID" => $row[0], "RATING1" => $row[1], "RATING2" => $row[2], "RATING3" => $row[3]));

    //다음과 같이 출력함
    //"response":["noticeContent":"NOTICE NUMBER1","noticeName":"GAKARI","noticeDate":"2017-01-03",
    //"noticeContent":"NOTICE NUMBER1","noticeName":"GAKARI","noticeDate":"2017-01-02",
    //"noticeContent":"NOTICE NUMBER1","noticeName":"GAKARI","noticeDate":"2017-01-01"]
    echo json_encode(array("response" => $response));
    mysqli_close($con);
?>