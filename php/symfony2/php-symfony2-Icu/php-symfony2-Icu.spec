%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_channel pear.symfony.com
%global pear_name    Icu
%global php_min_ver  5.3.3
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%global gh_commit    7299cd3d8d6602103d1ebff5d0a9917b7bc6de72
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     symfony
%global gh_project   Icu

Name:           php-symfony2-Icu
Version:        1.2.0
Release:        1%{?dist}
Summary:        Symfony2 Icu Component

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

BuildRequires:  php-pear(PEAR)
BuildRequires:  php-channel(%{pear_channel})
%if %with_tests
# For tests
BuildRequires:  php(language) >= %{php_min_ver}
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)
BuildRequires:  php-pear(%{pear_channel}/Intl) > 2.3
%endif

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-channel(%{pear_channel})
# phpci
Requires:       php-ctype
Requires:       php-intl
Requires:       php-pear(%{pear_channel}/Intl) > 2.3

# Not yet available via pear channel
# https://github.com/symfony/Icu/issues/3
Provides:       php-pear(pear.symfony.com/Icu) = %{version}

%description
Contains data of the ICU library.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

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
    $prefix = 'Symfony\\Component\\Icu\\';
    if ('\\' == $class[0]) {
        $class = substr($class, 1);
    }
    if (strpos($class, $prefix)===0) {
        $class = substr($class, strlen($prefix));
    }

    $file = str_replace('\\', '/', $class).'.php';
    @include $file;
});
PHPUNIT_AUTOLOADER
) > phpunit.autoloader.php

# Update PHPUnit config
sed -e 's#vendor/autoload.php#./phpunit.autoloader.php#' \
    -i phpunit.xml.dist



%build
# Empty build section, most likely nothing required.


%install
# Library
DESTDIR=%{buildroot}%{pear_phpdir}/Symfony/Component/%{pear_name}
install -dm 0755 $DESTDIR
install -pm 0644 *php $DESTDIR
cp -pr Resources $DESTDIR/Resources

# Documentation
DESTDIR=%{buildroot}%{pear_docdir}/%{pear_name}/Symfony/Component/%{pear_name}
install -dm 0755 $DESTDIR
install -pm 0644 LICENSE README.md composer.json $DESTDIR


%check
%if %with_tests
%{_bindir}/phpunit \
    -d include_path="%{buildroot}%{pear_phpdir}:%{buildroot}%{pear_testdir}/%{pear_name}:.:%{pear_phpdir}:%{_datadir}/php" \
    -d date.timezone="UTC"
%endif


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
%{pear_phpdir}/Symfony/Component/%{pear_name}


%changelog
* Sun Oct 27 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- initial RPM
- open https://github.com/symfony/Icu/issues/3
