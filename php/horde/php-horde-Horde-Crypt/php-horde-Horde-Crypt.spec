%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Crypt
%global pear_channel pear.horde.org

Name:           php-horde-Horde-Crypt
Version:        2.2.2
Release:        1%{?dist}
Summary:        Horde Cryptography API

Group:          Development/Libraries
License:        LGPLv2
URL:            http://%{pear_channel}
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
BuildRequires:  gettext
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%if 0%{?rhel} < 6
# Don't work with GnuPG 2
BuildRequires:  gnupg < 2
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-date
Requires:       php-hash
Requires:       php-openssl
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Mime) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Filter) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Translation) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Util) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
The Horde_Crypt package class provides an API for various cryptographic
systems.

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
%doc %{pear_docdir}/%{pear_name}
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Crypt
%{pear_phpdir}/Horde/Crypt.php
%{pear_testdir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}
%dir %{pear_datadir}/%{pear_name}/locale


%changelog
* Tue Aug 27 2013 Remi Collet <remi@fedoraproject.org> - 2.2.2-1
- Update to 2.2.2

* Thu Jun 27 2013 Remi Collet <remi@fedoraproject.org> - 2.2.1-1
- Update to 2.2.1

* Tue May 07 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- Update to 2.2.0

* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.1.3-1
- Update to 2.1.3

* Mon Feb 11 2013 Remi Collet <remi@fedoraproject.org> - 2.1.2-2
- cleanups for review

* Tue Jan 29 2013 Remi Collet <remi@fedoraproject.org> - 2.1.2-1
- Update to 2.1.2

* Wed Jan  9 2013 Remi Collet <remi@fedoraproject.org> - 2.1.1-1
- Update to 2.1.1
- use local script instead of find_lang
- new test layout (requires Horde_Test 2.1.0)
- add option for test (can't be run in mock)

* Wed Nov  7 2012 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Sat Nov  3 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.2-1
- Initial package
