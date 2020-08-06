<?php

$db = new SQLite3('/usr/share/yourflix/yourflix.db');
$result = $db->query('SELECT * FROM Program_Db');

$listOfPrograms = [];
while($content = $result->fetchArray()) 
{
    array_push($listOfPrograms,json_encode($content));
}
echo json_encode($listOfPrograms);
$db->close();

?>
