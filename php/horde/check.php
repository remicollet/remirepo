#!/usr/bin/php
<?php

$packs = array();
$conf = array();

function loadConf($verb) {
    if ($verb) echo "Reading configuration\n";

    $conf = array();
    $json = file_get_contents(__DIR__."/check.json");
    if ($json) {
        $conf = json_decode($json, true);
    }
    if (!is_array($conf)) {
        $conf = array();
    }
    if (!is_array($conf['blacklist'])) {
        $conf['blacklist'] = array();
    }
    if (!is_array($conf['ignore'])) {
        $conf['ignore'] = array();
    }
    if (!isset($conf['channel'])) {
        $conf['channel'] = "pear.php.net";
    }

    return $conf;
}

function loadFiles($verb) {
    global $conf, $packs;

    if ($verb) echo "Reading packages\n";

    $packs = array();
    $found = array();
    foreach(glob("php-*") as $file) {

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
                'name'      => $name,
                'version'   => $ver,
                'build'     => array_unique($breq),
                'requires'  => array_unique($req),
                'mandatory' => array(),
                'optional'  => array(),
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
                if ($dep->channel==$conf['channel']) {
                    $n = (string)$dep->name;
                    $packs[$name]['mandatory'][] = $n;
                    $found[$n] = $n;
                }
            }
        }
        if (isset($xml->dependencies->optional->package)) {
            foreach($xml->dependencies->optional->package as $dep) {
                if ($dep->channel==$conf['channel']) {
                    $n = (string)$dep->name;
                    if ($n == 'Horde_Test') {
                        if (!in_array($n, $breq)) {
                            printf("\t%s Missing BuildRequires on %s\n", ($verb ? "*" : $name), $n);
                        }
                    } else {
                       $packs[$name]['optional'][] = $n;
                    }
                    $found[$n] = $n;
                }
            }
        }
    }
    foreach ($found as $k => $v) {
        if (key_exists($k, $packs) || in_array($v, $conf['blacklist'])) {
            unset($found[$k]);
        }
    }
    $conf['missing'] = $found;
}

function showBuildOrder($verb) {
    global $conf, $packs;

    echo "Build order\n";

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
                    && !(isset($conf['ignore'][$pack['name']]) && in_array($need, $conf['ignore'][$pack['name']]))) {
                    $ok = false;
                }
            }
            // Can install ?
            if ($ok) {
                $cant[$pack['name']] = array();
                foreach ($pack['requires'] as $need) {
                    if (!array_key_exists($need, $done)
                        && !(isset($conf['ignore'][$pack['name']]) && in_array($need, $conf['ignore'][$pack['name']]))) {
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
                if (isset($conf['ignore'][$key])) {
                    $tmp = array_diff($pack['build'], $conf['ignore'][$key]);
                    $ir  = "I: ".implode(', ', $conf['ignore'][$key]);
                } else {
                    $tmp = $pack['build'];
                    $ir  = '';
                }
                $br = (count($tmp) ? "BR: ".implode(', ', $tmp) : '');
                $rr = (count($pack['requires']) ? "R: ".implode(', ', $pack['requires']) : '');
                printf("\t%-25s %-10s %s %s %s\n", $pack['name'], $pack['version'], $br, $ir, $rr);
                $i++;
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
    // Use build order
    $packs = $done;
}

function getRequires($name, $res=array()) {
    global $conf, $packs;

    if (in_array($name, $res) || !isset($packs[$name])) {
        return $res;
    }
    $res[] = $name;
    foreach($packs[$name]['requires'] as $n) {
        if (!in_array($n, $res)) {
            $res = array_unique(array_merge($res, getRequires($n, $res)));
        }
    }
    return ($res);
}

function scanOptional($verb) {
    global $conf, $packs;

    if (!$verb) return;

    if (count($conf['missing'])) {
        echo "\nMissing packages:\n\t".implode("\n\t", $conf['missing'])."\n";
    }

    echo "Optional requires\n";

    foreach ($packs as $pack) {
        $first = true;

        // add current package to avoid circular dep issue.
        $req   = array($pack['name']);

        foreach ($pack['mandatory'] as $n) {
            if (in_array($n, $pack['requires'])) {
                $req = getRequires($n, $req);
            } else {
                if ($first) {
                    $first = false;
                    echo $pack['name']."\n";
                }
                echo "\t* $n mandatory, missing\n";
            }
        }
        foreach ($pack['optional'] as $n) {
            if (in_array($n, $conf['blacklist'])) {
                continue;
            }
            // Explicit requires
            if (in_array($n, $pack['requires'])) {
                // Implicit requires
                if (in_array($n, $req)) {
                    if ($first) {
                        $first = false;
                        echo $pack['name']."\n";
                    }
                    echo "\t- $n optional and implicitly required\n";
                }
                $req = getRequires($n, $req);

            // Not explicit
            } else {
                // Not implicit
                if (!in_array($n, $req)
                    && !(in_array($n, $conf['missing']))
                    && !(isset($conf['ignore'][$pack['name']]) && in_array($n, $conf['ignore'][$pack['name']]))) {
                    if ($first) {
                        $first = false;
                        echo $pack['name']."\n";
                    }
                    echo "\t+ $n  optional, missing\n";
                }
            }
        }
    }
}

$verb = in_array('-v', $_SERVER['argv']);
$conf = loadConf($verb);
loadFiles($verb);
showBuildOrder($verb);
scanOptional($verb);
