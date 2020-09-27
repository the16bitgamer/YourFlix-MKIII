<?php

    $POST = NULL;

    if ($_SERVER['REQUEST_METHOD'] === 'POST') 
    {
        
        $_rest_json = file_get_contents("php://input");
        $POST = json_decode($_rest_json, true);
    }

    function ConnectToDatabase()
    {
        $_db = new SQLite3('/usr/share/yourflix/yourflix.db');
        return $_db;
    }

    function ErrorMessage($ERROR, $SQL)
    {
        return "ERR ". $ERROR . " - " . $SQL;
    }
?>