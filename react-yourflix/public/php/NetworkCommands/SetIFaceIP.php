<?php
    $targetIFace = "eth1";
    $newIP = "192.168.0.69";
    $currentNetmask = "255.255.255.0";
    $currentGW = "192.168.0.1";
    $newGW = "192.168.0.1";

    $results = shell_exec('sudo route del default gw '.$currentGW.' '.$targetIFace);
    $results = shell_exec('sudo ifconfig '.$targetIFace.' '.$newIP.' netmask '.$currentNetmask.' up');
    $results = shell_exec('sudo route add default gw '.$newGW.' '.$targetIFace);
?>