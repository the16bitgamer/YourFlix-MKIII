<?php
	class AvaliableDrives
	{
		public $Name;
       	public $UUID;
       	public $FSTYPE;
       	public $SIZE;
       	public $FSUSED;
       	public $FSAVAIL;
       	public $FSUSEPER;
       	public $MOUNTPOINT;
       	public $LABEL;
    }

	$rawDrives = shell_exec('lsblk -r -o NAME,UUID,FSTYPE,SIZE,FSUSED,FSAVAIL,FSUSE%,MOUNTPOINT,LABEL,PARTLABEL');
	$allDrives = str_replace("\\x", "%", strval($rawDrives));
	$driveList = preg_split('/\r\n|\n|\r/', $allDrives);
	$driveArray = array();
	foreach ($driveList as &$drive)
	{
		$newDrive = explode(" ", $drive);
    	if($newDrive[1] != "UUID" && $newDrive[1] != "" && $newDrive[9] != "Microsoft%20reserved%20partition" && $newDrive[7] != "/boot")
		{
			$tempDrive = new AvaliableDrives();
			$tempDrive->Name = $newDrive[0];
			$tempDrive->UUID = $newDrive[1];
			$tempDrive->FSTYPE = $newDrive[2];
			$tempDrive->SIZE = $newDrive[3];
			$tempDrive->FSUSED = $newDrive[4];
			$tempDrive->FSAVAIL = $newDrive[5];
			$tempDrive->FSUSEPER = $newDrive[6];
			if($newDrive[7] == '/')
				$tempDrive->MOUNTPOINT = "/var/www/html/Videos";
			else
				$tempDrive->MOUNTPOINT = $newDrive[7];
			$tempDrive->LABEL = $newDrive[8];

			array_push($driveArray, $tempDrive);
		}
	}
	unset($drive);

	echo json_encode($driveArray);
?>