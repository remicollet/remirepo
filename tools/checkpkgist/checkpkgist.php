#!/usr/bin/php
<?php
/**
 * CheckPkgist is a tool to check RPM update needed
 * using information from https://packagist.org/
 *
 * PHP version 5
 *
 * Copyright (C) 2014  Remi Collet
 * https://github.com/remicollet/remirepo/tree/master/tools/checkpkgist
 *
 * CheckPkgist is free software; you can redistribute it and/or
 * modify it under the terms of the GNU Lesser General Public
 * License as published by the Free Software Foundation; either
 * version 2.1 of the License, or (at your option) any later version.
 *
 * FedoraClient is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
 * Lesser General Public License for more details.
 *
 * See <http://www.gnu.org/licenses/>
 *
 * @category  CheckPkgist
 * @package   FedoraClient
 *
 * @author    Remi Collet <remi@fedoraproject.org>
 * @copyright 2014 Remi Collet
 * @license   http://www.gnu.org/licenses/lgpl-2.1.txt LGPL License 2.1 or (at your option) any later version
 * @link      https://github.com/remicollet/remirepo/tree/master/tools/checkpkgist
 */

require_once 'Cache/Lite.php';

define ('VERSION', '1.0.0-dev');

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

printf("\nCheckPkgist version %s by Remi Collet.\n\n", VERSION);

if (in_array('-h', $_SERVER['argv']) || in_array('--help', $_SERVER['argv'])) {
	echo <<<END
usage checkpkg [ options ]

    -h
    --help     Display help (this page)

    -v
    --verbose  Display all packages, with upsteam information

    -q
    --quiet    Don't display not installed packages
               or packages with latest version installed

    -s
    --sort     Sort output by package name
END;
	die("\n\n");
}

$sort   = (in_array('-s', $_SERVER['argv']) || in_array('--sort', $_SERVER['argv']));
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

if ($sort) {
	natcasesort($pkgs);
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
		$maxver = "";
		$maxdat = false;
		$display = false;
		foreach ($pkgs['package']['versions'] as $pkver => $pkg) {
			if (strpos($pkver, 'dev') !== false) {
				continue;
			}
			$date = new DateTime($pkg['time']);
			if (version_compare($pkver, $maxver, 'gt')) {
				$maxver = $pkver;
				$maxdat = $date;
			}
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
				$display = true;
				break;
			}
			else if (version_compare($pkver, $rpmver, 'eq') && $verb) {
				printf(" %-40s %15s %15s %15s\n", $rpm, $rpmver, $pkver, $date->format("Y-m-d"));
				$display = true;
				break;
			}
		}
		if ($verb && !$display) {
			printf(" %-40s %15s %15s %15s\n", $rpm, $rpmver, ($maxver ?: 'unkown'), ($maxdat ? $date->format("Y-m-d") : ''));
		}
	} else {
		printf(" %-40s %15s %15s\n", $rpm, $rpmver, 'Not found !');
	}
}