<?php
/**
 * Autoloader for bartlett/php-reflect and its dependencies
 */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Bartlett\\', dirname(__DIR__));
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php/Symfony/Component/autoload.php',
    '/usr/share/php/PhpParser/autoload.php',
    '/usr/share/php/Seld/JsonLint/autoload.php',
    '/usr/share/php/JsonSchema/autoload.php',
    '/usr/share/php/SebastianBergmann/Version/autoload.php',
    '/usr/share/php/Doctrine/Common/Collections/autoload.php',
    '/usr/share/php/Doctrine/Common/Cache/autoload.php',
    '/usr/share/php/phpDocumentor/Reflection/DocBlock/autoload.php',
));
\Fedora\Autoloader\Dependencies::optional(array(
    '/usr/share/php/Bartlett/CompatInfo/autoload.php', // Needed when installed for 'Bartlett\CompatInfo\Analyser\CompatibilityAnalyser'
    '/usr/share/php/Bartlett/UmlWriter/autoload.php',
    '/usr/share/php/Psr/Log/autoload.php',
    '/usr/share/php/Monolog/autoload.php',
));

$vendorDir = '/usr/share/php';

