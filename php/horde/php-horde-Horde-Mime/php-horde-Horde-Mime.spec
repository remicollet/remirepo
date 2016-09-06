# remirepo/fedora spec file for php-horde-Horde-Mime
#
# Copyright (c) 2012-2016 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global bootstrap    0
%global pear_name    Horde_Mime
%global pear_channel pear.horde.org
%if %{bootstrap}
# Can run test because of circular dependency with Horde_Mail
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-horde-Horde-Mime
Version:        2.10.1
Release:        1%{?dist}
Summary:        Horde MIME Library

Group:          Development/Libraries
# lib/Horde/Mime.php is BSD and LGPLv2
# other files are LGPLv2
License:        LGPLv2 and BSD
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Support) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Mail) >= 2.5.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-fileinfo
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_ListHeaders) >= 1.2.0
Requires:       php-pear(%{pear_channel}/Horde_ListHeaders) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.5.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) >= 1.3.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.1.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Flowed) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Nls) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Nls) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Text_Filter) <  3.0.0
Requires:       php-intl
Requires:       php-pear(Net_DNS2)

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-mime) = %{version}


%description
Provides methods for dealing with MIME (RFC 2045) and related e-mail (RFC
822/2822/5322) standards.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}\.po/d' \
    -e '/%{pear_name}\.mo/s/md5sum=.*name=/name=/' \
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
cd %{pear_name}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

for loc in locale/{??,??_??}
do
    lang=$(basename $loc)
    test -d $loc && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%if 0%{?rhel} == 5
rm MdnTest.php
%endif

# remirepo:11
run=0
ret=0
if which php56; then
   php56 %{_bindir}/phpunit . || ret=1
   run=1
fi
if which php71; then
   php71 %{_bindir}/phpunit . || ret=1
   run=1
fi
if [ $run -eq 0 ]; then
%{_bindir}/phpunit --verbose .
# remirepo:2
fi
exit $ret
%else
: bootstrap build with test suite disabled
%endif


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
%{pear_phpdir}/Horde/Mime
%{pear_phpdir}/Horde/Mime.php
%{pear_testdir}/%{pear_name}
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale


%changelog
* Tue Sep 06 2016 Remi Collet <remi@fedoraproject.org> - 2.10.1-1
- Update to 2.10.1

* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 2.10.0-1
- Update to 2.10.0

* Thu Jun 02 2016 Remi Collet <remi@fedoraproject.org> - 2.9.5-1
- Update to 2.9.5

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 2.9.4-1
- Update to 2.9.4

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.9.3-1
- Update to 2.9.3
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Wed Sep 02 2015 Remi Collet <remi@fedoraproject.org> - 2.9.2-1
- Update to 2.9.2

* Fri May 22 2015 Remi Collet <remi@fedoraproject.org> - 2.9.1-1
- Update to 2.9.1

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- Update to 2.9.0

* Tue Apr 14 2015 Remi Collet <remi@fedoraproject.org> - 2.8.1-1
- Update to 2.8.1

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0

* Wed Jan 21 2015 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0
- add provides php-composer(horde/horde-mime)

* Mon Dec 29 2014 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Fri Dec 05 2014 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Tue Nov 25 2014 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2
- enable test suite

* Mon Nov 24 2014 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1

* Sun Nov 23 2014 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0
- add dependency on Horde_ListHeaders
- raise dependency on Horde_Mail >= 2.5.0
- raise dependency on Horde_Translation >= 2.2.0

* Thu Aug 28 2014 Remi Collet <remi@fedoraproject.org> - 2.4.5-1
- Update to 2.4.5

* Sun Aug 03 2014 Remi Collet <remi@fedoraproject.org> - 2.4.4-1
- Update to 2.4.4

* Wed Jul 09 2014 Remi Collet <remi@fedoraproject.org> - 2.4.3-1
- Update to 2.4.3

* Mon Jun 23 2014 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 2.3.5-1
- Update to 2.3.5

* Sat May 10 2014 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4

* Sat May 03 2014 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Tue Apr 22 2014 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1

* Tue Mar 11 2014 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 2.2.9-1
- Update to 2.2.9

* Fri Nov 22 2013 Remi Collet <remi@fedoraproject.org> - 2.2.8-1
- Update to 2.2.8

* Sat Sep 28 2013 Remi Collet <remi@fedoraproject.org> - 2.2.7-1
- Update to 2.2.7

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 2.2.5-1
- Update to 2.2.5

* Wed Aug 07 2013 Remi Collet <remi@fedoraproject.org> - 2.2.4-1
- Update to 2.2.4
- add Requires Horde_Stream >= 1.3.0

* Wed Jul 17 2013 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0
- switch from Conflicts >= max to Requires < max

* Fri Apr 19 2013 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Tue Apr 09 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- Requires Horde_Support >= 2.1.0

* Tue Mar 26 2013 Nick Bebout <nb@fedoraproject.org> - 2.0.4-2
- Update for review

* Tue Feb 12 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- Update to 2.0.4

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 2.0.3-1
- Update to 2.0.3
- drop merged patch for http://bugs.horde.org/ticket/11913

* Sat Jan  5 2013 Remi Collet <remi@fedoraproject.org> - 2.0.2-1
- Update to 2.0.2

* Fri Dec 21 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- patch for php 5.5

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Fri Nov  2 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.4.1-1
- Initial package
