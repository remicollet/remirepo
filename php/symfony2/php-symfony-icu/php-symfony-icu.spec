%global github_owner          symfony
%global github_name           Icu
%global github_version        1.2.0
%global github_commit         7299cd3d8d6602103d1ebff5d0a9917b7bc6de72

%global php_min_ver           5.3.3
# "symfony/intl": "~2.3" (composer.json)
%global symfony_intl_min_ver  2.3
%global symfony_intl_max_ver  3.0
# "lib-ICU": ">=3.8" (composer.json)
%global libicu_min_ver        4.4

%global symfony_dir           %{_datadir}/php/Symfony

# Tests are only run with rpmbuild --with tests
#
# Will be run by default when the required php-symfony-intl pkg
# version is available
%global with_tests  %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-symfony-icu
Version:        %{github_version}
Release:        2%{dist}
Summary:        Symfony Icu Component

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests
# always ok BuildRequires:  libicu >= %{libicu_min_ver}
BuildRequires:  php(language)    >= %{php_min_ver}
BuildRequires:  php-symfony-intl >= %{symfony_intl_min_ver}
BuildRequires:  php-symfony-intl <  %{symfony_intl_max_ver}
# For tests: phpcompatinfo
Requires:       php-ctype
Requires:       php-intl
%endif

# always ok Requires:       libicu  >= %{libicu_min_ver}
Requires:       php(language)    >= %{php_min_ver}
# Disabled until the required php-symfony-intl pkg version is available
#Requires:       php-symfony-intl >= %%{symfony_intl_min_ver}
#Requires:       php-symfony-intl <  %%{symfony_intl_max_ver}
# phpcompatinfo
Requires:       php-ctype
Requires:       php-intl

# Rename
Obsoletes:      php-symfony2-Icu < %{version}-%{release}
Provides:       php-symfony2-Icu = %{version}-%{release}


%description
Contains data of the ICU library.

You should not directly use this component. Use it through the API of the Intl
component instead.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}%{symfony_dir}/Component/Icu
cp -rp *.php Resources Tests %{buildroot}%{symfony_dir}/Component/Icu/

# Lang files
for res_file in \
    %{buildroot}%{symfony_dir}/Component/Icu/Resources/data/*/*.res
do
    res_file_lang=$(basename $res_file | sed 's#\(_.*\)*\.res##')
    if [ "root" != "$res_file_lang" ] && \
       [ "supplementaldata" != "$res_file_lang" ]
    then
        echo "%lang($res_file_lang) $res_file"
    else
        echo "$res_file"
    fi
done > %{name}.lang
sed -i "s#%{buildroot}##" %{name}.lang


%check
%if %{with_tests}
# Create tests' autoloader
mkdir vendor
( cat <<'AUTOLOADER'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOADER
) > vendor/autoload.php

# Create PHPUnit config w/ colors turned off
cat phpunit.xml.dist \
    | sed 's/colors="true"/colors="false"/' \
    > phpunit.xml

%{_bindir}/phpunit \
    --include-path %{buildroot}%{_datadir}/php \
    --exclude-group tty,benchmark \
    -d date.timezone="UTC"
%else
: Tests skipped, missing '--with tests' option
%endif


%files -f %{name}.lang
%defattr(-,root,root,-)
%doc LICENSE *.md composer.json
%doc Resources/data/*.txt

%dir %{symfony_dir}
%dir %{symfony_dir}/Component
%dir %{symfony_dir}/Component/Icu
     %{symfony_dir}/Component/Icu/*.php
%dir %{symfony_dir}/Component/Icu/Resources
%dir %{symfony_dir}/Component/Icu/Resources/data
%dir %{symfony_dir}/Component/Icu/Resources/data/curr
%dir %{symfony_dir}/Component/Icu/Resources/data/lang
%dir %{symfony_dir}/Component/Icu/Resources/data/locales
%dir %{symfony_dir}/Component/Icu/Resources/data/region
%exclude %{symfony_dir}/Component/Icu/Resources/data/*.txt
%exclude %{symfony_dir}/Component/Icu/Tests


%changelog
* Sat Nov 23 2013 Remi Collet <remi@fedoraproject.org> 1.2.0-2
- update to 1.2.0 and backport stuff

* Mon Nov 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-2
- Renamed from "php-symfony2-icu" to "php-symfony-icu"
- Direct libicu dependency instead of using pkgconfig
- Added tests (only run with rpmbuild --with tests)
- Dependency "php-symfony2-intl" => "php-symfony-intl"

* Mon Nov 18 2013 Remi Collet <remi@fedoraproject.org> 1.2.0-2
- update to 1.2.0 and backport stuff

* Sun Nov 17 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-1
- Initial package
