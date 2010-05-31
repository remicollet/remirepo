#!/usr/bin/php
<?php
function loaddtd ($file, &$tab) {

	echo "+ Loading $file\n";
	$tab=array();

	$fic=fopen($file, "r");
	$prev=false;
	if ($fic) while ($buf=fgets($fic)) {
		if (empty($buf) || $buf=="\n") {
			//echo "+ empty\n";
		} else if (preg_match('/^<!ENTITY (.*)"(.*)">$/', $buf, $res)) {
			//echo "+ Line  '".$res[1]."'\n";
			$ind=trim($res[1]);
			$tab[$ind] = $res[1].'"'.$res[2].'">';
			$prev=false;
		} else if (preg_match('/^<!ENTITY (.*)"(.*)$/', $buf, $res)) {
			//echo "+ Start '".$res[1]."'\n";
			$ind=trim($res[1]);
			$tab[$ind] = $res[1].'"'.$res[2];
			$prev=$ind;
		} else if ($prev && preg_match('/^(.*)">$/', $buf, $res)) {
			//echo "+ End   '".$prev."'\n";
			$tab[$prev] .= "\n".$res[1].'">';
			$prev=false;
		} else if ($prev && preg_match('/^(.*)$/', $buf, $res)) {
			//echo "+ Cont. '".$prev."'\n";
			$tab[$prev] .= "\n".$res[1];
		} else {
			die("- unkonwn ($buf) !\n");
		}
	}
}
function loadprop ($file, &$tab) {

	echo "+ Loading $file\n";
	$tab=array();

	$fic=fopen($file, "r");
	if ($fic) while ($buf=fgets($fic)) {
		if (empty($buf) || $buf=="\n") {
			//echo "+ empty\n";
		} else if (preg_match('/^#/', $buf, $res)) {
			//echo "+ comments\n";
		} else if (preg_match('/^([A-Za-z0-9._]*)[[:space:]]*=[[:space:]]*(.*)/', $buf, $res)) {
			//echo "+ Value '".$res[1]."'\n";
			$ind=trim($res[1]);
			$tab[$ind] = $res[1].'='.$res[2];
		} else {
			echo("\tIgnored ($buf) !\n");
		}
	}
}
if ($_SERVER["argc"]<3) die ("usage enigmail-fixlang.php fromdir destdir\n");
$from=$_SERVER["argv"][1];
$dest=$_SERVER["argv"][2];
if (!is_file("$from/enigmail.dtd")) 		die ("$from/enigmail.dtd not found\n");
if (!is_file("$from/enigmail.properties")) 	die ("$from/enigmail.properties not found\n");
if (!is_file("$dest/enigmail.dtd")) 		die ("$dest/enigmail.dtd not found\n");
if (!is_file("$dest/enigmail.properties")) 	die ("$dest/enigmail.properties not found\n");

loaddtd("$from/enigmail.dtd", $endtd);
loaddtd("$dest/enigmail.dtd", $frdtd);

echo "+ Writing $dest/enigmail.dtd\n";
$fic=fopen("$dest/enigmail.dtd", "w");
foreach($endtd as $ind => $line) 
	if (isset($frdtd[$ind])) {
		fputs($fic, "<!ENTITY ".$frdtd[$ind]."\n");
	} else {
		echo "\tAdding missing $ind\n";
		fputs($fic, "<!ENTITY ".$endtd[$ind]."\n");
	}
fclose($fic);

loadprop("$from/enigmail.properties", $enprop);
loadprop("$dest/enigmail.properties", $frprop);

echo "+ Writing $dest/enigmail.properties\n";
$fic=fopen("$dest/enigmail.properties", "w");
foreach($enprop as $ind => $line) 
	if (isset($frprop[$ind])) {
		fputs($fic, $frprop[$ind]."\n");
	} else {
		echo "\tAdding missing $ind\n";
		fputs($fic, $enprop[$ind]."\n");
	}
fclose($fic);
?>

