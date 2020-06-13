<?php 
    $con = mysqli_connect("localhost", "davichiar1", "a1b1c1**", "davichiar1");
    mysqli_query($con, "SET NAMES utf8");

    $result = mysqli_query($con, "SELECT * FROM MV_CONTEXT");
    $response = array();
    while($row = mysqli_fetch_array($result))
      array_push($response, array("ID" => $row[0], "TITLE" => $row[1], "LINK" => $row[2], "IMGLINK" => $row[3], "CONTEXT1" => $row[4], "DATE" => $row[5], "NICNAME" => $row[6], "ADD_TEXT" => $row[7], "ACTIVE_TEXT" => $row[8], "TEXT" => $row[9]));

    //다음과 같이 출력함
    //"response":["noticeContent":"NOTICE NUMBER1","noticeName":"GAKARI","noticeDate":"2017-01-03",
    //"noticeContent":"NOTICE NUMBER1","noticeName":"GAKARI","noticeDate":"2017-01-02",
    //"noticeContent":"NOTICE NUMBER1","noticeName":"GAKARI","noticeDate":"2017-01-01"]
    echo json_encode(array("response" => $response));
    mysqli_close($con);
?>