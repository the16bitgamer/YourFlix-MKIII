<?php

    class CurrentFileData
    {
        public $fileLoc;
        public $perems;
        public $owner;
    }

    function GetFileOwner($FILE_IN)
    {
        $newFileData = new CurrentFileData();
        $newFileData->fileLoc = $FILE_IN;
        $newFileData->perems = substr(sprintf('%o', fileperms($FILE_IN)),2)."<br/>";
        $newFileData->owner = posix_getpwuid(fileowner($FILE_IN))['name'];
        return $newFileData;
    }

?>