# spec file for php-horde-Horde-Imap-Client
#
# Copyright (c) 2012-2013 Remi Collet
# License: CC-BY-SA
# http://creativecommons.org/licenses/by-sa/3.0/
#
# Please, preserve the changelog entries
#
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Imap_Client
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Imap-Client
Version:        2.16.2
Release:        1%{?dist}
Summary:        Horde IMAP abstraction interface

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Stream) >= 1.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
BuildRequires:  php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
# From package.xml
Requires:       php(language) >= 5.3.0
Requires:       php-hash
Requires:       php-json
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mail) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Secret) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Secret) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Socket_Client) >= 1.1.0
Requires:       php-pear(%{pear_channel}/Horde_Socket_Client) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) >= 1.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream) <  2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0
# Optional
Requires:       php-mbstring
Requires:       php-pear(%{pear_channel}/Horde_Cache) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cache) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Db) <  3.0.0
# From phpcompatinfo report for version 2.16.1
Requires:       php-date
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl
# Optional and implicilyt required :
#   Horde_Compress_Fast, Horde_Mongo, mongo

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
An abstracted API interface to various IMAP4rev1 (RFC 3501) backend
drivers.


%prep
%setup -q -c
cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find locale -name \*.po)
do
   msgfmt $po -o $(dirname $po)/$(basename $po .po).mo
done


%install
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
    test -d $loc && echo "%%lang(${lang%_*}) %{pear_datadir}/%{pear_name}/$loc"
done | tee ../%{pear_name}.lang


%check
src=$(pwd)/%{pear_name}-%{version}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit \
    -d include_path=$src/lib:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .


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
%dir %{pear_phpdir}/Horde/Imap
%{pear_phpdir}/Horde/Imap/Client
%{pear_phpdir}/Horde/Imap/Client.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale
%{pear_datadir}/%{pear_name}/migration


%changelog
* Wed Nov 27 2013 Remi Collet <remi@fedoraproject.org> - 2.16.2-1
- Update to 2.16.2

* Fri Nov 22 2013 Remi Collet <remi@fedoraproject.org> - 2.16.1-1
- Update to 2.16.1

* Thu Oct 31 2013 Remi Collet <remi@fedoraproject.org> - 2.16.0-1
- Update to 2.16.0
- add dependency: Horde_Socket_Client >= 1.1.0

* Sat Oct 12 2013 Remi Collet <remi@fedoraproject.org> - 2.15.5-1
- Update to 2.15.5

* Thu Oct 10 2013 Remi Collet <remi@fedoraproject.org> - 2.15.4-1
- Update to 2.15.4

* Tue Sep 17 2013 Remi Collet <remi@fedoraproject.org> - 2.15.3-1
- Update to 2.15.3

* Mon Sep 16 2013 Remi Collet <remi@fedoraproject.org> - 2.15.2-1
- Update to 2.15.2

* Sun Sep 08 2013 Remi Collet <remi@fedoraproject.org> - 2.15.0-1
- Update to 2.15.0

* Mon Aug 26 2013 Remi Collet <remi@fedoraproject.org> - 2.14.0-1
- Update to 2.14.0

* Wed Aug 21 2013 Remi Collet <remi@fedoraproject.org> - 2.13.1-1
- Update to 2.13.1

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 2.13.0-1
- Update to 2.13.0

* Thu Jul 25 2013 Remi Collet <remi@fedoraproject.org> - 2.12.0-1
- Update to 2.12.0
- Horde_Secret, Horde_Stream_Filter and json are now mandatory

* Tue Jun 18 2013 Remi Collet <remi@fedoraproject.org> - 2.11.6-1
- Update to 2.11.6

* Wed Jun 12 2013 Remi Collet <remi@fedoraproject.org> - 2.11.5-1
- Update to 2.11.5

* Wed Jun 05 2013 Remi Collet <remi@fedoraproject.org> - 2.11.4-1
- Update to 2.11.4

* Fri May 31 2013 Remi Collet <remi@fedoraproject.org> - 2.11.2-1
- Update to 2.11.2
- add mising requires on Horde_Translation

* Tue May 21 2013 Remi Collet <remi@fedoraproject.org> - 2.10.1-1
- Update to 2.10.1

* Sat May 18 2013 Remi Collet <remi@fedoraproject.org> - 2.10.0-1
- Update to 2.10.0

* Wed May 15 2013 Remi Collet <remi@fedoraproject.org> - 2.9.1-1
- Update to 2.9.1
- switch from Conflicts >= max to Requires < max

* Sat May 04 2013 Remi Collet <remi@fedoraproject.org> - 2.9.0-1
- Update to 2.9.0
- drop optional requires imap
- add optional dependency on Horde_Db

* Fri Apr 19 2013 Remi Collet <remi@fedoraproject.org> - 2.8.2-1
- Update to 2.8.2

* Fri Mar 29 2013 Remi Collet <remi@fedoraproject.org> - 2.8.1-1
- Update to 2.8.1

* Wed Mar 27 2013 Remi Collet <remi@fedoraproject.org> - 2.8.0-1
- Update to 2.8.0

* Sat Mar 09 2013 Remi Collet <remi@fedoraproject.org> - 2.7.2-1
- Update to 2.7.2

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.7.1-1
- Update to 2.7.1

* Tue Feb 26 2013 Remi Collet <remi@fedoraproject.org> - 2.7.0-1
- Update to 2.7.0

* Sat Feb 09 2013 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Wed Jan 23 2013 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- Update to 2.5.0

* Sat Jan  5 2013 Remi Collet <remi@fedoraproject.org> - 2.4.2-1
- Update to 2.4.2

* Fri Dec 21 2012 Remi Collet <remi@fedoraproject.org> - 2.4.1-1
- Update to 2.4.1

* Tue Dec 18 2012 Remi Collet <remi@fedoraproject.org> - 2.4.0-1
- Update to 2.4.0

* Sat Dec  8 2012 Remi Collet <remi@fedoraproject.org> - 2.3.2-1
- Update to 2.3.2

* Tue Dec  4 2012 Remi Collet <remi@fedoraproject.org> - 2.3.0-1
- Update to 2.3.0

* Wed Nov 28 2012 Remi Collet <remi@fedoraproject.org> - 2.2.3-1
- Update to 2.2.3

* Tue Nov 27 2012 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2
- review locale management

* Thu Nov 22 2012 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Mon Nov 12 2012 Remi Collet <remi@fedoraproject.org> - 2.1.6-1
- Update to 2.1.6

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.1.5-1
- Update to 2.1.5

* Tue Nov  6 2012 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Sun Nov  4 2012 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1

* Sat Nov  3 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

