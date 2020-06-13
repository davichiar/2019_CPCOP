<?php
    $con = mysqli_connect("localhost", "davichiar1", "a1b1c1**", "davichiar1");
    mysqli_query($con, "SET NAMES utf8");

    $userID = $_POST["userID"];

    $statement = mysqli_prepare($con, "SELECT userID FROM MV_USER WHERE userID = ?");
    // 위에서 *로 하면 mysqli_stmt_bind_result에서 에러가 나서 정정함
    mysqli_stmt_bind_param($statement, "s", $userID);
    mysqli_stmt_execute($statement);

    mysqli_stmt_store_result($statement);
    mysqli_stmt_bind_result($statement, $userID);

    $response = array();
    $response["success"] = true;

    while(mysqli_stmt_fetch($statement)) {
        $response["success"] = false;
        $response["userID"] = $userID;
    }

    echo json_encode($response);
?>