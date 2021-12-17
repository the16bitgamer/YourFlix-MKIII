<?php
    require 'DatabaseHandler.php';

    //Pulling All Folder Information so we can swap Program Folder at any time
    function PullFolderContent($DB_CONN, $FOLDER_ID)
    {
        $_select = 'SELECT Folder_Content.Content_Id, Folder_Content.Content_Name ';
        $_from = 'FROM Folder_Content ';
        $_where = 'WHERE Folder_Content.Folder_Id = ' . $FOLDER_ID . ' ';
        $_orderBy = 'ORDER BY Folder_Content.Content_Name COLLATE NOCASE ASC ';

        $_query = ($_select . $_from . $_where . $_orderBy);

        $_result = $DB_CONN->query($_query);
        $_returnMessage = ErrorMessage("No Results Found", $_query);

        if($_result)
        {
            $_returnArray = [];
            while($_row = $_result->fetchArray())
            {
                array_push($_returnArray, json_encode($_row));
            }
            $_returnMessage = json_encode($_returnArray);
        }
        return $_returnMessage;
    }

    $db = ConnectToDatabase();
    $folderId = 271;

    if($POST)
    {
        if(array_key_exists('Id', $POST))
            $folderId = $POST['Id'];
    }

    echo PullFolderContent($db, $folderId);
    $db->close();
?>