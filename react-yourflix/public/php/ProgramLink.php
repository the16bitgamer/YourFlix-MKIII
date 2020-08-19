<?php
    function GetProgramLink($DB_CONN, $FOLDER_ID)
    {
        $result = $DB_CONN->query('SELECT Id, File_Type FROM Content_Db WHERE Parent_Id == '.$FOLDER_ID.' ORDER BY Name');
        $returnId = -1;
        $otherFiles = 0;
        $returnLink = "/Video?id=";
        while($content = $result->fetchArray()) 
        {
            //Checks for folder and sets the return id to itself as a show
            if($content['File_Type'] == 'Folder' && $returnId == -1)
            {
                $returnLink = "/Show?id=";
                $returnId = (int)$content['Id'];
            }
            //Checks for a Non-Folder and returns the parent folder as a show, it also breaks
            else if($otherFiles >= 1 || $returnId != -1)
            {
                $returnLink = "/Show?id=";
                $otherFiles++;
                $returnId = (int)$FOLDER_ID;
                break; 
            }
            //Checks for a Non-Folder and returns itself, assuming it's a Video
            else
            {
                $otherFiles++;
                $returnId = (int)$content['Id'];
            }
        }

        return $returnLink . $returnId;
    }
?>