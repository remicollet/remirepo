%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Translation

Name:           php-horde-Horde-Translation
Version:        1.0.1
Release:        1%{?dist}
Summary:        Horde translation library

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz
# /usr/lib/rpm/find-lang.sh from fedora 16
Source1:        find-lang.sh

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(pear.horde.org)
BuildRequires:  gettext

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(pear.horde.org)
Requires:       php-common >= 5.2.0
Requires:       php-pear(PEAR) >= 1.7.0

Provides:       php-pear(pear.horde.org/Horde_Translation) = %{version}


%description
Translation wrappers.

%prep
%setup -q -c
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
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

%if 0%{?fedora} > 13
%find_lang %{pear_name}
%find_lang Horde_Other
%else
sh %{SOURCE1} $RPM_BUILD_ROOT %{pear_name}
sh %{SOURCE1} $RPM_BUILD_ROOT Horde_Other
%endif
cat Horde_Other.lang >> %{pear_name}.lang
cat %{pear_name}.lang

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files -f %{pear_name}-%{version}/%{pear_name}.lang
%defattr(-,root,root,-)
# own locales (non standard) directories, .mo own by find_lang
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Horde
%{pear_phpdir}/Horde/Translation
%{pear_phpdir}/Horde/Translation.php
# own locales (non standard) directories, .mo own by find_lang
%dir %{pear_testdir}/Horde_Translation
%dir %{pear_testdir}/Horde_Translation/Horde
%dir %{pear_testdir}/Horde_Translation/Horde/Translation
%dir %{pear_testdir}/Horde_Translation/Horde/Translation/locale
%dir %{pear_testdir}/Horde_Translation/Horde/Translation/locale/de
%dir %{pear_testdir}/Horde_Translation/Horde/Translation/locale/de/LC_MESSAGES
%{pear_testdir}/Horde_Translation/Horde/Translation/*.php


%changelog
* Mon Feb 20 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
