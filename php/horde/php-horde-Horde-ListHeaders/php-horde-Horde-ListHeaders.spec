# remirepo/fedora spec file for php-horde-Horde-ListHeaders
#
# Copyright (c) 2013-2017 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_ListHeaders
%global pear_channel pear.horde.org

Name:           php-horde-Horde-ListHeaders
Version:        1.2.4
Release:        1%{?dist}
Summary:        Horde List Headers Parsing Library

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php-common >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-common >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional and implicitly requires Horde_Mime

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-listheaders) = %{version}


%description
The Horde_ListHeaders library parses Mailing List Headers as defined
in RFC 2369 & RFC 2919.


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
    test -d %{buildroot}%{pear_datadir}/%{pear_name}/$loc \
         && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%clean
rm -rf %{buildroot}


%check
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
%{_bindir}/phpunit .

if which php70; then
   php70 %{_bindir}/phpunit . || :
fi


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
%{pear_phpdir}/Horde/ListHeaders
%{pear_phpdir}/Horde/ListHeaders.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale


%changelog
* Tue Apr 05 2016 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2
- add dependency on Horde_Util

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1
- add provides php-composer(horde/horde-listheaders)

* Sun Nov 23 2014 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0
- raise dependency on Horde_Translation >= 2.2.0

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 1.1.5-1
- Update to 1.1.5

* Tue Jun 17 2014 Remi Collet <remi@fedoraproject.org> - 1.1.4-1
- Update to 1.1.4

* Tue Jun 10 2014 Remi Collet <remi@fedoraproject.org> - 1.1.3-1
- Update to 1.1.3
- regenerate locales during build

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- Update to 1.1.2

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- Update to 1.1.1

* Mon Oct 28 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- Update to 1.1.0

* Sat Jan 12 2013 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- Initial package
