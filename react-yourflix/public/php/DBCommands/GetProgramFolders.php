<?php
    require 'DatabaseHandler.php';

    //Pulling the Program Information for the Top of the Show Page
    function PullProgramInformation($DB_CONN, $FOLDER_ID)
    {
        $_select = 'SELECT Program.Program_Name, Program.Program_Id, Program_Image.Img_Location ';
        $_from = 'FROM Content_Folder LEFT JOIN Program ON Content_Folder.Program_Id = Program.Program_Id LEFT JOIN Program_Image ON Program.Program_Id == Program_Image.Program_Id ';
        $_where = 'WHERE Folder_Id = ' . $FOLDER_ID . ' ';
        
        //We are using Group By to ignore more than 1 image in the meta folders, else we'd get douplicate Programs
        $_groupBy = 'GROUP BY Program.Program_Id ';
        $_orderBy = 'ORDER BY Program.Program_Name COLLATE NOCASE ASC ';

        $_query = ($_select . $_from . $_where . $_groupBy . $_orderBy);

        $_result = $DB_CONN->query($_query);
        $_returnMessage = ErrorMessage("No Results Found", $_query);

        if($_result)
        {
            while($_row = $_result->fetchArray())
            {
                $_returnMessage = $_row;
                break;
            }
        }
        return $_returnMessage;
    }

    //Pulling All Folder in a Program
    function PullProgramFolderContent($DB_CONN, $PROGRAM_ID)
    {
        $_select = 'SELECT Content_Folder.Folder_Id, Content_Folder.Folder_Name ';
        $_from = 'FROM Content_Folder ';
        $_where = 'WHERE Content_Folder.Program_Id = ' . $PROGRAM_ID . ' ';
        $_orderBy = 'ORDER BY Content_Folder.Folder_Name COLLATE NOCASE ASC ';

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
    $folderId = 0;

    if($POST)
    {
        if(array_key_exists('Id', $POST))
            $folderId = $POST['Id'];
    }

    $programResults = PullProgramInformation($db, $folderId);
    if(!is_string($programResults))
    {
        if(array_key_exists('Program_Id', $programResults))
        {
            $showResults = PullProgramFolderContent($db, $programResults['Program_Id']);
            $returnArray = [json_encode($programResults), $showResults];
            echo json_encode($returnArray); 
        }
    }
    else
        echo json_encode($programResults);
    
    $db->close();
?>