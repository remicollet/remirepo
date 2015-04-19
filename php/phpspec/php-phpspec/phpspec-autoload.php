<?php
/* not namespaced, use classs-map */
require_once 'phpspec/php-diff/autoload.php';
/* prophecy and its dependencies */
require_once 'Prophecy/autoload.php';

$vendorDir = '/usr/share/php';
require_once $vendorDir . '/Symfony/Component/ClassLoader/UniversalClassLoader.php';
use Symfony\Component\ClassLoader\UniversalClassLoader;

$loader = new UniversalClassLoader();
$ns = array(
    'Doctrine\\Instantiator'              => $vendorDir,
    'SebastianBergmann'                   => $vendorDir,
    'Symfony\\Component'                  => $vendorDir,
    'PhpSpec'                             => dirname(__DIR__),
);
/* spec tree in current dir, when exists */
if (is_dir(getcwd().'/spec')) {
    $ns['spec'] = getcwd();
}
$loader->registerNamespaces($ns);
$loader->register();
