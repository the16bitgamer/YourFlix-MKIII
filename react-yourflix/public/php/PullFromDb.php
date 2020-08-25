<?php

include 'ProgramLink.php';
$db = new SQLite3('/usr/share/yourflix/yourflix.db');
$result = $db->query('SELECT * FROM Program_Db ORDER BY Name');

$listOfPrograms = [];
$listOfProgLink = [];

while($content = $result->fetchArray()) 
{
    $progId = $content['Id'];
    $folderId = $content['Folder_Id'];
    $progLink = GetProgramLink($db,$progId,$folderId);
    array_push($listOfProgLink,json_encode($progLink));
    array_push($listOfPrograms,json_encode($content));
}
$returnArray = [$listOfPrograms, $listOfProgLink];
echo json_encode($returnArray);
$db->close();

?>
