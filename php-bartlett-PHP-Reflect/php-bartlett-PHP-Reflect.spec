%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global channel   bartlett.laurent-laville.org
%global pear_name PHP_Reflect

Name:           php-bartlett-PHP-Reflect
Version:        0.5.0
Release:        1%{?dist}
Summary:        Adds the ability to reverse-engineer classes, interfaces, functions, constants and more

Group:          Development/Libraries
License:        BSD License
URL:            http://bartlett.laurent-laville.org/package/PHP_Reflect
Source0:        http://%{channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.2
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0

Requires:       php-pear(PEAR) >= 1.9.2
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-channel(%{channel})

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
PHP_Reflect adds the ability to reverse-engineer classes, interfaces,
functions, constants 
and more, by connecting php callbacks to other tokens.


%prep
%setup -q -c

# Create a "localized" php.ini to avoid build warning
cp -pf /etc/php.ini .
echo "date.timezone=UTC" >> php.ini

# Package is V2
cd %{pear_name}-%{version}
mv -f ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%check
cd %{pear_name}-%{version}

# OK (20 tests, 37 assertions)
%{_bindir}/phpunit \
  -d date.timezone=UTC \
  --bootstrap $RPM_BUILD_ROOT%{pear_phpdir}/Bartlett/PHP/Reflect/Autoload.php \
  tests


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Bartlett
%{pear_testdir}/PHP_Reflect


%changelog
* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.5.0-1
- Version 0.4.0 (beta) - API 0.5.0 (beta)

* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 0.4.0-1
- Version 0.4.0 (beta)
- Initial RPM package

