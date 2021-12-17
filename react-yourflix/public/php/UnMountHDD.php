<?php
    
    $driveUUID = "A06D-EC8D";
    $mountPoint = "/var/www/html/Videos_".$driveUUID;

    $results = shell_exec('sudo umount '.$mountPoint);
    $results = shell_exec('sudo rm -r '.$mountPoint);
?>