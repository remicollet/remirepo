echo "See: https://github.com/composer/composer/commits/master"

COMMIT=$(wget https://getcomposer.org/version -q -O -)
echo Commit: $COMMIT

wget https://github.com/composer/composer/commit/$COMMIT.patch -q -O - | grep Date:
