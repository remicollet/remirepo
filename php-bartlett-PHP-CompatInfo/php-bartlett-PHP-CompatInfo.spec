%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHP_CompatInfo
%global channel   bartlett.laurent-laville.org

%global prever RC3

Name:           php-bartlett-PHP-CompatInfo
Version:        2.0.0
Release:        0.2.%{prever}%{?dist}
Summary:        Find out version and the extensions required for a piece of code to run

Group:          Development/Libraries
License:        BSD
URL:            http://php5.laurent-laville.org/compatinfo/
Source0:        http://bartlett.laurent-laville.org/get/%{pear_name}-%{version}%{?prever}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR) >= 1.9.1
BuildRequires:  php-channel(%{channel})
# to run test suite
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0
BuildRequires:  php-pear(%{channel}/PHP_Reflect) >= 0.5.0

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-xml >= 5.2.0
Requires:       php-pear(PEAR) >= 1.9.1
Requires:       php-pear(%{channel}/PHP_Reflect) >= 0.5.0
Requires:       php-pear(Console_CommandLine) >= 1.1.3
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6.1
Requires:       php-pear(pear.phpunit.de/PHPUnit) >= 3.5.0
# Optional and not yet availalble php-pear(Net_Growl) >= 2.2.2

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}%{?prever}


%description
PHP_CompatInfo will parse a file/folder/array to find out the minimum
version and extensions required for it to run. CLI version has many reports
(extension, interface, class, function, constant) to display and ability to
show content of dictionary references.


%prep
%setup -q -c

# Create a "localized" php.ini to avoid build warning
cp -pf /etc/php.ini .
echo "date.timezone=UTC" >> php.ini

# Package is V2
cd %{pear_name}-%{version}%{?prever}
mv -f ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}%{?prever}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}%{?prever}
PHPRC=../php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

# Fix wrong-script-end-of-line-encoding
sed -i -e 's/\r//' $RPM_BUILD_ROOT%{_bindir}/phpci
sed -i -e 's/\r//' $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/README.markdown


%check
cd %{pear_name}-%{version}%{?prever}

# OK (64 tests, 806 assertions) when all extensions installed
# OK, but incomplete or skipped tests!
# Tests: 56, Assertions: 478, Skipped: 10.
%{_bindir}/phpunit \
    -d date.timezone=UTC \
    --bootstrap $RPM_BUILD_ROOT%{pear_phpdir}/Bartlett/PHP/CompatInfo/Autoload.php \
    tests


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
%doc %{pear_docdir}/%{pear_name}
%dir %{pear_cfgdir}/%{pear_name}
%config(noreplace) %{pear_cfgdir}/%{pear_name}/*dist
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Bartlett/PHP/Compat*
%{pear_testdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{_bindir}/phpci


%changelog
* Fri Mar 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.2.RC3
- Version 2.0.0RC3

* Wed Feb 25 2011 Remi Collet <Fedora@FamilleCollet.com> - 2.0.0-0.1.RC2
- Version 2.0.0RC2
- Initial Release

