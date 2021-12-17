<?php
    $targetIFace = "eth0";
    $action = "add";

    switch($action)
    {
        case "add":
            $results = shell_exec('sudo iptables -t nat -A POSTROUTING -o '.$targetIFace.' -j MASQUERADE');
            break;
        case "remove":
            $results = shell_exec('sudo iptables -t nat -D POSTROUTING -o '.$targetIFace.' -j MASQUERADE');
            break;
    }
    $results = shell_exec('sudo netfilter-persistent save');
?>