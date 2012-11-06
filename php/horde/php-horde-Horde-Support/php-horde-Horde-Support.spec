%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Support
%global pear_channel pear.horde.org

# Can run test because of circular dependency with Horde_Test
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-Horde-Support
Version:        2.0.0
Release:        2%{?dist}
Summary:        Horde support package

Group:          Development/Libraries
License:        BSD
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.0.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-channel(%{pear_channel})
Requires:       php-date
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Exception) >= 3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Stream_Wrapper) >= 2.0.0
Conflicts:      php-pear(%{pear_channel}/Horde_Stream_Wrapper) >= 3.0.0
# designed to work with php-pecl-uuid, not uuid-php
Requires:       php-pecl(uuid)
Conflicts:      uuid-php

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Support classes not tied to Horde but is used by it. These classes can be
used outside of Horde as well.


%prep
%setup -q -c -T
tar xif %{SOURCE0}

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
cd %{pear_name}-%{version}/test/$(echo %{pear_name} | sed -e s:_:/:g)
phpunit -d date.timezone=UTC AllTests.php
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


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Horde/Support
%{pear_testdir}/%{pear_name}


%changelog
* Sun Nov  4 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-2
- conflicts with uuid-php
- add optionnal %%check

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-1
- Update to 2.0.0 for remi repo

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.0.2-3
- rebuilt for new pear_testdir

* Wed Aug 01 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.0.2-2
- backport for remi repo

* Thu Jul 12 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-2
- Fix packaging issues

* Thu Jun 21 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.2-1
- Upgrade to 1.0.2

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
