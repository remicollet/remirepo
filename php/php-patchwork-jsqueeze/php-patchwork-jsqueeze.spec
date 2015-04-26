%global github_owner    tchwork
%global github_name     jsqueeze
%global github_version  2.0.2
%global github_commit   2e581762884cfd035d9b148794ef2a4ab2c3b893
%global packagist_owner patchwork
%global packagist_name  jsqueeze
%global psr4_namespace  Patchwork

# phpci (uses namespacing)
%global php_min_ver         5.3.0

Name:           php-%{packagist_owner}-%{packagist_name}
Version:        %{github_version}
Release:        1%{?dist}
Summary:        Efficient JavaScript minification

Group:          Development/Libraries
License:        ASL 2.0 or GPLv2
URL:            https://github.com/%{github_owner}/%{github_name}
# Must use commit-based not tag-based github tarball:
# https://fedoraproject.org/wiki/Packaging:SourceURL#Github
Source0:        https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{github_name}-%{github_commit}.tar.gz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
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


%build
# Empty build section, nothing required


%install
rm -rf %{buildroot}
# use PSR-0 layout relative to _datadir/php
mkdir -p %{buildroot}%{_datadir}/php/%{psr4_namespace}
cp -pr src/* %{buildroot}%{_datadir}/php/%{psr4_namespace}


%check
%{_bindir}/phpunit


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.ASL20 LICENSE.GPLv2
%doc README.md composer.json
%{_datadir}/php/%{psr4_namespace}


%changelog
* Sat Apr 25 2015 Adam Williamson <awilliam@redhat.com> - 2.0.2-1
- new release 2.0.2

* Tue Mar 17 2015 Remi Collet <remmi@fedoraproject.org> - 2.0.1-2
- add backport stuff for #remirepo

* Mon Mar 16 2015 Adam Williamson <awilliam@redhat.com> - 2.0.1-2
- backport a couple of bugfixes from upstream

* Thu Jan 01 2015 Adam Williamson <awilliam@redhat.com> - 2.0.1-1
- new release, adjust for upstream PSR-4 layout change, add licenses

* Mon Dec 29 2014 Adam Williamson <awilliam@redhat.com> - 1.0.5-1
- initial package
