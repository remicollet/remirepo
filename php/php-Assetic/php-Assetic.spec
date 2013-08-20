%global github_owner   kriswallsmith
%global github_name    assetic
%global github_version 1.1.2
%global github_commit  735cffd3982c6e8cdebe292d5db39d077f65890f

Name:          php-Assetic
Version:       %{github_version}
Release:       1%{?dist}
Summary:       Asset Management for PHP

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot:     %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:     noarch

Requires:      php(language) >= 5.3.1
Requires:      php-pear(pear.symfony.com/Process) >= 2.1
Requires:      php-pear(pear.symfony.com/Process) <  3.0
# phpcompatinfo
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
Requires:      php-pear(pear.twig-project.org/Twig) >= 1.6
Requires:      php-pear(pear.twig-project.org/Twig) <  2.0
Requires:      php-lessphp
Requires:      php-scssphp

%description
Assetic is an asset management framework for PHP.

Optional dependency: APC (php-pecl-apc)

Optional packages:
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
#       https://github.com/kriswallsmith/assetic/blob/v1.1.2/.gitattributes


%files
%defattr(-,root,root,-)
%doc LICENSE *.md composer.json
%{_datadir}/php/Assetic


%changelog
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
