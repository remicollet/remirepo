<?php
$CONFIG = array (
    "log_type" => "syslog",
    "datadirectory" => "/var/lib/owncloud/data",
    "updatechecker" => false,
    "check_for_working_htaccess" => false,
    "asset-pipeline.enabled" => false,
    "assetdirectory" => '/var/lib/owncloud',
    "preview_libreoffice_path" => '/usr/bin/libreoffice',


    "apps_paths" => array(
        0 =>
        array (
            'path'=> '/usr/share/owncloud/apps',
            'url' => '/apps',
            'writable' => false,
        ),
        1 =>
        array (
            'path' => '/var/lib/owncloud/apps',
            'url' => '/apps-appstore',
            'writable' => true,
        ),
    ),
);
