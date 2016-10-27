<?php
/* Autoloader for robmorgan/phinx and its dependencies */

require_once '/usr/share/php/Fedora/Autoloader/autoload.php';

\Fedora\Autoloader\Autoload::addPsr4('Phinx\\', __DIR__);
\Fedora\Autoloader\Dependencies::required(array(
    '/usr/share/php/Symfony/Component/autoload.php',
));
