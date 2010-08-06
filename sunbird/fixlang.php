#!/usr/bin/php
<?php

/*
./fixlang.php  --xpi=gdata-provider.xpi \
   --ref=calendar/locales/en-US/chrome/calendar/providers/gdata \
   --output=toto \
   --manifest=mani

   calendar/locales/en-US/chrome/calendar/providers/gdata

   calendar/locales/en-US/chrome/lightning/
   calendar/locales/en-US/chrome/calendar/

Manifest:
locale gdata-provider 	en-US 	jar:chrome/gdata-provider-en-US.jar!/locale/en-US/
locale calendar 	en-US 	jar:chrome/calendar-en-US.jar!/locale/en-US/calendar/
locale lightning	en-US 	jar:chrome/lightning-en-US.jar!/locale/en-US/lightning/

 */
$tmp = "./FIXJAR";
is_dir($tmp) or mkdir($tmp);

$debug=false;
for ($i = 1 ; $i < $_SERVER["argc"] ; $i++) {
   $it = explode("=", $argv[$i], 2);
   $it[0] = preg_replace('/^--/', '', $it[0]);
   if (in_array($it[0], array('debug','xpi','gdata-provider','lightning','calendar','output','manifest'))) {
      $$it[0] = $it[1];
   }
}

function LoadDtd ($file, &$tab) {
   global $debug;
//$debug=(basename($file)=='global.dtd' ? 2 : 1);
   $tab=array();

   $fic=@fopen($file, "r");
   if (!$fic) {
      die ("*** Cannot read $file\n");
   }
   $prev=false;
   if ($debug) echo "\t\tLoading $file\n";
   while ($buf=fgets($fic)) {
      $buf = rtrim($buf);
      if (empty($buf) || $buf=="\n") {
         if ($debug>1) echo "+ empty\n";
      } else if ($prev!='comment' && preg_match('/^<!ENTITY (.+)"(.*)"( *)> *(<!--.*-->|)$/', $buf, $res)) {
         if ($debug>1) echo "+ Line  '".$res[1]."'\n";
         $ind=trim($res[1]);
         $tab[$ind] = $res[1].'"'.$res[2].'">';
         $prev=false;
      } else if ($prev!='comment' && preg_match('/^<!ENTITY (.*)"(.*)$/', $buf, $res)) {
         if ($debug>1) echo "+ Start '".$res[1]."'\n";
         $ind=trim($res[1]);
         $tab[$ind] = $res[1].'"'.$res[2];
         $prev=$ind;
      } else if (preg_match('/^<!--(.*)-->$/', $buf, $res)) {
         if ($debug>1) echo "+ Comment (".$res[1].")\n";
      } else if (preg_match('/^[[:space:]]*<!--(.*)$/', $buf, $res)) {
         if (isset($tab['license'])) {
            $ind='comment';
         } else {
            $ind='license';
         }
         if ($debug>1) echo "+ Start '$ind' (".$res[1].")\n";
         $tab[$ind] = $res[1];
         $prev=$ind;
      } else if ($prev=="license" && preg_match('/^(.*)-->$/', $buf, $res)) {
         if ($debug>1) echo "+ End   'License'\n";
         $tab[$prev] .= "\n".$res[1];
         $prev=false;
      } else if ($prev=="comment" && preg_match('/^(.*)-->$/', $buf, $res)) {
         if ($debug>1) echo "+ End   'Comment'\n";
         unset($tab['comment']);
         $prev=false;
      } else if ($prev && preg_match('/^(.*)">$/', $buf, $res)) {
         if ($debug>1) echo "+ End   '".$prev."'\n";
         $tab[$prev] .= "\n".$res[1].'">';
         $prev=false;
      } else if ($prev && preg_match('/^(.*)$/', $buf, $res)) {
         if ($debug>1) echo "+ Cont. '".$prev."'\n";
         $tab[$prev] .= "\n".$res[1];
      } else {
         die("*** - unkonwn ($buf) !\n");
      }
   }
}

function SaveDtd ($locpath, $loc, $ref) {
   global $debug;

   $fic=@fopen($locpath, "w");
   if (!$fic) {
      die ("*** Cannot create $locpath\n");
   }
   if ($debug) echo "\tCreate $locpath\n";
   if (isset($ref['license'])) {
      fputs($fic, "<!-- ".$ref['license']." -->\n");
      unset($ref['license']);
   }
   // print_r($ref); print_r($loc);
   foreach($ref as $ind => $line) {
      if (isset($loc[$ind])) {
         fputs($fic, "<!ENTITY ".$loc[$ind]."\n");
      } else {
         echo "\tAdding missing $ind to $locpath\n";
         fputs($fic, "<!ENTITY ".$ref[$ind]."\n");
      }
   }
   fclose($fic);
}

function FixDtd ($locpath, $refpath) {
   global $debug;
   static $cache=array();

   if ($debug) echo "\tCheck DTD: $locpath $refpath\n";

   $key = basename($locpath);
   if (!isset($cache[$key])) {
      LoadDtd($refpath,$cache[$key]);
   }
   $ref = $cache[$key];
   $loc = array();
   LoadDtd($locpath, $loc);
   SaveDtd($locpath, $loc, $ref);
}

function LoadProp ($file, &$tab) {
   global $debug;

   $fic=@fopen($file, "r");
   if (!$fic) {
      die ("*** Cannot read $file\n");
   }
   if ($debug) echo "\t\tLoading $file\n";
   $tab=array();
   $tab['comment']=array();

   if ($fic) while ($buf=fgets($fic)) {
      $buf = rtrim($buf);
      if (empty($buf) || $buf=="\n") {
         if ($debug>1) echo "+ empty\n";
      } else if (preg_match('/^#(.*)$/', $buf, $res)) {
         if ($debug>1) echo "+ comments\n";
         $tab['comment'][]=$res[1];
      } else if (preg_match('/^([A-Za-z0-9._{}@-]*)[[:space:]]*=[[:space:]]*(.*)/', $buf, $res)) {
         if ($debug>1) echo "+ Value '".$res[1]."'\n";
         $ind=trim($res[1]);
         $tab[$ind] = $res[1].'='.$res[2];
      } else {
         echo("\tIgnored ($buf) in $file !\n");
      }
   }
}

function SaveProp ($locpath, $loc, $ref) {
   global $debug;

   $fic=@fopen($locpath, "w");
   if (!$fic) {
      die ("*** Cannot create $locpath\n");
   }
   if ($debug) echo "\tCreate $locpath\n";
   if (isset($ref['license'])) {
      fputs($fic, "<!-- ".$ref['license']." -->\n");
      unset($ref['license']);
   }
   foreach($ref['comment'] as $com) {
      fputs($fic, "#$com\n");
   }
   unset($ref['comment']);
   // print_r($ref); print_r($loc);
   foreach($ref as $ind => $line) {
      if (isset($loc[$ind])) {
         fputs($fic, $loc[$ind]."\n");
      } else {
         echo "\tAdding missing $ind to $locpath\n";
         fputs($fic, $ref[$ind]."\n");
      }
   }
   fclose($fic);
}

function FixProp ($locpath, $refpath) {
   global $debug;
   static $cache=array();

   if ($debug) echo "\tCheck Properties: $locpath $refpath\n";

   $key = basename($locpath);
   if (!isset($cache[$key])) {
      LoadProp($refpath,$cache[$key]);
   }
   $ref = $cache[$key];
   $loc = array();
   LoadProp($locpath, $loc);
   SaveProp($locpath, $loc, $ref);
}


if (!isset($xpi)
    || !isset($manifest) || !is_file($manifest)
    || !isset($output) || !is_dir($output)) {
      echo "xpi=$xpi, ref=$ref\n";
   die("usage php fixlang.php --xpi=pathto.xpi --<extname>=pathtorefdir --output=pathtooutputdir --manifest=pathto/chrome.manifest [ --debug=# ]\n");
}
$zip = new ZipArchive();
$zip2 = new ZipArchive();
$zip3 = new ZipArchive();
if (!$zip->open($xpi)) {
   die("*** Can't read $xpi\n");
}
$ficman=@fopen($manifest, "a");
if (!$ficman) {
   die("*** Can't read $manifest\n");
}
for ($i=0 ; $i <$zip->numFiles; $i++) {
   $file=$zip->statIndex($i);
   if (preg_match('/^chrome\/(.*)-([a-z]{2}-[a-zA-Z]{2}).jar$/', $file['name'], $regs)) {
      $extn = $regs[1];
      $lang = $regs[2];
   } else if (preg_match('/^chrome\/(.*)-([a-z]{2}).jar$/', $file['name'], $regs)) {
      $extn = $regs[1];
      $lang = $regs[2];
   } else {
      continue;
   }
   if (isset($$extn) && is_dir($$extn)) {
      $ref=$$extn;
   } else {
      die("*** Missing --$extn options\n");
   }
   if ($lang == 'en-US') {
      continue;
   }
   //if ($lang != 'et') continue; /// for debug
   if ($debug) echo "Working on $tmp/chrome/$extn-$lang.jar to $output/chrome/$extn-$lang.jar \n";
   $zip->extractTo($tmp, "chrome/$extn-$lang.jar");

   if ($zip2->open($zipin="$tmp/chrome/$extn-$lang.jar")!==true) {
      die("*** Can't read $zipin\n");
   }
   if ($zip3->open($zipout="$output/chrome/$extn-$lang.jar", ZIPARCHIVE::CREATE)!==true) {
      die("*** Can't write $zipout=\n");
   }

   for ($j=0 ; $j <$zip2->numFiles; $j++) {
      $file=$zip2->statIndex($j);

      $zip2->extractTo($tmp, $file['name']);
      if (preg_match('/.dtd$/', $file['name'])) {
         $sub = basename(dirname($file['name']));
         if (is_file("$ref/".basename($file['name']))) {
            FixDtd("$tmp/".$file['name'], "$ref/".basename($file['name']));
         } else if (is_file("$ref/$sub/".basename($file['name']))) {
            FixDtd("$tmp/".$file['name'], "$ref/$sub/".basename($file['name']));
         } else {
            echo "\tSkip check of $tmp/".$file['name']." ($sub)\n";
         }

      } else if (preg_match('/.properties$/', $file['name'])) {
         $sub = basename(dirname($file['name']));
         if (is_file("$ref/".basename($file['name']))) {
            FixProp("$tmp/".$file['name'], "$ref/".basename($file['name']));
         } else if (is_file("$ref/$sub/".basename($file['name']))) {
            FixProp("$tmp/".$file['name'], "$ref/$sub/".basename($file['name']));
         } else if (basename($file['name'])=='wcap.properties') {
            FixProp("$tmp/".$file['name'], "$ref/providers/wcap/".basename($file['name']));
         } else if (basename($file['name'])=='timezones.properties') {
            FixProp("$tmp/".$file['name'], "$ref/../calendar/".basename($file['name']));
         } else {
            echo "\tSkip check of $tmp/".$file['name']." ($sub)\n";
         }
      } else {
         if ($debug) echo "Copy  $tmp/".$file['name']."\n";
      }

      if ($zip3->addFile("$tmp/".$file['name'], $file['name'])) {
         if ($debug) echo "\tAdd "."$tmp/".$file['name']." in $zipout\n";
      } else {
         die ("*** Can't add ".$file['name']." in $zipout\n");
      }
      $base = dirname($file['name']);
   }
   fputs($ficman, "locale\t$extn\t$lang\tjar:chrome/$extn-$lang.jar!/$base/\n");
   $zip2->close();
   $zip3->close();
}
fclose($ficman);
?>
