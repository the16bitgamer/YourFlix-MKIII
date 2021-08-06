<?php
    require 'DatabaseHandler.php';

    function GetChannelPrograms($CHANNEL_ID)
    {
        $_db = ConnectToDatabase();

        $_select = 'SELECT Program.Program_Name, Program.Program_Id, Program.First_Content, Program.First_Folder, Program.Num_Content, Program_Image.Img_Location, Program.Program_Last_Updated ';
        $_from = 'FROM Channel_Program LEFT JOIN Program ON Program.Program_Id == Channel_Program.Program_Id '.
        'LEFT JOIN Program_Image ON Program.Program_Id == Program_Image.Program_Id '.
        'LEFT JOIN Channel ON Channel_Program.Channel_Id == Channel.Channel_Id ';
        $_where = 'WHERE Channel.Channel_Name = "'. $CHANNEL_ID .'" AND Program.Num_Content > 0 ';
        
        //We are using Group By to ignore more than 1 image in the meta folders, else we'd get douplicate Programs
        $_groupBy = 'GROUP BY Program.Program_Id ';
        $_orderBy = 'ORDER BY Program.Program_Name COLLATE NOCASE ASC ';
        
        $_query = ($_select . $_from . $_where . $_groupBy . $_orderBy);

        $_result = $_db->query($_query);
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

        $_db->close();
        return $_returnMessage;
    }

    $Channel = "All";

    if($POST)
    {
        if(array_key_exists('Channel_Id', $POST))
            $Channel = $POST['Channel_Id'];
    }

    $returnArray = GetChannelPrograms($Channel);

    echo $returnArray;
?>