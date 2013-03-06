%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

%global pear_channel pear.symfony.com
%global pear_name    %(echo %{name} | sed -e 's/^php-symfony2-//' -e 's/-/_/g')
%global php_min_ver  5.3.3
# Circular dependency with Form
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-symfony2-PropertyAccess
Version:        2.2.0
Release:        1%{?dist}
Summary:        Symfony2 %{pear_name} Component

Group:          Development/Libraries
License:        MIT
URL:            http://symfony.com/components
Source0:        http://pear.symfony.com/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= %{php_min_ver}
BuildRequires:  php-pear(PEAR)
%if %{with_tests}
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:  php-pear(%{pear_channel}/Form) >= 2.2.0
%endif

BuildRequires:  php-ctype
BuildRequires:  php-pcre
BuildRequires:  php-reflection
BuildRequires:  php-spl
BuildRequires:  php-channel(%{pear_channel})

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php(language) >= %{php_min_ver}
Requires:       php-ctype
Requires:       php-pcre
Requires:       php-reflection
Requires:       php-spl
Requires:       php-pear(PEAR)
Requires:       php-channel(pear.symfony.com)

Provides:       php-pear(pear.symfony.com/%{pear_name}) = %{version}


%description
Symfony2 PropertyAccess Component

%prep
%setup -q -c

# Modify PEAR package.xml file:
# - Remove .gitignore file
# - Change role from "php" to "doc" for CHANGELOG.md file
# - Change role from "php" to "test" for all test files
# - Remove md5sum from bootsrap.php file since it was patched
sed -e '/\.git/d' \
    -e '/CHANGELOG.md/s/role="php"/role="doc"/' \
    -e '/phpunit.xml.dist/s/role="php"/role="test"/' \
    -e '/Tests/s/role="php"/role="test"/' \
    -i package.xml

# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, most likely nothing required.


%install
rm -rf %{buildroot}
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

sed -e '/bootstrap/s:vendor/autoload.php:%{pear_phpdir}/Symfony/Component/%{pear_name}/autoloader.php:' \
      %{buildroot}%{pear_testdir}/%{pear_name}/Symfony/Component/%{pear_name}/phpunit.xml.dist \
    > %{buildroot}%{pear_testdir}/%{pear_name}/Symfony/Component/%{pear_name}/phpunit.xml


%check
%if %{with_tests}
cd %{pear_name}-%{version}/Symfony/Component/%{pear_name}
sed -e '/bootstrap/s:vendor/autoload.php:autoloader.php:' \
    phpunit.xml.dist > phpunit.xml
%{_bindir}/phpunit -d date.timezone=UTC
%else
: Tests skipped, missing '--with tests' option
%endif


%clean
rm -rf %{buildroot}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.symfony.com/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Symfony/Component/%{pear_name}
%{pear_testdir}/%{pear_name}



%changelog
* Wed Mar 06 2013 Remi Collet <remi@fedoraproject.org> - 2.2.0-1
- New package
