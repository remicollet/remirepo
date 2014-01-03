%{!?__pear: %global __pear %{_bindir}/pear}
%global pear_name    Horde_Autoloader
%global pear_channel pear.horde.org

# Can run test because of circular dependency with Horde_Test
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-horde-Horde-Autoloader
Version:        2.0.1
Release:        4%{?dist}
Summary:        Horde Autoloader

Group:          Development/Libraries
License:        LGPLv2
URL:            http://pear.horde.org
Source0:        http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

# Fedora specific - ensure Sabre is taken from /usr/share/php
Patch0:         %{name}-Sabre.patch

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.7.0
BuildRequires:  php-channel(%{pear_channel})
%if %{with_tests}
# To run unit tests
BuildRequires:  php-pear(%{pear_channel}/Horde_Test) >= 2.1.0
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= 5.3.0
Requires:       php-pcre
Requires:       php-spl
Requires:       php-pear(PEAR) >= 1.7.0
Requires:       php-channel(%{pear_channel})

Provides:       php-pear(%{pear_channel}/Horde_Autoloader) = %{version}


%description
Autoload implementation and class loading manager for Horde.


%prep
%setup -q -c -T
tar xif %{SOURCE0}

cd %{pear_name}-%{version}
%patch0 -p1 -b .fedora
sed -e '/Default.php/s/md5sum=".*" name/name/' \
    ../package.xml >%{name}.xml


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
%{pear_phpdir}/Horde/Autoloader
%{pear_phpdir}/Horde/Autoloader.php
%{pear_testdir}/Horde_Autoloader


%changelog
* Fri Jan  3 2014 Remi Collet <remi@fedoraproject.org> - 2.0.1-2
- patch autoloader for Sabre

* Mon Nov 19 2012 Remi Collet <remi@fedoraproject.org> - 2.0.1-1
- Update to 2.0.1

* Mon Nov  5 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-2
- make test optional

* Thu Nov  1 2012 Remi Collet <remi@fedoraproject.org> - 2.0.0-1
- Update to 2.0.0

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-3
- rebuilt for new pear_testdir

* Sat Jun 16 2012 Remi Collet <remi@fedoraproject.org> - 1.0.1-1
- backport for remi repo

* Sat Jan 28 2012 Nick Bebout <nb@fedoraproject.org> - 1.0.1-1
- Initial package
