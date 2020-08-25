<?php
    
    //$rest_json = file_get_contents("php://input");
    //$_POST = json_decode($rest_json, true);
    //$counter = $_POST['limit'];
    $PROG_ID = 10594;
    
    $db = new SQLite3('/usr/share/yourflix/yourflix.db');
    $result = $db->query('SELECT Content_Db.Id, Content_Db.Name FROM Content_Db LEFT JOIN FileType_Db ON FileType_Db.Id == Content_Db.File_Type WHERE Parent_Id =='.$PROG_ID.' AND FileType_Db.Name=="MP4" ORDER BY Content_Db.Name');
    
    $returnArray = [];
    while($content = $result->fetchArray()) 
    {
        array_push($returnArray,json_encode($content));
    }

    echo json_encode($returnArray);
    $db->close();
?>