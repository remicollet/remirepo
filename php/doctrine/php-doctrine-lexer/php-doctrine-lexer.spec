%global github_owner   doctrine
%global github_name    lexer
%global github_version 1.0
%global github_commit  f12a5f74e5f4a9e3f558f3288504e121edfad891
# Additional commits after v1.0 tag
%global github_release .20131220git%(c=%{github_commit}; echo ${c:0:7})

# "php": ">=5.3.2"
%global php_min_ver    5.3.2

Name:          php-%{github_owner}-%{github_name}
Version:       %{github_version}
Release:       2%{?github_release}%{?dist}
Summary:       Base library for a lexer that can be used in top-down, recursive descent parsers

Group:         Development/Libraries
License:       MIT
URL:           https://github.com/%{github_owner}/%{github_name}
Source0:       %{url}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildArch:     noarch

Requires:      php(language) >= %{php_min_ver}
# phpcompatinfo (computed from v1.0 git commit f12a5f74e5f4a9e3f558f3288504e121edfad891)
Requires:      php-pcre
Requires:      php-reflection

%description
Base library for a lexer that can be used in top-down, recursive descent
parsers.

This lexer is used in Doctrine Annotations and in Doctrine ORM (DQL).


%prep
%setup -q -n %{github_name}-%{github_commit}


%build
# Empty build section, nothing required


%install
mkdir -p %{buildroot}/%{_datadir}/php
cp -rp lib/* %{buildroot}/%{_datadir}/php/


%check
# No upstream tests


%files
%doc LICENSE *.md composer.json
%dir %{_datadir}/php/Doctrine
%dir %{_datadir}/php/Doctrine/Common
     %{_datadir}/php/Doctrine/Common/Lexer


%changelog
* Mon Jan 06 2014 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-2.20131220gitf12a5f7
- Conditional %%{?dist}

* Mon Dec 23 2013 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1.20131220gitf12a5f7
- Initial package
