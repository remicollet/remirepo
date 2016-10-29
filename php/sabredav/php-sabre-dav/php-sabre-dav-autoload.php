<?php
/**
 * Autoloader for sabre/dav and its dependencies
 */

$vendorDir = '/usr/share/php';

// Use Symfony autoloader
if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once $vendorDir . '/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$thisdir = dirname(dirname(__DIR__));
$fedoraClassLoader->addPrefixes(array(
  'Sabre\\DAV\\'     => $thisdir,
  'Sabre\\DAVACL\\'  => $thisdir,
  'Sabre\\CalDAV\\'  => $thisdir,
  'Sabre\\CardDAV\\' => $thisdir,
));

// dependencies
require_once $vendorDir . '/Sabre/Event/autoload.php';
require_once $vendorDir . '/Sabre/HTTP/autoload.php';
require_once $vendorDir . '/Sabre/VObject/autoload.php';
require_once $vendorDir . '/Sabre/Xml/autoload.php';
require_once $vendorDir . '/Sabre/Uri/autoload.php';
