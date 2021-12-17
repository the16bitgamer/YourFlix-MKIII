<?php

    $devName = "/dev/sdb1";
    $driveUUID = "A06D-EC8D";
    $fileFormat = "exfat";
    $mountPoint = "/var/www/html/Videos_".$driveUUID;

    if(!file_exists($mountPoint))
    {
        $results = shell_exec('sudo mkdir '.$mountPoint);
    }
    $results = shell_exec('sudo mount '.$devName.' '.$mountPoint);
?>