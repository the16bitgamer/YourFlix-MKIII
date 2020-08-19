<?php
include 'ProgramLink.php';
if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    
    $rest_json = file_get_contents("php://input");
    $_POST = json_decode($rest_json, true);
    
    $db = new SQLite3('/usr/share/yourflix/yourflix.db');
    $result = $db->query('SELECT * FROM Program_Db ORDER BY Name');
    
    $listOfPrograms = [];
    $listOfProgLink = [];
    $counter = $_POST['limit'];
    while($content = $result->fetchArray()) 
    {
        $search = stripos($content['Name'], $_POST['query']);
        if($search !== false)
        {
            $progLink = GetProgramLink($db,$content['Folder_Id']);
            array_push($listOfProgLink,json_encode($progLink));
            array_push($listOfPrograms,json_encode($content));
            $counter--;
        }
        if($counter <= 0)
        {
            break;
        }
    }
    $returnArray = [$listOfPrograms, $listOfProgLink];
    echo json_encode($returnArray);
    $db->close();
}


?>
