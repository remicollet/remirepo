# remirepo spec file for php-Assetic, from
#
# Fedora spec file for php-Assetic
#
# Copyright (c) 2013-2016 Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     kriswallsmith
%global github_name      assetic
%global github_version   1.3.2
%global github_commit    9928f7c4ad98b234e3559d1049abd13387f86db5

%global composer_vendor  kriswallsmith
%global composer_project assetic

# "php": ">=5.3.1"
%global php_min_ver 5.3.1
# "cssmin/cssmin": "3.0.1"
%global cssmin_min_ver 3.0.1
%global cssmin_max_ver 3.0.2
# "joliclic/javascript-packer": "1.1"
%global javascript_packer_min_ver 1.1
%global javascript_packer_max_ver 1.2
# "kamicane/packager": "1.0"
%global packager_min_ver 1.0
%global packager_max_ver 1.1
# "leafo/lessphp": "^0.3.7"
%global lessphp_min_ver 0.3.7
%global lessphp_max_ver 1.0
# "leafo/scssphp": "~0.1"
#     NOTE: Min version not 0.1 because autoloader required
%global scssphp_min_ver 0.1.6
%global scssphp_max_ver 1.0
# "mrclay/minify": "~2.2"
%global minify_min_ver 2.2
%global minify_max_ver 3.0
# "patchwork/jsqueeze": "~1.0|~2.0"
%global jsqueeze_min_ver 1.0
%global jsqueeze_max_ver 3.0
# "psr/log": "~1.0"
#     NOTE: Min version not 1.0 because autoloader required
%global psr_log_min_ver 1.0.0-8
%global psr_log_max_ver 2.0
# "ptachoire/cssembed": "~1.0"
%global cssembed_min_ver 1.0
%global cssembed_max_ver 2.0
# "symfony/process": "~2.1|~3.0"
#     NOTE: Min version not 2.1 because autoloader required
%global symfony_min_ver %{?el6:2.3.31}%{!?el6:2.7.1}
%global symfony_max_ver 4.0
# twig/twig": "~1.8|~2.0"
#     "conflict": "twig/twig": "<1.23"
%global twig_min_ver 1.23
%global twig_max_ver 3.0

# Conditionals for BuildRequires and Suggests
%global with_libjpeg_turbo_utils 0%{?fedora} || 0%{?rhl} >= 7
%global with_npm_clean_css       0%{?fedora} || 0%{?rhl} >= 7
%global with_npm_handlebars      0%{?fedora} || 0%{?rhl} >= 6
%global with_npm_typescript      0%{?fedora} >= 23
%global with_rubygem_compass     0%{?fedora} >= 23
%global with_rubygem_sass        0%{?fedora} >= 23
%global with_rubygem_sprockets   0%{?fedora}

# Build using "--without tests" to disable tests
%global with_tests 0%{!?_without_tests:1}

%{!?phpdir:  %global phpdir  %{_datadir}/php}

Name:          php-Assetic
Version:       %{github_version}
Release:       4%{?dist}
Summary:       Asset Management for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}

# GitHub export does not include tests.
# Run php-Assetic-get-source.sh to create full source.
Source0:       %{name}-%{github_version}-%{github_commit}.tar.gz
Source1:       %{name}-get-source.sh

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# Tests
%if %{with_tests}
## composer.json
BuildRequires: php(language)                    >= %{php_min_ver}
BuildRequires: php-composer(leafo/lessphp)      >= %{lessphp_min_ver}
BuildRequires: php-composer(leafo/scssphp)      >= %{scssphp_min_ver}
BuildRequires: php-composer(patchwork/jsqueeze) >= %{jsqueeze_min_ver}
BuildRequires: php-composer(phpunit/phpunit)
#BuildRequires: php-composer(psr/log)            >= %%{psr_log_min_ver}
BuildRequires: php-PsrLog                       >= %{psr_log_min_ver}
BuildRequires: php-composer(symfony/process)    >= %{symfony_min_ver}
BuildRequires: php-composer(twig/twig)          >= %{twig_min_ver}
## phpcompatinfo (computed from version 1.3.2)
BuildRequires: php-ctype
BuildRequires: php-curl
BuildRequires: php-date
BuildRequires: php-fileinfo
BuildRequires: php-hash
BuildRequires: php-json
BuildRequires: php-pcre
BuildRequires: php-reflection
BuildRequires: php-simplexml
BuildRequires: php-spl
BuildRequires: php-tokenizer
## Autoloader
BuildRequires: php-composer(symfony/class-loader)
## package.json
%if %{with_npm_clean_css}
BuildRequires: npm(clean-css)
%endif
%if %{with_npm_handlebars}
BuildRequires: npm(handlebars)
%endif
%if %{with_npm_typescript}
BuildRequires: npm(typescript)
%endif
## Gemfile
%if %{with_rubygem_compass}
BuildRequires: rubygem(compass)
%endif
%if %{with_rubygem_sass}
BuildRequires: rubygem(sass)
%endif
%if %{with_rubygem_sprockets}
BuildRequires: rubygem(sprockets)
%endif
## Other
%if %{with_libjpeg_turbo_utils}
BuildRequires: libjpeg-turbo-utils
%endif
BuildRequires: optipng
%endif

# composer.json
Requires:      php(language)                 >= %{php_min_ver}
Requires:      php-composer(symfony/process) >= %{symfony_min_ver}
Requires:      php-composer(symfony/process) <  %{symfony_max_ver}
# phpcompatinfo (computed from version 1.3.2)
Requires:      php-ctype
Requires:      php-curl
Requires:      php-date
Requires:      php-hash
Requires:      php-json
Requires:      php-pcre
Requires:      php-reflection
Requires:      php-spl
Requires:      php-tokenizer
# Autoloader
Requires:      php-composer(symfony/class-loader)

# Weak dependencies
%if 0%{?fedora} >= 21
Suggests:      optipng
Suggests:      php-composer(leafo/lessphp)
Suggests:      php-composer(leafo/scssphp)
Suggests:      php-composer(patchwork/jsqueeze)
Suggests:      php-composer(twig/twig)
Suggests:      php-pecl(apcu)
%if %{with_libjpeg_turbo_utils}
Suggests:      libjpeg-turbo-utils
%endif
%if %{with_npm_clean_css}
Suggests:      npm(clean-css)
%endif
%if %{with_npm_handlebars}
Suggests:      npm(handlebars)
%endif
%if %{with_npm_typescript}
Suggests:      npm(typescript)
%endif
%if %{with_rubygem_compass}
Suggests:      rubygem(compass)
%endif
%if %{with_rubygem_sass}
Suggests:      rubygem(sass)
%endif
%if %{with_rubygem_sprockets}
Suggests:      rubygem(sprockets)
%endif
%endif
Conflicts:     php-composer(leafo/lessphp)      <  %{lessphp_min_ver}
Conflicts:     php-composer(leafo/lessphp)      >= %{lessphp_max_ver}
Conflicts:     php-composer(leafo/scssphp)      <  %{scssphp_min_ver}
Conflicts:     php-composer(leafo/scssphp)      >= %{scssphp_max_ver}
Conflicts:     php-composer(patchwork/jsqueeze) <  %{jsqueeze_min_ver}
Conflicts:     php-composer(patchwork/jsqueeze) >= %{jsqueeze_max_ver}
Conflicts:     php-composer(twig/twig)          <  %{twig_min_ver}
Conflicts:     php-composer(twig/twig)          >= %{twig_max_ver}

# Standard "php-{COMPOSER_VENDOR}-{COMPOSER_PROJECT}" naming
Provides:      php-%{composer_vendor}-%{composer_project}           = %{version}-%{release}
# Composer
Provides:      php-composer(%{composer_vendor}/%{composer_project}) = %{version}

%description
Assetic is an asset management framework for PHP.

Autoloader: %{phpdir}/Assetic/autoload.php


%prep
%setup -q -n %{github_name}-%{github_commit}

: Move functions file
mv src/functions.php src/Assetic/

: Remove executable bits
chmod a-x package.json


%build
: Create autoloader
cat <<'AUTOLOAD' | tee src/Assetic/autoload.php
<?php
/**
 * Autoloader for %{name} and its' dependencies
 * (created by %{name}-%{version}-%{release}).
 *
 * @return \Symfony\Component\ClassLoader\ClassLoader
 */

if (!isset($fedoraClassLoader) || !($fedoraClassLoader instanceof \Symfony\Component\ClassLoader\ClassLoader)) {
    if (!class_exists('Symfony\\Component\\ClassLoader\\ClassLoader', false)) {
        require_once '%{phpdir}/Symfony/Component/ClassLoader/ClassLoader.php';
    }

    $fedoraClassLoader = new \Symfony\Component\ClassLoader\ClassLoader();
    $fedoraClassLoader->register();
}

$fedoraClassLoader->addPrefix('Assetic\\', dirname(__DIR__));
require_once __DIR__.'/functions.php';

// Dependencies (autoloader => required)
foreach (array(
    '%{phpdir}/Symfony/Component/Process/autoload.php' => true,
    '%{phpdir}/Leafo/ScssPhp/autoload.php'             => false,
    '%{phpdir}/lessphp/lessc.inc.php'                  => false,
    '%{phpdir}/Patchwork/JSqueeze.php'                 => false,
    '%{phpdir}/Twig/autoload.php'                      => false,
) as $dependency => $required) {
    if ($required || file_exists($dependency)) {
        require_once($dependency);
    }
}

return $fedoraClassLoader;
AUTOLOAD


%install
rm -rf %{buildroot}

mkdir -p %{buildroot}%{phpdir}
cp -rp src/Assetic %{buildroot}%{phpdir}/


%check
%if %{with_tests}
: Skip tests known to fail
rm -f \
    tests/Assetic/Test/Asset/HttpAssetTest.php \
    tests/Assetic/Test/Filter/GoogleClosure/CompilerApiFilterTest.php
sed 's/function testCompassExtensionCanBeDisabled/function SKIP_testCompassExtensionCanBeDisabled/' \
    -i tests/Assetic/Test/Filter/ScssphpFilterTest.php

: Create tests bootstrap
cat <<'BOOTSTRAP' | tee bootstrap.php
<?php
$fedoraClassLoader = require '%{buildroot}%{phpdir}/Assetic/autoload.php';
$fedoraClassLoader->addPrefix('Assetic\\Test\\', __DIR__.'/tests');
BOOTSTRAP

: Run tests
# remirepo:11
run=0
ret=0
if which php56; then
   php70 %{_bindir}/phpunit --bootstrap bootstrap.php
   run=1
fi
if which php71; then
   php70 %{_bindir}/phpunit --bootstrap bootstrap.php
   run=1
fi
if [ $run -eq 0 ]; then
: Run upstream test suite
%{_bindir}/phpunit --verbose --bootstrap bootstrap.php
# remirepo:2
fi
exit $ret
%else
: Tests skipped
%endif


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc *.json
%doc *.md
%doc docs
%doc Gemfile
%{phpdir}/Assetic


%changelog
* Mon Oct 10 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.2-4
- Skip addtional test known to fail (FTBFS in rawhide; RHBZ #1383374)

* Wed Apr 13 2016 James Hogarth <james.hogarth@gmail.com> - 1.3.2-3
- Change to using array() in autoloader to be php5.3 compatible for el6

* Wed Apr 13 2016 James Hogarth <james.hogarth@gmail.com> - 1.3.2-2
- Check if file exists and then require in the Fedora autoloader (RHBZ #1326825)

* Sat Mar 26 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.3.2-1
- Updated to 1.3.2 (RHBZ #1153986)
- Added additional non-PHP build dependencies
- Added additional non-PHP weak dependencies

* Fri Mar 25 2016 Shawn Iwinski <shawn.iwinski@gmail.com> - 1.2.1-4
- Added spec copyright header
- Included tests in source, added BuildRequires, enabled tests
- Dependencies changed to virtual provides ("php*(*)")
- Added weak dependencies suggests (Fedora >= 21)
- Added autoloader
- Added additional docs

* Mon Dec 29 2014 Adam Williamson <awilliam@redhat.com> - 1.2.1-1
- new release 1.2.1

* Tue Aug 20 2013 Remi Collet <remi@fedoraproject.org> - 1.1.2-1
- backport 1.1.2 for remi repo.

* Sun Aug 18 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.2-1
- Updated to 1.1.2

* Mon Jun 10 2013 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- backport 1.1.1 for remi repo.

* Fri Jun 07 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.1-1
- Updated to 1.1.1

* Mon Mar 11 2013 Remi Collet <remi@fedoraproject.org> - 1.1.0-0.2.alpha4
- backport for remi repo.

* Sat Mar 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-0.2.alpha4
- Updated to upstream pre-release version 1.1.0-alpha4

* Wed Feb 27 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-0.1.alpha3
- Initial package
