<?php
/* Autoloader for composer/composer and its dependencies */

$vendorDir = '/usr/share/php';
if (!class_exists('Fedora\\Autoloader\\Autoload', false)) {
    require_once '/usr/share/php/Fedora/Autoloader/autoload.php';
}

\Fedora\Autoloader\Autoload::addPsr4('Composer\\', __DIR__);

// Dependencies
\Fedora\Autoloader\Dependencies::required(array(
	$vendorDir . '/Symfony/Component/autoload.php',
	$vendorDir . '/Seld/JsonLint/autoload.php',
	$vendorDir . '/Seld/PharUtils/autoload.php',
	$vendorDir . '/Seld/CliPrompt/autoload.php',
	$vendorDir . '/Composer/CaBundle/autoload.php',
	$vendorDir . '/Composer/Spdx/autoload.php',
	$vendorDir . '/Composer/Semver/autoload.php',
	$vendorDir . '/JsonSchema2/autoload.php',
	$vendorDir . '/Psr/Log/autoload.php',
));

