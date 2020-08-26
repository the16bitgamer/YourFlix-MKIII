<?php
    function GetVideoLink($DB_CONN, $FOLDER_ID)
    {
        $result = $DB_CONN->query('SELECT Content_Db.Id  FROM Content_Db LEFT JOIN FileType_Db ON FileType_Db.Id == Content_Db.File_Type WHERE Parent_Id =='.$FOLDER_ID.' AND FileType_Db.Name=="MP4" ORDER BY Content_Db.Name');
        
        $returnLink = FALSE;
        $numVideos = 0;
        //Using this since the sqlite_count_row is broken and count always returns 1
        while($row = $result->fetchArray())
        {
            if($numVideos == 0)
            {
                $numVideos++;
                $returnLink = "/Video?id=".$row['Id'];
            }
            else
            {
                $returnLink = "/Show?id=".$FOLDER_ID;
            }
            break;
        }
        return $returnLink;
    }

    function GetFolderLink($DB_CONN, $FOLDER_ID)
    {
        $result = $DB_CONN->query('SELECT Id FROM Content_Db WHERE Parent_Id == '.$FOLDER_ID.' ORDER BY Name');
        $content = $result->fetchArray();
        return "/Show?id=".$content['Id'];
    }

    function GetProgramLink($DB_CONN, $PROG_ID, $FOLDER_ID)
    {
        //$progData = "&prog=".$PROG_ID;
        $returnLink = GetVideoLink($DB_CONN, $FOLDER_ID);
        if($returnLink === FALSE)
        {
            $returnLink = GetFolderLink($DB_CONN, $FOLDER_ID);
        }

        return $returnLink;
    }
?>