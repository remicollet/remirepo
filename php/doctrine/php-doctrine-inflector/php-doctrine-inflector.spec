%global github_owner   doctrine
%global github_name    inflector
%global github_version 1.0
%global github_commit  a81c334f2764b09e2f13a55cfd8fe3233946f728
# Additional commits after v1.0 tag
%global github_release .20131221git%(c=%{github_commit}; echo ${c:0:7})

# "php": ">=5.3.2"
%global php_min_ver    5.3.2

Name:          php-%{github_owner}-%{github_name}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Common string manipulations with regard to casing and singular/plural rules

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: php-pear(pear.phpunit.de/PHPUnit)
# For tests: phpcompatinfo (computed from v1.0 git commit a81c334f2764b09e2f13a55cfd8fe3233946f728)
BuildRequires: php-pcre
BuildRequires: php-spl

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from v1.0 git commit a81c334f2764b09e2f13a55cfd8fe3233946f728)
Requires:      php-pcre

%description
Doctrine Inflector is a small library that can perform string manipulations
with regard to upper-/lowercase and singular/plural forms of words.


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
# Create PHPUnit config w/ colors turned off
cat phpunit.xml.dist \
    | sed 's/colors="true"/colors="false"/' \
    > phpunit.xml

%{_bindir}/phpunit --include-path ./lib:./tests -d date.timezone="UTC"


%files
%doc LICENSE *.md composer.json
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Inflector


%changelog
* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-2.20131221gita81c334
- Conditional %%{?dist}

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1.20131221gita81c334
- Initial package
