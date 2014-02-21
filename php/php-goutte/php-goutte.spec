%global github_owner    fabpot
%global github_name     Goutte
%global github_version  1.0.5
%global github_commit   a30e84e28fbaf14909d2d007249c24cd0ecd425e

# "php": ">=5.3.0"
%global php_min_ver     5.3.0
# "guzzle/*": "~3.1"
%global guzzle_min_ver  3.1
%global guzzle_max_ver  4.0
# "symfony/*": "~2.1"
%global symfony_min_ver 2.1
%global symfony_max_ver 3.0

Name:          php-goutte
Version:       %{github_version}
Release:       1%{?github_release}%{?dist}
Summary:       A simple PHP web scraper

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: php(language)           >= %{php_min_ver}
BuildRequires: php-symfony-browserkit  >= %{symfony_min_ver}
BuildRequires: php-symfony-browserkit  <  %{symfony_max_ver}
BuildRequires: php-symfony-cssselector >= %{symfony_min_ver}
BuildRequires: php-symfony-cssselector <  %{symfony_max_ver}
BuildRequires: php-symfony-domcrawler  >= %{symfony_min_ver}
BuildRequires: php-symfony-domcrawler  <  %{symfony_max_ver}
BuildRequires: php-symfony-finder      >= %{symfony_min_ver}
BuildRequires: php-symfony-finder      <  %{symfony_max_ver}
BuildRequires: php-symfony-process     >= %{symfony_min_ver}
BuildRequires: php-symfony-process     <  %{symfony_max_ver}
BuildRequires: php-pear(guzzlephp.org/pear/Guzzle) >= %{guzzle_min_ver}
BuildRequires: php-pear(guzzlephp.org/pear/Guzzle) <  %{guzzle_max_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo (computed from v1.0.5)
BuildRequires: php-curl

Requires:      php(language)           >= %{php_min_ver}
Requires:      php-symfony-browserkit  >= %{symfony_min_ver}
Requires:      php-symfony-browserkit  <  %{symfony_max_ver}
Requires:      php-symfony-cssselector >= %{symfony_min_ver}
Requires:      php-symfony-cssselector <  %{symfony_max_ver}
Requires:      php-symfony-domcrawler  >= %{symfony_min_ver}
Requires:      php-symfony-domcrawler  <  %{symfony_max_ver}
Requires:      php-symfony-finder      >= %{symfony_min_ver}
Requires:      php-symfony-finder      <  %{symfony_max_ver}
Requires:      php-symfony-process     >= %{symfony_min_ver}
Requires:      php-symfony-process     <  %{symfony_max_ver}
Requires:      php-pear(guzzlephp.org/pear/Guzzle) >= %{guzzle_min_ver}
Requires:      php-pear(guzzlephp.org/pear/Guzzle) <  %{guzzle_max_ver}
# phpcompatinfo (computed from v1.0.5)
Requires:      php-curl

%description
Goutte is a screen scraping and web crawling library for PHP.

Goutte provides a nice API to crawl websites and extract data
from the HTML/XML responses.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -pm 0755 %{buildroot}/%{_datadir}/php/%{github_name}
cp -p %{github_name}/Client.php %{buildroot}/%{_datadir}/php/%{github_name}/


%check
# Create tests' bootstrap
mkdir vendor
cat > vendor/autoload.php <<'AUTOLOAD'
<?php
spl_autoload_register(function ($class) {
    $src = str_replace(array('\\', '_'), '/', $class).'.php';
    @include_once $src;
});
AUTOLOAD

# Create PHPUnit config w/ colors turned off
sed 's/colors="true"/colors="false"/' phpunit.xml.dist > phpunit.xml

%{_bindir}/phpunit -d date.timezone="UTC"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.rst composer.json
%{_datadir}/php/%{github_name}


%changelog
* Fri Feb 21 2014 Remi Collet <remi@fedoraproject.org> 1.0.5-1
- backport for remi repo

* Wed Feb 19 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.5-1
- Updated to 1.0.5
- Conditional release dist
- Fixed %%files

* Mon Jan 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0.3-1.20140118gite83f8f9
- Initial package
