#/bin/sh

RPM=$(which rpm)

if [ -z "$RPM" ]
then
    echo "ERROR: 'rpm' command not found" 1>&2
    exit 1
fi

function print {
    echo -e "\e[0;33m>>>>> ${1}\e[0m"
}

if [ -x "$1" ]
then
    SPEC=$1
else
    SPEC=`ls *.spec | head -1`
fi

print "SPEC = $SPEC"

NAME=$(echo $SPEC | sed 's#\.spec##')
VERSION=$(egrep '%global\s*github_version' $SPEC | awk '{print $3}')

print "NAME = $NAME"
print "VERSION = $VERSION"

GIT_OWNER=$(egrep '%global\s*github_owner' $SPEC | awk '{print $3}')
GIT_NAME=$(egrep '%global\s*github_name' $SPEC | awk '{print $3}')
GIT_COMMIT=$(egrep '%global\s*github_commit' $SPEC | awk '{print $3}')
GIT_REPO=https://github.com/${GIT_OWNER}/${GIT_NAME}
SOURCE_FILENAME=${NAME}-${VERSION}-${GIT_COMMIT}.tar.gz
RPM_SOURCE_DIR=$(rpm --eval "%{_sourcedir}")

print "GIT_OWNER = $GIT_OWNER"
print "GIT_NAME = $GIT_NAME"
print "GIT_COMMIT = $GIT_COMMIT"
print "GIT_REPO = $GIT_REPO"
print "SOURCE_FILENAME = $SOURCE_FILENAME"
print "RPM_SOURCE_DIR = $RPM_SOURCE_DIR"

pushd /tmp
    print "Getting full source..."
    rm -f ${SOURCE_FILENAME}
    wget https://github.com/${GIT_OWNER}/${GIT_NAME}/archive/${GIT_COMMIT}/${SOURCE_FILENAME}

    print "Uncompressing full source..."
    tar -xvzf ${SOURCE_FILENAME}
    rm -f ${SOURCE_FILENAME}

    print "Removing non-allowable licened content..."
    rm -rf ${GIT_NAME}-${GIT_COMMIT}/doc

    print "Re-compressing allowable source..."
    rm -f ${RPM_SOURCE_DIR}/${SOURCE_FILENAME}
    tar -cvzf ${RPM_SOURCE_DIR}/${SOURCE_FILENAME} ${GIT_NAME}-${GIT_COMMIT}
    rm -rf ${GIT_NAME}-${GIT_COMMIT}

    print "Source = \"${RPM_SOURCE_DIR}/${SOURCE_FILENAME}\""
popd
