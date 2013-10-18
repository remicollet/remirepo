%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}

%global pear_channel    pear.symfony.com
%global pear_name       Debug
%global php_min_ver     5.3.3

%global symfony_min_ver 2.1
%global symfony_max_ver 3.0

Name:             php-symfony2-%{pear_name}
Version:          2.3.6
Release:          1%{?dist}
Summary:          Symfony2 %{pear_name} Component

Group:            Development/Libraries
License:          MIT
URL:              http://symfony.com/doc/current/components/debug.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch

BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})
# For tests
BuildRequires:    php-common >= %{php_min_ver}
BuildRequires:    php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:    php-pear(%{pear_channel}/HttpFoundation) >= %{symfony_min_ver}
BuildRequires:    php-pear(%{pear_channel}/HttpFoundation) <  %{symfony_max_ver}
BuildRequires:    php-pear(%{pear_channel}/HttpKernel) >= %{symfony_min_ver}
BuildRequires:    php-pear(%{pear_channel}/HttpKernel) <  %{symfony_max_ver}
# For tests: phpci
BuildRequires:    php-reflection
BuildRequires:    php-spl

Requires:         php-common >= %{php_min_ver}
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci
Requires:         php-reflection
Requires:         php-spl
# Optional
Requires:         php-pear(%{pear_channel}/ClassLoader) >= %{symfony_min_ver}
Requires:         php-pear(%{pear_channel}/ClassLoader) <  %{symfony_max_ver}
Requires:         php-pear(%{pear_channel}/HttpFoundation) >= %{symfony_min_ver}
Requires:         php-pear(%{pear_channel}/HttpFoundation) <  %{symfony_max_ver}
Requires:         php-pear(%{pear_channel}/HttpKernel) >= %{symfony_min_ver}
Requires:         php-pear(%{pear_channel}/HttpKernel) <  %{symfony_max_ver}

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
The Debug Component provides tools to ease debugging PHP code.

Optional: Xdebug


%prep
%setup -q -c

# Create PHPUnit autoloader
( cat <<'PHPUNIT_AUTOLOADER'
<?php

# This file was created by RPM packaging and is not part of the original
# Symfony2 %{pear_name} PEAR package.

set_include_path(
    '%{pear_testdir}/%{pear_name}'.PATH_SEPARATOR.
    get_include_path()
);

spl_autoload_register(function ($class) {
    if ('\\' == $class[0]) {
        $class = substr($class, 1);
    }

    $file = str_replace('\\', '/', $class).'.php';
    @include $file;
});
PHPUNIT_AUTOLOADER
) > phpunit.autoloader.php

# Update PHPUnit config
sed -e 's#vendor/autoload.php#./phpunit.autoloader.php#' \
    -i %{pear_name}-%{version}/Symfony/Component/%{pear_name}/phpunit.xml.dist

# Modify PEAR package.xml file:
# - Change role from "php" to "test" for all test files
# - Remove md5sum from phpunit.xml.dist file since it was updated
sed -e '/Tests/s/role="php"/role="test"/' \
    -e '/phpunit.xml.dist/s/role="php"/role="test"/' \
    -e '/phpunit.xml.dist/s/md5sum="[^"]*"\s*//' \
    -i package.xml

# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}

# Install PHPUnit autoloader
install -pm 0644 ../phpunit.autoloader.php \
    %{buildroot}/%{pear_testdir}/%{pear_name}/Symfony/Component/%{pear_name}/


%check
cd %{pear_name}-%{version}/Symfony/Component/%{pear_name}

cp ../../../../phpunit.autoloader.php .

%{_bindir}/phpunit \
    -d include_path="%{buildroot}%{pear_phpdir}:%{buildroot}%{pear_testdir}/%{pear_name}:.:%{pear_phpdir}:%{_datadir}/php" \
    -d date.timezone="UTC"


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
%{pear_phpdir}/Symfony/Component/%{pear_name}
%{pear_testdir}/%{pear_name}


%changelog
* Fri Oct 18 2013 Remi Collet <remi@fedoraproject.org> - 2.3.6-1
- Update to 2.3.6

* Fri Jun 14 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.1-1
- Initial package
