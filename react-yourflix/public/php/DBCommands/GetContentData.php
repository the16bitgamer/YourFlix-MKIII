<?php
    require 'DatabaseHandler.php';

    function PullContentData($DB_CONN, $CONTENT_ID)
    {
        $_select = 'SELECT Folder_Content.Content_Id, Folder_Content.Content_Name, Folder_Content.Content_Location, Folder_Content.Folder_Id, Program.Num_Content ';
        $_from = 'FROM Folder_Content LEFT JOIN Content_Folder ON Folder_Content.Folder_Id == Content_Folder.Folder_Id LEFT JOIN Program ON Program.Program_Id == Content_Folder.Program_Id ';
        $_where = 'WHERE Folder_Content.Content_Id = '. $CONTENT_ID .' ';

        $_query = ($_select . $_from . $_where);

        $_result = $DB_CONN->query($_query);
        $_returnMessage = ErrorMessage("No Results Found", $_query);

        if($_result)
        {
            $_currContent = $_result->fetchArray();

            if(array_key_exists('Folder_Id', $_currContent))
            {
                $_folderId = $_currContent['Folder_Id'];

                $_select = 'SELECT Folder_Content.Content_Id ';
                $_from = 'FROM Folder_Content ';
                $_where = 'WHERE Folder_Content.Folder_Id = '. $_folderId .' ';
                $_orderBy = 'ORDER BY Folder_Content.Content_Name COLLATE NOCASE ASC ';
        
                $_query = ($_select . $_from . $_where . $_orderBy);
        
                $_result = $DB_CONN->query($_query);
                $_returnMessage = ErrorMessage("No Results Found", $_query);

                $_listOfSiblings = [];

                while($_content = $_result->fetchArray()) 
                {
                    array_push($_listOfSiblings, json_encode($_content));
                }

                $_returnArray = [$_currContent, $_listOfSiblings];
                return json_encode($_returnArray);
            }
        }
        
        return $_returnMessage;    
    }

    
    $db = new SQLite3('/usr/share/yourflix/yourflix.db');
    $contentID = 1028;

    if($POST)
    {
        if(array_key_exists('Id', $POST))
            $contentID = $POST['Id'];
    }

    echo PullContentData($db, $contentID);
    $db->close();
?>