%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Translation
%global pear_channel pear.horde.org

# Can run test because of circular dependency with Horde_Test
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-Horde-Translation
Version:        2.0.0
Release:        2%{?dist}
Summary:        Horde translation library

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  gettext
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.0.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php(language) >= 5.3.0
Requires:       php-gettext
Requires:       php-spl

Provides:       php-pear(%{pear_channel}/Horde_Translation) = %{version}


%description
Translation wrappers.

%prep
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}

# Don't install .po and .pot files
# Remove checksum for .mo, as we regenerate them
sed -e '/%{pear_name}.po/d' \
    -e '/Horde_Other.po/d' \
    -e '/%{pear_name}.mo/s/md5sum=.*name=/name=/' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}

# Regenerate the locales
for po in $(find test -name \*.po)
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

%if 0%{?fedora} > 13
%find_lang %{pear_name}
%find_lang Horde_Other
%else
sh %{SOURCE1} %{buildroot} %{pear_name}
sh %{SOURCE1} %{buildroot} Horde_Other
%endif
cat Horde_Other.lang >> %{pear_name}.lang
cat %{pear_name}.lang


%check
%if %{with_tests}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit AllTests.php
%else
: Test disabled, missing '--with tests' option.
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}-%{version}/%{pear_name}.lang
%defattr(-,root,root,-)
# own locales (non standard) directories, .mo own by find_lang
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Horde
%{pear_phpdir}/Horde/Translation
%{pear_phpdir}/Horde/Translation.php
%doc %{pear_docdir}/Horde_Translation
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_testdir}/Horde_Translation
%dir %{pear_testdir}/Horde_Translation/Horde
%dir %{pear_testdir}/Horde_Translation/Horde/Translation
%dir %{pear_testdir}/Horde_Translation/Horde/Translation/locale
%dir %{pear_testdir}/Horde_Translation/Horde/Translation/locale/de
%dir %{pear_testdir}/Horde_Translation/Horde/Translation/locale/de/LC_MESSAGES
%{pear_testdir}/Horde_Translation/Horde/Translation/*.php


%changelog
* Mon Nov  5 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-2
- make test optionnal

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0.2-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-1
- Upgrade to 1.0.2, backport for remi repo

* Thu Jun 14 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-1
- Upgrade to 1.0.2

* Mon Feb 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
