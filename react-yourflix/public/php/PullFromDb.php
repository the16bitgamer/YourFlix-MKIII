<?php

$db = new SQLite3('/usr/share/yourflix/yourflix.db');
$result = $db->query('SELECT * FROM Program_Db ORDER BY Name COLLATE NOCASE ASC');

$returnArray = [];

while($content = $result->fetchArray()) 
{
    $progId = $content['Id'];
    $folderId = $content['Folder_Id'];
    array_push($returnArray,json_encode($content));
}
echo json_encode($returnArray);
$db->close();

?>
