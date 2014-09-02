<?php 

#
# strip.php /path/to/file key_name
# 
# Takes a file as input and a string prefix; reads
# the file as a serialized data blob and removes a
# key with name key_name from the hash.
# Serializes again and writes output to stdout.
# 

$file = $_SERVER['argv'][1];
$key = $_SERVER['argv'][2];

function remove_key($array, $name) {
    if (array_key_exists($name, $array)) {
        unset($array[$name]);
    }

    return $array;
}

$input = file_get_contents($file);

# Special case for /etc/pear.conf.
if (strncmp($input, "#PEAR_Config 0.9\n", 17) == 0) {
    echo substr($input, 0, 17);
    $s = substr($input, 17);
} else {
    $s = $input;
}

echo serialize(remove_key(unserialize($s), $key));

?>