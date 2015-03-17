%global github_owner    tchwork
%global github_name     jsqueeze
%global github_version  2.0.1
%global github_commit   70a8167daf0e2d5522d5d77a11e3a7d6753683ce
%global packagist_owner patchwork
%global packagist_name  jsqueeze
%global psr4_namespace  Patchwork

# phpci (uses namespacing)
%global php_min_ver         5.3.0

Name:           php-%{packagist_owner}-%{packagist_name}
Version:        %{github_version}
Release:        2%{?dist}
Summary:        Efficient JavaScript minification

Group:          Development/Libraries
License:        ASL 2.0 or GPLv2
URL:            https://github.com/%{github_owner}/%{github_name}
# Must use commit-based not tag-based github tarball:
# https://fedoraproject.org/wiki/Packaging:SourceURL#Github
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{github_name}-%{github_commit}.tar.gz

# Backported bug fixes
Patch0:         https://github.com/%{github_owner}/%{github_name}/commit/f3747ee91e3025b46e29b2128bbb83f63cbb7f2a.patch
Patch1:         https://github.com/%{github_owner}/%{github_name}/dc3c4073c2060d62a8578848c5d222a8b7608df1.patch

BuildArch:      noarch
# For tests
BuildRequires: php(language) >= %{php_min_ver}
BuildRequires: %{_bindir}/phpunit

Requires:       php(language) >= %{php_min_ver}
Requires:       php-pcre

Provides:       php-composer(%{packagist_owner}/%{packagist_name}) = %{version}


%description
JSqueeze shrinks / compresses / minifies / mangles Javascript code.
It's a single PHP class that is developed, maintained and thoroughly
tested since 2003 on major JavaScript frameworks (e.g. jQuery).

JSqueeze operates on any parse error free JavaScript code, even when
semi-colons are missing.

In term of compression ratio, it compares to YUI Compressor and
UglifyJS.


%prep
%setup -qn %{github_name}-%{github_commit}
%patch0 -p1
%patch1 -p1


%build
# Empty build section, nothing required


%install
# use PSR-0 layout relative to _datadir/php
mkdir -p %{buildroot}%{_datadir}/php/%{psr4_namespace}
cp -pr src/* %{buildroot}%{_datadir}/php/%{psr4_namespace}


%check
%{_bindir}/phpunit


%files
%{!?_licensedir:%global license %%doc}
%license LICENSE.ASL20 LICENSE.GPLv2
%doc README.md composer.json
%{_datadir}/php/%{psr4_namespace}


%changelog
* Mon Mar 16 2015 Adam Williamson <awilliam@redhat.com> - 2.0.1-2
- backport a couple of bugfixes from upstream

* Thu Jan 01 2015 Adam Williamson <awilliam@redhat.com> - 2.0.1-1
- new release, adjust for upstream PSR-4 layout change, add licenses

* Mon Dec 29 2014 Adam Williamson <awilliam@redhat.com> - 1.0.5-1
- initial package
