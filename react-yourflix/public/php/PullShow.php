<?php
    //Gather all required data for the Program
    function GetProgramData($Folder_ID, $DB)
    {
        $result = $DB->query('SELECT * FROM Content_Db WHERE Id=='.$Folder_ID);
        $parent_Id = $result->fetchArray();
        $result = $DB->query('SELECT * FROM Program_Db WHERE Folder_Id=='.$Folder_ID.' OR Folder_Id=='.$parent_Id['Parent_Id']);
        $content = $result->fetchArray();
        return $content;
    }

    function GetAllFolderData($PROG_ID, $DB)
    {
        //check to include parent as a result (Maybe pull from xml for supported file types???)
        $result = $DB->query('SELECT Content_Db.Name  FROM Content_Db LEFT JOIN FileType_Db ON FileType_Db.Id == Content_Db.File_Type WHERE Parent_Id =='.$PROG_ID.' AND FileType_Db.Name=="MP4" ORDER BY Content_Db.Name COLLATE NOCASE ASC');
        
        $returnArray = [];
        //Using this since the sqlite_count_row is broken and count always returns 1
        while($row = $result->fetchArray())
        {
            $result = $DB->query('SELECT Content_Db.Id, Content_Db.Name FROM Content_Db WHERE Id =='.$PROG_ID);
            array_push($returnArray, json_encode($result->fetchArray()));
            break;
        }

        //Pull remaining Folders
        $result = $DB->query('SELECT Content_Db.Id, Content_Db.Name FROM Content_Db LEFT JOIN FileType_Db ON FileType_Db.Id == Content_Db.File_Type WHERE Parent_Id =='.$PROG_ID.' AND FileType_Db.Name=="Folder" ORDER BY Content_Db.Name COLLATE NOCASE ASC');
        while($content = $result->fetchArray()) 
        {
            array_push($returnArray, json_encode($content));
        }

        return $returnArray;
    }

    $rest_json = file_get_contents("php://input");
    $_POST = json_decode($rest_json, true);

    $progId = $_POST['Id'];
    $db = new SQLite3('/usr/share/yourflix/yourflix.db');

    $programMeta = GetProgramData($progId, $db);
    $folderData = GetAllFolderData($programMeta['Folder_Id'], $db);

    $returnArray = [json_encode($programMeta), json_encode($folderData)];
    echo json_encode($returnArray); 
    $db->close();

?>