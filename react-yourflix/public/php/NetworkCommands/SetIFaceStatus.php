<?php
    
    $targetIFace = "wlan0";
    $action = "on";

    switch($action)
    {
        case "on":
            $results = shell_exec('sudo ifconfig '.$targetIFace.' up');
            break;
        case "off":
            $results = shell_exec('sudo ifconfig '.$targetIFace.' down');
            break;
    }

?>