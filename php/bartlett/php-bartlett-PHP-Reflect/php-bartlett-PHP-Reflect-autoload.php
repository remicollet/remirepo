<?php
/**
 * Autoloader for bartlett/php-reflect and its dependencies
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
$fedoraClassLoader->addPrefixes(array(
    'Symfony\\Component'                  => $vendorDir,
    'Bartlett'                            => dirname(dirname(__DIR__)),
));

// Needed when installed for 'Bartlett\CompatInfo\Analyser\CompatibilityAnalyser'
if (is_dir("$vendorDir/Bartlett/CompatInfo")) {
   $fedoraClassLoader->addPrefix('Bartlett\\CompatInfo', $vendorDir);
}

// Dependencies (autoloader => required)
foreach(array(
    "$vendorDir/PhpParser/autoload.php"                         => true,
    "$vendorDir/Seld/JsonLint/autoload.php"                     => true,
    "$vendorDir/JsonSchema/autoload.php"                        => true,
    "$vendorDir/SebastianBergmann/Version/autoload.php"         => true,
    "$vendorDir/Doctrine/Common/Collections/autoload.php"       => true,
    "$vendorDir/Doctrine/Common/Cache/autoload.php"             => true,
    "$vendorDir/phpDocumentor/Reflection/DocBlock/autoload.php" => true,
    "$vendorDir/Bartlett/UmlWriter/autoload.php"                => false,
    "$vendorDir/Psr/Log/autoload.php"                           => false,
    "$vendorDir/Monolog/autoload.php"                           => false,
) as $dependencyAutoloader => $required) {
    if ($required || file_exists($dependencyAutoloader)) {
        require_once $dependencyAutoloader;
    }
}

