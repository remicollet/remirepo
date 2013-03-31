#!/usr/bin/php
<?php

$packs = array();

function loadFiles($verb) {
    global $packs;

    // Non free packages
    $blacklist = array('Horde_ActiveSync');

    if ($verb) echo "Reading packages\n";

    $packs = array();
    $found = array();
    foreach(glob("php-horde-*") as $file) {

        $spec = @fopen("$file/$file.spec", "r") 
            or die("*** Can't read $file/$file.spec\n");

        $breq = $req = array();
        $name = $ver = false;

        while ($buf=fgets($spec)) {
            if (preg_match('/^Version:[[:space:]]*([0-9.]*)/', $buf, $reg)) {
                $ver = $reg[1];
            } else if (preg_match('/^%global[[:space:]]*pear_name[[:space:]]*([_a-zA-Z]*)/', $buf, $reg)) {
                $name = $reg[1];
            } else if (preg_match('/^Provides:[[:space:]]*php-pear\(%{pear_channel}\/(.*)\)/', $buf, $reg)) {
                if (!$name) $name = $reg[1];
            } else if (preg_match('/^BuildRequires:[[:space:]]*php-pear\(%{pear_channel}\/(.*)\)/', $buf, $reg)) {
                $breq[] = $reg[1];
            } else if (preg_match('/^Requires:[[:space:]]*php-pear\(%{pear_channel}\/(.*)\)/', $buf, $reg)) {
                $req[] = $reg[1];
            }
        }
        if ($ver && $name) {
            $packs[$name] = array(
                'name'     => $name,
                'version'  => $ver,
                'build'    => array_unique($breq),
                'requires' => array_unique($req),
            );
            if ($verb) {
                echo "+ $name version $ver\n";
            }
        } else {
            die("*** Name / Version not found for $file\n");
        }
        fclose($spec);

        if (file_exists("$file/$name-$ver.tgz") 
            && !file_exists("$file/package.xml")
            && !file_exists("$file/package-$ver.xml")) {
            if ($verb) echo "\tExtract package.xml from $name-$ver.tgz\n";
            exec("tar xf $file/$name-$ver.tgz -C $file package.xml");
            rename("$file/package.xml", "$file/package-$ver.xml");
        }
        $xml = @simplexml_load_file("$file/package-$ver.xml")
            or $xml = @simplexml_load_file("$file/package.xml")
            or die("*** Can't load $file/package-$ver.xml or $file/package.xml\n");
        if ($xml->name != $name || $xml->version->release != $ver) {
            die("*** Bad pakage.xml\n");
        }

        if (isset($xml->dependencies->required->package)) {
            foreach($xml->dependencies->required->package as $dep) {
                if ($dep->channel=='pear.horde.org') {
                    $n = (string)$dep->name;
                    if (!in_array($n, $req)) {
                        printf("\t%s Missing Requires on %s\n", ($verb ? "*" : $name), $n);
                    }
                    $found[$n] = $n;
                }
            }
        }
        if (isset($xml->dependencies->optional->package)) {
            foreach($xml->dependencies->optional->package as $dep) {
                if ($dep->channel=='pear.horde.org') {
                    $n = (string)$dep->name;
                    if ($n == 'Horde_Test') {
                        if (!in_array($n, $breq)) {
                            printf("\t%s Missing BuildRequires on %s\n", ($verb ? "*" : $name), $n);
                        }
                    } else if ($verb 
                               && !in_array($n, $blacklist)
                               && !in_array($n, $req)) {
                       echo "\t  Missing optional Requires on $n\n";
                    }
                    $found[$n] = $n;
                }
            }
        }
    }
    foreach ($found as $k => $v) {
        if (key_exists($k, $packs) || in_array($v, $blacklist)) {
            unset($found[$k]);
        }
    }
    if (count($found)) {
        echo "Missing packages: ".implode(', ', $found)."\n";
    }
}

function showBuildOrder($verb) {
    global $packs;

    // Ignore depency, to allow build order
    $ignore = array(
        // Allow to build Horde_Test
        'Horde_Cli'             => array('Horde_Test'),
        'Horde_Constraint'      => array('Horde_Test'),
        'Horde_Exception'       => array('Horde_Test'),
        'Horde_Support'         => array('Horde_Test'),
        'Horde_Translation'     => array('Horde_Test'),
        'Horde_Util'            => array('Horde_Test'),
        'Horde_Log'             => array('Horde_Test'),
        // Circular dependency
        'Horde_Mail'            => array('Horde_Mime'),
        // TO clean
        'Horde_Date'            => array('Horde_Icalendar'),
        'Horde_Cache'           => array('Horde_Db'),
        'Horde_Notification'    => array('Horde_Alarm'),
        'Horde_Form'            => array('Horde_Core'),
    );
    if ($verb) echo "Build order\n";

    $todo = $packs;
    $done = array();
    $i = 1;
    while (count($todo)) {
        $j = $i;
        $cant = array();
        foreach ($todo as $key => $pack) {
            $ok = true;
            // Can build ?
            foreach($pack['build'] as $need) {
                if (!array_key_exists($need, $done)
                    && !(isset($ignore[$pack['name']]) && in_array($need, $ignore[$pack['name']]))) {
                    $ok = false;
                }
            }
            // Can install ?
            if ($ok) {
                $cant[$pack['name']] = array();
                foreach ($pack['requires'] as $need) {
                    if (!array_key_exists($need, $done)
                        && !(isset($ignore[$pack['name']]) && in_array($need, $ignore[$pack['name']]))) {
                        $cant[$pack['name']][] = $need;
                        $ok = false;
                    }   
                }   
                if (count($cant[$pack['name']])>1) {
                    unset($cant[$pack['name']]);
                }          
            }
            if ($ok) {
                $done[$key] = $pack;
                unset($todo[$key]);
                if (isset($ignore[$key])) {
                    $tmp = array_diff($pack['build'], $ignore[$key]);
                    $ir  = "I: ".implode(', ', $ignore[$key]);
                } else {
                    $tmp = $pack['build'];
                    $ir  = '';
                }
                $br = (count($tmp) ? "BR: ".implode(', ', $tmp) : '');
                $rr = (count($pack['requires']) ? "R: ".implode(', ', $pack['requires']) : '');
                printf("%4d %-25s %-10s %s %s %s\n", $i++, $pack['name'], $pack['version'], $br, $ir, $rr);
            }
        }
        if ($j == $i) {
            if (count($cant)) {
                echo "Packages which CAN be build but CANNOT be installed because of a single dependency\n";
                print_r($cant);
                //echo "All packages not yet build\n";
                //print_r($todo);
            }
            die("*** Broken build order\n");
        }
    }
}

$verb = in_array('-v', $_SERVER['argv']);
loadFiles($verb);
showBuildOrder($verb);

