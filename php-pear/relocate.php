<?php 

#
# relocate.php /path/to/file prefix
# 
# Takes a file as input and a string prefix; reads
# the file as a serialized data blob and strips PREFIX
# from the beginning of each string value within the blob.
# Serializes again and writes output to stdout.
# 

$file = $_SERVER['argv'][1];
$destdir = $_SERVER['argv'][2];

$destdir_len = strlen($destdir);

function relocate_string($value) {
    global $destdir, $destdir_len;

    if (strncmp($value, $destdir, $destdir_len) == 0) {
        $value = substr($value, $destdir_len);
    }
    return $value;
}
    
function relocate_value($value) {
    if (is_string($value)) {
        $value = relocate_string($value);
    } else if (is_array($value)) {
        $value = relocate_array($value);
    }
    
    return $value;
}

function relocate_array($array) {
    $result = array();

    foreach ($array as $key => $value) {
        if (is_string($key)) {
            $key = relocate_string($key);
        }
        $result[$key] = relocate_value($value);
    }

    return $result;
}

$input = file_get_contents($file);

# Special case for /etc/pear.conf.
if (strncmp($input, "#PEAR_Config 0.9\n", 17) == 0) {
    echo substr($input, 0, 17);
    $s = substr($input, 17);
} else {
    $s = $input;
}

echo serialize(relocate_value(unserialize($s)));

?>