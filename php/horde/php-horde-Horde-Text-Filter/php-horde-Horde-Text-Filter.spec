# remirepo/fedora spec file for php-horde-Horde-Text-Filter
#
# Copyright (c) 2012-2017 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Text_Filter
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Text-Filter
Version:        2.3.5
Release:        1%{?dist}
Summary:        Horde Text Filter API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}/
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Text_Flowed) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Idna) >= 1.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Idna) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Idna) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional
Requires:       php-tidy
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) <  3.0.0
# From phpcompatinfo report for version 2.2.0
Requires:       php-dom
Requires:       php-pcre
# Optional and implicitly required: Horde_Translation
# Optional but non-free: Horde_Text_Filter_Jsmin

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-text-filter) = %{version}


%description
Common methods for fitering and converting text.

%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/Horde_Other.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml
touch -r ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Locales
for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc \
         && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)

%if 0%{?rhel} == 5
sed -e 's/testHtml2textVarious/SKIP_testHtml2textVarious/' \
    -e 's/testHtml2text/SKIP_testHtml2text/' \
    -i Html2textTest.php
sed -e 's/testBug9567/SKIP_testBug9567/' \
    -i XssTest.php
sed -e 's/testXss/SKIP_testXss/' \
    -i XssTest.php
sed -e 's/testOfficeNamespace/SKIP_testOfficeNamespace/' \
    -i MsofficeTest.php
%endif

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php70; then
   php70 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%if 0%{?rhel} == 6
# Only fails with PHP < 5.3.6, see http://3v4l.org/Vkcdu
sed -e 's/testLinkurls/SKIP_testLinkurls/' \
    -i LinkurlsTest.php
sed -e 's/testMsoNormalCss/SKIP_testMsoNormalCss/' \
    -i MsofficeTest.php
%endif

%{_bindir}/phpunit --verbose .
# remirepo:2
fi
exit $ret


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Text/Filter
%{pear_phpdir}/Horde/Text/Filter.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale


%changelog
* Wed Sep 07 2016 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- Update to 2.3.5

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Fri Jul 31 2015 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2 (no change)

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1

* Fri Apr 03 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2
- add provides php-composer(horde/horde-text-filter)
- add dependency on Horde_Idna

* Sat May 03 2014 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Wed Nov 20 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0
- upstream have move JSMin non-free code to a separate package
- add dependency on php-dom


* Thu Oct 24 2013 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5

* Thu Oct 10 2013 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Fri May 17 2013 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2
- switch from Conflicts >= max to Requires < max

* Tue May 07 2013 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.0.5-2
- fix License (review #908389)

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5

* Wed Feb  6 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-3
- cleanups for review
- always run tests but skip 2 for now

* Sun Jan 13 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-2
- remove non-free stuff

* Thu Jan 10 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4
- add option for test (need investigation)
- add patch php 5.5 compatibility (preg_replace with eval)
  http://bugs.horde.org/ticket/11943

* Tue Nov 27 2012 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Fri Nov  2 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.5-1
- Upgrade to 1.1.5

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.2-1
- Initial package
