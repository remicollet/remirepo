#
# RPM spec file for php-symfony-icu
#
# Copyright (c) 2013-2014 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     symfony
%global github_name      Icu
%global github_version   1.2.2
%global github_commit    d4d85d6055b87f394d941b45ddd3a9173e1e3d2a

%global composer_vendor  symfony
%global composer_project icu

# "php": ">=5.3.3"
%global php_min_ver          5.3.3
# "symfony/intl": "~2.3"
%global symfony_intl_min_ver 2.3
%global symfony_intl_max_ver 3.0
# "lib-ICU": ">=4.4"
%global libicu_min_ver       4.4

%global symfony_dir          %{_datadir}/php/Symfony

# Tests are only run with rpmbuild --with tests to avoid circular dependency
%global with_tests           %{?_with_tests:1}%{!?_with_tests:0}

Name:           php-%{composer_vendor}-%{composer_project}
Version:        %{github_version}
Release:        1%{dist}
Summary:        Symfony Icu Component

Group:          Development/Libraries
License:        MIT
URL:            https://github.com/%{github_owner}/%{github_name}
Source0:        %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
%if %{with_tests}
# For tests: composer.json
# always ok BuildRequires:  libicu >= %{libicu_min_ver}
BuildRequires:  php(language)    >= %{php_min_ver}
BuildRequires:  php-symfony-intl >= %{symfony_intl_min_ver}
BuildRequires:  php-symfony-intl <  %{symfony_intl_max_ver}
BuildRequires:  php-intl
# For tests: phpcompatinfo (computed from version 1.2.2)
BuildRequires:  php-ctype
%endif

# composer.json
# always ok Requires:       libicu  >= %{libicu_min_ver}
Requires:       php(language) >= %{php_min_ver}
Requires:       php-intl
# phpcompatinfo (computed from version 1.2.2)
Requires:       php-ctype

# Composer
Provides:       php-composer(%{composer_vendor}/%{composer_project}) = %{version}

# Disabled to prevent circular dependency
#Requires:       php-symfony-intl >= %%{symfony_intl_min_ver}
#Requires:       php-symfony-intl <  %%{symfony_intl_max_ver}
# Ensure conflicting versions are not installed
Conflicts:      php-symfony-intl <  %{symfony_intl_min_ver}
Conflicts:      php-symfony-intl >= %{symfony_intl_max_ver}
# Rename
Obsoletes:      php-symfony2-Icu < %{version}-%{release}
Provides:       php-symfony2-Icu = %{version}-%{release}


%description
Contains data of the ICU library.

You should not directly use this component. Use it through the API of the
Symfony Intl component instead.

NOTE: This package requires the Symfony Intl package (>= %{symfony_intl_min_ver}, < %{symfony_intl_max_ver})
      but does not explicitly require it to prevent a circular dependency.


%prep
%setup -qn %{github_name}-%{github_commit}


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
done | sed "s#%{buildroot}##" > %{name}.lang


%check
%if %{with_tests}
# Create autoloader
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOADER'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace('\\', '/', $class).'.php';
    @include_once $src;
});
AUTOLOADER

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit \
    --include-path %{buildroot}%{_datadir}/php \
    --exclude-group tty,benchmark \
    -d date.timezone="UTC"
%else
: Tests skipped, missing '--with tests' option
%endif


%files -f %{name}.lang
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.md composer.json
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
* Thu Jul 31 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.2-1
- Updated to 1.2.2 (BZ #1124230)

* Thu Jun 12 2014 Remi Collet <remi@fedoraproject.org> 1.2.1-3
- backport rawhide changes (composer)

* Wed Jun 11 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.1-3
- Added php-composer(%%{composer_vendor}/%%{composer_project}) virtual provide

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> 1.2.1-1
- update to 1.2.0 (backport)

* Mon Apr 28 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.1-1
- Updated to 1.2.1 (BZ #1078756)

* Wed Nov 27 2013 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.0-1
- Updated to 1.2.0

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
