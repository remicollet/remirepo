#!/usr/bin/php
<?php
require_once 'Cache/Lite.php';

class PkgClient {
	const URL = 'https://packagist.org/';
	protected $cache;

	function __construct () {
		$dir = "/tmp/pkgist-".posix_getlogin()."/";
		@mkdir($dir);
		$this->cache = new Cache_Lite(
			array(
				'memoryCaching'             => true,
				'cacheDir'                  => $dir,
				'automaticSerialization'    => true
			)
		);
	}

	function getPackage($name) {
		$url = self::URL.'packages/'.$name.'.json';
		$rep = $this->cache->get(__METHOD__, $url);
		if (!$rep) {
			$rep = @file_get_contents($url);
			$this->cache->save($rep, __METHOD__, $url);
		}
		return ($rep ? json_decode($rep, true) : false);
	}
}

if (in_array('-h', $_SERVER['argv']) || in_array('--help', $_SERVER['argv'])) {
	echo <<<END

usage checkpkg [ options ]

    -h
    --help    Display help (this page)

    -v
    --verbose  Display all packages, with upsteam information

    -q
    --quiet    Don't display not installed packages
               or packages with latest version installed
END;
	die("\n\n");
}

$verb   = (in_array('-v', $_SERVER['argv']) || in_array('--verbose', $_SERVER['argv']));
$quiet  = (in_array('-q', $_SERVER['argv']) || in_array('--quiet', $_SERVER['argv']));
$client = new PkgClient();

$pkgs = file_get_contents(__DIR__."/checkpkgist.json");
if (!$pkgs) {
	die("Missing configuration file\n");
}
$pkgs = json_decode($pkgs, true, 5, JSON_PARSER_NOTSTRICT);
if (!$pkgs) {
	die("Bad configuration file\n");
}

printf(" %-40s %15s %15s %15s\n", "Name", "Version", "Upstream", "Date");

foreach ($pkgs as $name => $rpm) {
	$rpmver = exec("rpm -q --qf '%{VERSION}' $rpm", $out, $ret);
	if ($ret) {
		if ($quiet) {
			continue;
		}
		$rpmver = "n/a";
	}
	$pkgs = $client->getPackage($name);
	if ($pkgs) {
		foreach ($pkgs['package']['versions'] as $pkver => $pkg) {
			if (strpos($pkver, 'dev') !== false) {
				continue;
			}
			$date = new DateTime($pkg['time']);
			if (version_compare($pkver, $rpmver, 'gt')) {
				$diff = $date->diff(new DateTime("now"));
				if ($diff->days <2) {
					$note = "(Just released)";
				} else if ($diff->days <20) {
					$note = $diff->format("(%a days)");
				} else {
					$note = "";
				}

				//print_r($pkg);
				printf(" %-40s %15s %15s %15s %s\n", $rpm, $rpmver, $pkver, $date->format("Y-m-d"), $note);
				if ($pkg['source']['type']=='git' && $verb) {
					printf("\tURL:  %s\n\tHash: %s\n",
						($pkg['source']['url']?:'unkown'),
						($pkg['source']['reference']?:'unkown'));
				}
				break;
			}
			else if (version_compare($pkver, $rpmver, 'eq') && $verb) {
				printf(" %-40s %15s %15s %15s\n", $rpm, $rpmver, $pkver, $date->format("Y-m-d"));
				break;
			}
		}
	} else {
		printf(" %-40s %15s %15s\n", $rpm, $rpmver, 'Not found !');
	}
}