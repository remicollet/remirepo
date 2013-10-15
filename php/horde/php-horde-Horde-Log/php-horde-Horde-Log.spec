%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name    Horde_Log
%global pear_channel pear.horde.org

# Can run test because of circular dependency with Horde_Test
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-Horde-Log
Version:        2.1.0
Release:        1%{?dist}
Summary:        Horde Logging library

Group:          Development/Libraries
License:        BSD
URL:            http://%{pear_channel}
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
Requires:       php-date
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})
Requires:       php-pear(%{pear_channel}/Horde_Constraint) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Constraint) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Exception) <  3.0.0
# Optional
Requires:       php-dom
Requires:       php-pear(%{pear_channel}/Horde_Cli) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Cli) <  3.0.0
Requires:       php-pear(%{pear_channel}/Horde_Scribe) >= 2.0.0
Requires:       php-pear(%{pear_channel}/Horde_Scribe) <  3.0.0

Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Horde Logging package with configurable handlers, filters, and formatting.

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
phpunit\
    -d include_path=%{buildroot}%{pear_phpdir}:.:%{pear_phpdir} \
    -d date.timezone=UTC \
    .
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
%{pear_phpdir}/Horde/Log
%{pear_phpdir}/Horde/Log.php
%{pear_testdir}/Horde_Log


%changelog
* Tue Oct 15 2013 Remi Collet <remi@fedoraproject.org> - 2.1.0-1
- Update to 2.1.0

* Mon Nov 19 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.1-1
- Update to 2.0.1 for remi repo

* Mon Nov  5 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-3
- requires Horde_Scribe
- make test optional

* Thu Nov  1 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.0.0-2
- Update to 2.0.0 for remi repo

* Thu Aug 2 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.2-2
- Fix packaging issues

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.1.2-1
- Initial package
