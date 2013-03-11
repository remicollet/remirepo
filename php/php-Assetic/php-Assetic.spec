%global github_owner        kriswallsmith
%global github_name         assetic
%global github_version      1.1.0
%global github_commit       df03baa337ae1c87803a7b1a76a393f8a59813f3
%global github_date         20130224

%global github_release      alpha4

%global php_min_ver         5.3.1

%global symfony_min_ver     2.1.0
%global symfony_max_ver     2.3
%global twig_min_ver        1.6.0
%global twig_max_ver        2.0

Name:          php-Assetic
Version:       %{github_version}
Release:       0.2.%{github_release}%{?dist}
Summary:       Asset Management for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch

Requires:      php-common >= %{php_min_ver}
Requires:      php-pear(pear.symfony.com/Process) >= %{symfony_min_ver}
Requires:      php-pear(pear.symfony.com/Process) <  %{symfony_max_ver}
# phpci
Requires:      php-ctype
Requires:      php-curl
Requires:      php-date
Requires:      php-hash
Requires:      php-json
Requires:      php-pcre
Requires:      php-spl
Requires:      php-standard
Requires:      php-tokenizer
# Optional
Requires:      php-pear(pear.twig-project.org/Twig) >= %{twig_min_ver}
Requires:      php-pear(pear.twig-project.org/Twig) <  %{twig_max_ver}
Requires:      php-lessphp
# TODO:        leafo/scssphp
#                  In progress, but waiting for upstream.
#                  https://bugzilla.redhat.com/show_bug.cgi?id=880880

%description
Assetic is an asset management framework for PHP.

Optional dependency: APC (php-pecl-apc)

Optional packages:
* https://github.com/leafo/scssphp
* https://github.com/leafo/scssphp-compass
* https://github.com/krichprollsch/phpCssEmbed


%prep
%setup -q -n %{github_name}-%{github_commit}

# Move functions file
mv src/functions.php src/Assetic/

# Remove executable bit
chmod a-x CHANGELOG-1.1.md


%build
# Empty build section, nothing to build


%install
mkdir -p -m 755 %{buildroot}%{_datadir}/php
cp -rp src/Assetic %{buildroot}%{_datadir}/php/


%check
# TODO: Work with upstream to figure out why tests are ignored for export
#       (and therefore not included in a GitHub archive)
#       https://github.com/kriswallsmith/assetic/blob/v1.1.0-alpha4/.gitattributes


%files
%doc LICENSE *.md composer.json
%{_datadir}/php/Assetic


%changelog
* Sat Mar 09 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-0.2.alpha4
- Updated to upstream pre-release version 1.1.0-alpha4

* Wed Feb 27 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.1.0-0.1.alpha3
- Initial package
