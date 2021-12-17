<?php    
    require_once 'GetFileOwner.php';
    require_once 'ManageFileOwner.php';
    
    function UpdateFile($FILE)
    {
        $file = fopen($FILE, "r");
        if (file === FALSE)
        {
            echo "Cannot open file ($FILE)";
            exit;
        }
        $newFile = "";
        while(!feof($file))
        {
            $newFile .= fgets($file);
        }
        fclose($file);
        $newFile .= "#TestFile\n";
        $file = fopen($FILE, "w");
        if (fwrite($file, $newFile) === FALSE)
        {
            echo "Cannot write to file ($FILE)";
            exit;
        }
        fclose($file);
    }

    $targetFile = "/etc/fstab";
    $fileInfo = GetFileOwner($targetFile);
    ChangeOwner($fileInfo);
    UpdateFile($targetFile);
    RestoreOwner($fileInfo);
?>