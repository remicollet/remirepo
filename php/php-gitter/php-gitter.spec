%global github_owner    klaussilveira
%global github_name     gitter
%global github_version  0.2.0
%global github_commit   786e86a54121d1bb3c768e6bc93e37e431aa6264
# There are commits after the 0.2.0 version tag
%global github_release  .20131206git%(c=%{github_commit}; echo ${c:0:7})

%global lib_name        Gitter

%global php_min_ver     5.3.0
# "phpunit/phpunit": ">=3.7.1"
%global phpunit_min_ver 3.7.1
# "symfony/*": ">=2.2"
%global symfony_min_ver 2.2

Name:          php-%{github_name}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Object oriented interaction with Git repositories

Group:         Development/Libraries
License:       BSD
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch
# For tests
BuildRequires: git
BuildRequires: php(language)          >= %{php_min_ver}
BuildRequires: php-symfony-process    >= %{symfony_min_ver}
BuildRequires: php-symfony-filesystem >= %{symfony_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit) >= %{phpunit_min_ver}
# For tests: phpcompatinfo (computed from version 0.2.0 commit 786e86a54121d1bb3c768e6bc93e37e431aa6264)
BuildRequires: php-date
BuildRequires: php-pcre
BuildRequires: php-spl

Requires:      git
Requires:      php(language)       >= %{php_min_ver}
Requires:      php-symfony-process >= %{symfony_min_ver}
# phpcompatinfo (computed from version 0.2.0 commit 786e86a54121d1bb3c768e6bc93e37e431aa6264)
Requires:      php-date
Requires:      php-pcre
Requires:      php-spl

%description
Gitter allows you to interact in an object oriented manner with Git repositories
via PHP. The main goal of the library is not to replace the system git command,
but provide a coherent, stable and performatic object oriented interface.

Most commands are sent to the system's git command, parsed and then interpreted
by Gitter. Everything is transparent to you, so you don't have to worry about a
thing.


%prep
%setup -qn %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/%{lib_name} %{buildroot}/%{_datadir}/php/


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

%{_bindir}/phpunit --include-path="./lib:./tests" -d date.timezone="UTC"


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc LICENSE README.md composer.json
%{_datadir}/php/%{lib_name}


%changelog
* Fri Feb 21 2014 Remi Collet <remi@fedoraproject.org> 0.2.0-2.20131206git786e86a
- backport for remi repo

* Thu Feb 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-2.20131206git786e86a
- Conditional release dist

* Mon Jan 27 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 0.2.0-1.20131206git786e86a
- Initial package
