<?php

    class Network
	{
        public $IName;
        public $Active;
        public $Compatible;
        public $IPAddress;
        public $Netmask;
        public $GateWay;
        public $MacAddress;
        public $PostRoute;

    }

    function GetDefaultGateway($INTERFACE)
    {
        $defaultGateWays = shell_exec('ip route show default');
        $listConnectedGateways = explode(PHP_EOL, $defaultGateWays);
        
        $gateway = NULL;
        foreach ($listConnectedGateways as &$currentGateWay)
        {
            $newGateWay = explode(" ", $currentGateWay);
            
            if(in_array($INTERFACE,$newGateWay))
            {
                $gateway = $newGateWay[2];
            }
            
        }
        unset($currentGateWay);
        return $gateway;
    }

    function GetNetworkInfo($INTERFACE, $ISPOSTROUTED)
    {
        $searchedNetworks = shell_exec('ifconfig '.$INTERFACE);
        $network = str_replace(PHP_EOL, '', strval($searchedNetworks));
        $networkInfo = explode(" ", $network);

        $isNetworkUp = shell_exec('ip a show '.$INTERFACE.' up');

        if(strpos($INTERFACE, 'wlan') !== false)
            $isCompatible = shell_exec('iwconfig '.$INTERFACE);

        $newNetwork = new Network();
        $newNetwork->IName = $INTERFACE;
        $newNetwork->Active = $isNetworkUp !== NULL;
        $newNetwork->PostRoute = $ISPOSTROUTED;
        $newNetwork->IPAddress = NULL;
        $newNetwork->Netmask = NULL;
        $newNetwork->GateWay = GetDefaultGateway($INTERFACE);
        $newNetwork->MacAddress = NULL;

        if(strpos($INTERFACE, 'wlan') !== false)
            $newNetwork->Compatible = !(strpos($isCompatible, 'unassociated') !== false);
        else
            $newNetwork->Compatible = true;

        for ($i = 0; $i <= count($networkInfo) -1; $i++)
        {
            switch ($networkInfo[$i])
		    {
                case "inet":
                    $newNetwork->IPAddress = $networkInfo[$i+1];
                    break;
		        case "netmask":
                    $newNetwork->Netmask = $networkInfo[$i+1];
                    break;
                case "ether":
                    $newNetwork->MacAddress = $networkInfo[$i+1];
                    break;
            }
        }

        return $newNetwork;
    }

    $connectedNetworks = shell_exec('ifconfig -a -s');
	$allActiveNetworks = explode(PHP_EOL, $connectedNetworks);

    $postRouting = shell_exec('sudo iptables -t nat -v -L POSTROUTING -n --line-number');

    $activeNetworkArr = array();
	foreach ($allActiveNetworks as &$activeNetwork)
	{
		$newDrive = explode(" ", $activeNetwork);
        $iface = $newDrive[0];
        if($activeNetwork != "" && $iface != "Iface" && $iface != "lo")
        {
            $isPostRouted = strpos($postRouting , $iface) !== false;
            array_push($activeNetworkArr, GetNetworkInfo($iface, $isPostRouted));
        }
    }
	unset($activeNetwork);

    echo json_encode($activeNetworkArr);

?>