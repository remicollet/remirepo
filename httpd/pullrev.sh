#!/bin/sh

if [ $# -lt 1 ]; then
    echo "What?"
    exit 1
fi

repo="https://svn.apache.org/repos/asf/httpd/httpd/trunk"
ver=2.4.2
prefix="httpd-${ver}"
suffix="r$1${2:++}"
fn="${prefix}-${suffix}.patch"
vcurl="http://svn.apache.org/viewvc?view=revision&revision="

if test -f ${fn}; then
    mv -v -f ${fn} ${fn}\~
    sed '/^--- /,$d' < ${fn}\~ > ${fn}
else
    echo > ${fn}
fi

new=0
for r in $*; do
   if ! grep -q "${vcurl}${r}" ${fn}; then
       echo "${vcurl}${r}"
       new=1
   fi
done >> ${fn}

[ $new -eq 0 ] || echo >> ${fn}

prev=/dev/null
for r in $*; do
    echo "+ fetching ${r}"
    this=`mktemp /tmp/pullrevXXXXXX`
    svn diff -c ${r} ${repo} | filterdiff --remove-timestamps --addprefix="${prefix}/" > ${this}
    next=`mktemp /tmp/pullrevXXXXXX`
    combinediff --quiet ${prev} ${this} > ${next}
    rm -f "${this}"
    [ "${prev}" = "/dev/null" ] || rm -f "${prev}"
    prev=${next}
done

cat ${prev} >> ${fn}

vi "${fn}"
echo "+ git add ${fn}" 
git add "${fn}"
echo "+ spec template:"
echo "PatchN: ${fn}"
echo "%patchN -p1 -b .${suffix}"
