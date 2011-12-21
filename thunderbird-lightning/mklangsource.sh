#!/bin/bash
# This checks out and builds the language sources.  The lightning source needs
# to already be unpacked
locales=$PWD/thunderbird-lightning-1.1/comm-beta/calendar/locales/shipped-locales
if [ ! -f $locale ]
then
  echo "ERROR: missing $locales, try fedpkg prep first"
  exit 1
fi
rm -rf l10n
mkdir l10n
cd l10n
for lang in $(<$locales)
do
  hg clone http://hg.mozilla.org/releases/l10n/mozilla-aurora/$lang
done

# Tar up, minus the mercurial files
cd ..
tar caf l10n.tar.xz --exclude='.hg*'  l10n
