#!/bin/bash
# This checks out and builds the language sources.  The lightning source needs
# to already be unpacked
locales=$PWD/thunderbird-lightning-1.0/comm-release/calendar/locales/shipped-locales
if [ ! -f $locale ]
then
  echo "ERROR: missing $locales, try fedpkg prep first"
  exit 1
fi
rm -rf l10n-miramar
mkdir l10n-miramar
cd l10n-miramar
for lang in $(<$locales)
do
  hg clone http://hg.mozilla.org/releases/l10n-miramar/$lang
done

# Tar up, minus the mercurial files
cd ..
tar cjf l10n-miramar.tar.bz2 --exclude='.hg*'  l10n-miramar
