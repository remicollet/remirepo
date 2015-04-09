echo "See: https://github.com/composer/composer/commits/master"

COMMIT=$(wget https://getcomposer.org/version -q -O -)
echo "Commit:" $COMMIT
echo "Short :" ${COMMIT:0:7}
wget https://github.com/composer/composer/commit/$COMMIT.patch -q -O - | grep Date:
