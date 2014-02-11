# spec file for php-horde-Horde-Stream-Wrapper
#
# Copyright (c) 2012-2014 Nick Bebout, Remi Collet
#
# License: MIT
# https://fedoraproject.org/wiki/Licensing:MIT#Modern_Style_with_sublicense
#
# Please, preserve the changelog entries
#
%{!?__pear:       %global __pear       %{_bindir}/pear}
%global pear_name    Horde_Stream_Wrapper
%global pear_channel pear.horde.org
# Disable because of circular dependency with Horde_Test
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-Horde-Stream-Wrapper
Version:        2.1.0
Release:        1%{?dist}
Summary:        Horde Stream wrappers

Group:          Development/Libraries
License:        LGPLv2+
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.0
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-spl
BuildRequires:  php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
This package provides various stream wrappers.

%prep
%setup -q -c

cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%check
%if %{with_tests}
src=$(pwd)/%{pear_name}-%{version}
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit \
    -d include_path=$src/lib:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .
%else
: Tests disabled, use --with tests to enable them
%endif


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde
%doc %{pear_docdir}/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Tue Feb 11 2014 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0
- add tests, only run when build --with tests

* Thu Nov 22 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- Update to 2.0.1 for remi repo (no change)

* Mon Nov  5 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-2
- cleanups

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Tue Aug 21 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-3.1
- rebuild

* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-3
- backport for remi repo

* Thu Jul 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-3
- Fix packaging issues

* Tue Jul 10 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-2
- Fix packaging issues

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Upgrade to 1.0.1

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.0-1
- Initial package
