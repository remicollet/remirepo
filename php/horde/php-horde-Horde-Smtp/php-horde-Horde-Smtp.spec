# remirepo/fedora spec file for php-horde-Horde-Smtp
#
# Copyright (c) 2013-2016 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/4.0/
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Smtp
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Smtp
Version:        1.9.4
Release:        1%{?dist}
Summary:        Horde SMTP Client

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(pear.horde.org)
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) < 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Support) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.2.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
# From phpcompatinfo report
Requires:       php-date
Requires:       php-hash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl
# Optional
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Imap_Client) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Socket_Client) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Socket_Client) <  3
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Horde_Secret optional and implicitly required

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}
Provides:       php-composer(horde/horde-smtp) = %{version}


%description
Provides interfaces for connecting to a SMTP (RFC 5321) server to send
e-mail messages..

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
rm -rf %{buildroot}
cd %{pear_name}-%{version}
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
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}.lang
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Smtp
%{pear_phpdir}/Horde/Smtp.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale


%changelog
* Wed Dec 21 2016 Remi Collet <remi@fedoraproject.org> - 1.9.4-1
- Update to 1.9.4

* Mon Mar 21 2016 Remi Collet <remi@fedoraproject.org> - 1.9.3-1
- Update to 1.9.3

* Tue Feb 02 2016 Remi Collet <remi@fedoraproject.org> - 1.9.2-1
- Update to 1.9.2
- PHP 7 compatible version
- run test suite with both PHP 5 and 7 when available

* Tue Apr 28 2015 Remi Collet <remi@fedoraproject.org> - 1.9.1-1
- Update to 1.9.1
- add dependency on Horde_Util

* Tue Mar 10 2015 Remi Collet <remi@fedoraproject.org> - 1.9.0-1
- Update to 1.9.0
- add Provides php-composer(horde/horde-smtp)
- raise dependency on Horde_Socket_Client > 2

* Wed Jan 07 2015 Remi Collet <remi@fedoraproject.org> - 1.8.0-1
- Update to 1.8.0

* Sun Nov 23 2014 Remi Collet <remi@fedoraproject.org> - 1.7.0-1
- Update to 1.7.0
- raise dependency on Horde_Translation >= 2.2.0

* Mon Aug 04 2014 Remi Collet <remi@fedoraproject.org> - 1.6.0-1
- Update to 1.6.0

* Tue Jun 17 2014 Remi Collet <remi@fedoraproject.org> - 1.5.2-1
- Update to 1.5.2

* Tue Jun 10 2014 Remi Collet <remi@fedoraproject.org> - 1.5.1-1
- Update to 1.5.1

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 1.5.0-1
- Update to 1.5.0

* Fri Apr 04 2014 Remi Collet <remi@fedoraproject.org> - 1.4.1-1
- Update to 1.4.1
- add gettext for provided locales

* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.4.0
- Add dependency on Horde_Translation

* Fri Nov 22 2013 Remi Collet <remi@fedoraproject.org> - 1.3.1-1
- Update to 1.3.1

* Thu Oct 31 2013 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- raise dependency: Horde_Socket_Client >= 1.1.0

* Wed Oct 23 2013 Remi Collet <remi@fedoraproject.org> - 1.2.6-1
- Update to 1.2.6

* Sat Oct 19 2013 Remi Collet <remi@fedoraproject.org> - 1.2.5-1
- Update to 1.2.5
- add dependency: Horde_Socket_Client

* Tue Oct 15 2013 Remi Collet <remi@fedoraproject.org> - 1.2.4-1
- Update to 1.2.4

* Thu Sep 12 2013 Remi Collet <remi@fedoraproject.org> - 1.2.3-1
- Update to 1.2.3

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Wed Aug 28 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Fri Aug 23 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- initial package
