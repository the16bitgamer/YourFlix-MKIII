<?php
    require_once 'GetFileOwner.php';

    function ChangeOwner($FILE_IN)
    {
        $currentUser = exec('whoami');
        $results = shell_exec('sudo chown '.$currentUser.' '.$FILE_IN->fileLoc);
    }

    function RestoreOwner($FILE_IN)
    {
        $results = shell_exec('sudo chown '.$FILE_IN->owner.' '.$FILE_IN->fileLoc);
    }

?>