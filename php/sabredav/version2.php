<?php

spl_autoload_register(function ($class) {
    if (strpos($class, 'Sabre\\')===0) {
        $file = '/usr/share/php/'.str_replace('\\', '/', $class).'.php';
        @include $file;
    }
});

echo "\nInstalled versions PHP directory\n";
echo "Sabre_CalDAV:    " . Sabre\CalDAV\Version::VERSION . "\n";
echo "Sabre_CardDAV:   " . Sabre\CardDAV\Version::VERSION . "\n";
echo "Sabre_DAV:       " . Sabre\DAV\Version::VERSION . "\n";
echo "Sabre_DAVACL:    " . Sabre\DAVACL\Version::VERSION . "\n";
echo "Sabre_HTTP:      " . Sabre\HTTP\Version::VERSION . "\n";
echo "Sabre_VObject:   " . Sabre\VObject\Version::VERSION . "\n";

