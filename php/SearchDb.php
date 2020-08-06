<?php

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    $rest_json = file_get_contents("php://input");
    $_POST = json_decode($rest_json, true);
    
    $db = new SQLite3('/usr/share/yourflix/yourflix.db');
    $result = $db->query('SELECT * FROM Program_Db ORDER BY Name');
    
    $listOfPrograms = [];
    $counter = $_POST['limit'];
    while($content = $result->fetchArray()) 
    {
        $search = stripos($content['Name'], $_POST['query']);
        if($search !== false)
        {
            array_push($listOfPrograms,json_encode($content));
            $counter--;
        }
        if($counter <= 0)
        {
            break;
        }
    }
    echo json_encode($listOfPrograms);
    $db->close();

}


?>
