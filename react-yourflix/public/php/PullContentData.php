<?php
    $rest_json = file_get_contents("php://input");
    $_POST = json_decode($rest_json, true);

    $contentID = $_POST['Id'];

    $db = new SQLite3('/usr/share/yourflix/yourflix.db');
    $result = $db->query('SELECT * FROM Content_Db WHERE Content_Db.Id = '.$contentID);
    $currVideo = $result->fetchArray();
    $result = $db->query('SELECT Content_Db.Id FROM Content_Db WHERE Content_Db.Parent_Id = '.$currVideo['Parent_Id'].' ORDER BY Content_Db.Name COLLATE NOCASE ASC');
    $listOfSiblings = [];
    while($content = $result->fetchArray()) 
    {
        array_push($listOfSiblings, json_encode($content));
    }
    $returnArray = [$currVideo, $listOfSiblings];
    echo json_encode($returnArray);
    $db->close();
?>