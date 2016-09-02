# remirepo/fedora spec file for php-horde-Horde-Service-Weather
#
# Copyright (c) 2012-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Service_Weather
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Service-Weather
Version:        2.4.0
Release:        1%{?dist}
Summary:        Horde Weather Provider

Group:          Development/Libraries
License:        BSD
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Url) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-gettext
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Role) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Date) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Http) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Url) <  3.0.0
# Not documented, detected by phpci
Requires:       php-pear(%{pear_channel}/Horde_Serialize) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Serialize) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-service-weather) = %{version}


%description
Set of classes that provide an abstraction to various online weather
service providers. Includes drivers for WeatherUnderground,
WorldWeatherOnline, and Google Weather.


%prep
%setup -q -c

cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/Horde_Other.po/d' \
    -e '/%{pear_name}.mo/s/md5sum="[^"]*"//' \
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
%dir %{pear_phpdir}/Horde/Service
%{pear_phpdir}/Horde/Service/Weather
%{pear_phpdir}/Horde/Service/Weather.php
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
     %{pear_datadir}/%{pear_name}/migration
%{pear_testdir}/%{pear_name}
%{pear_hordedir}/themes


%changelog
* Fri Sep 02 2016 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Sat Jul 02 2016 Remi Collet <remi@fedoraproject.org> - 2.3.4-1
- Update to 2.3.4

* Wed Mar 16 2016 Remi Collet <remi@fedoraproject.org> - 2.3.3-1
- Update to 2.3.3

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2
- PHP 7 compatible version

* Fri Dec 04 2015 Remi Collet <remi@fedoraproject.org> - 2.3.1-1
- Update to 2.3.1
- run test suite with both PHP 5 and 7 when available

* Wed Oct 21 2015 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Sun Aug 30 2015 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Wed Mar 04 2015 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- Update to 2.1.6

* Fri Jan 09 2015 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5
- add dependency on Horde_Translation 2.2.0
- add provides php-composer(horde/horde-service-weather)

* Sun Oct 12 2014 Remi Collet <remi@fedoraproject.org> - 2.1.4-1
- Update to 2.1.4

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Thu Apr 03 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- temporary ignore test result (2 failures under investigation)

* Mon May 27 2013 Remi Collet <remi@fedoraproject.org> - 2.0.5-1
- Update to 2.0.5
- switch from Conflicts >= max to Requires < max

* Sat Apr  6 2013 Remi Collet <remi@fedoraproject.org> - 2.0.4-1
- initial package
