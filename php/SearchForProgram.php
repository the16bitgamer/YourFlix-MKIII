<?php
    require 'DatabaseHandler.php';

    function SearchDatabase($DB_CONN, $QUERY)
    {

        $_select = 'SELECT Program.Program_Name, Program.First_Content, Program.First_Folder, Program.Num_Content, Program_Image.Img_Location ';
        $_from = 'FROM Program LEFT JOIN Program_Image ON Program.Program_Id == Program_Image.Program_Id ';
        $_where = 'WHERE Program.Num_Content > 0 ';
        $_orderBy = 'ORDER BY Program.Program_Name COLLATE NOCASE ASC ';
        $_query = $_select . $_from . $_where . $_orderBy;

        $_result = $DB_CONN->query($_query);
        $_returnMessage = ErrorMessage("No Results Found", ($_query));

        if($_result)
        {
            $_returnArray = [];
            while($content = $_result->fetchArray()) 
            {
                $_search = stripos($content['Program_Name'], $QUERY);
                if($_search !== false)
                {
                    array_push($_returnArray,json_encode($content));
                }
            }
            $_returnMessage = json_encode($_returnArray);
        }

        return $_returnMessage;
    }
    
    $db = ConnectToDatabase();
    $query = '';

    if($POST)
    {
        if(array_key_exists('query', $POST))
        $query = $POST['query'];
    }
    $searchResults = SearchDatabase($db, $query);

    echo $searchResults;
    $db->close();
?>