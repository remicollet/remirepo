<?php

if (function_exists("uuid_export")) {
    echo "Version: ".uuid_version()."\n";
    if (uuid_create($uuid)) {
        die("Can't create\n");
    }
    for ($i=0 ; $i<10 ; $i++) {
        if (!uuid_make($uuid, UUID_MAKE_V4) && !uuid_export($uuid, UUID_FMT_STR, $str)) {
            echo "$i:   $str\n";
        }
    }
    uuid_destroy($uuid);
} else if (function_exists("uuid_create")) {
    for ($i=0 ; $i<10 ; $i++) {
        echo "$i:   ".uuid_create()."\n";
    }
} else {
    die ("No UUID extension\n");
}

