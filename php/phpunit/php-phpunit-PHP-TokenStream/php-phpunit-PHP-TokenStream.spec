%global bootstrap    0
%global gh_commit    db32c18eba00b121c145575fcbcd4d4d24e6db74
%global gh_short     %(c=%{gh_commit}; echo ${c:0:7})
%global gh_owner     sebastianbergmann
%global gh_project   php-token-stream
%global php_home     %{_datadir}/php
%global pear_name    PHP_TokenStream
%global pear_channel pear.phpunit.de
%if %{bootstrap}
%global with_tests   %{?_with_tests:1}%{!?_with_tests:0}
%else
%global with_tests   %{?_without_tests:0}%{!?_without_tests:1}
%endif

Name:           php-phpunit-PHP-TokenStream
Version:        1.4.0
Release:        1%{?dist}
Summary:        Wrapper around PHP tokenizer extension

Group:          Development/Libraries
License:        BSD
URL:            https://github.com/%{gh_owner}/%{gh_project}
Source0:        https://github.com/%{gh_owner}/%{gh_project}/archive/%{gh_commit}/%{gh_project}-%{version}.tar.gz

# Autoload template, from version 1.2.2
Source1:        Autoload.php.in

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php(language) >= 5.3.3
BuildRequires:  %{_bindir}/phpab
%if %{with_tests}
BuildRequires:  php-pear-PHPUnit >= 3.7.0
%endif

# From composer.json
#        "php": ">=5.3.3",
#        "ext-tokenizer": "*"
Requires:       php(language) >= 5.3.3
Requires:       php-tokenizer
# From phpcompatinfo report for version 1.2.2
Requires:       php-pcre
Requires:       php-spl

Provides:       php-composer(phpunit/php-token-stream) = %{version}

# For compatibility with PEAR mode
Provides:       php-pear(%{pear_channel}/%{pear_name}) = %{version}


%description
Wrapper around PHP tokenizer extension.


%prep
%setup -q -n %{gh_project}-%{gh_commit}

# Restore PSR-0 tree to ensure current sources are used by tests
mv src PHP


%build
phpab \
  --output   PHP/Token/Stream/Autoload.php \
  --template %{SOURCE1} \
  PHP


%install
rm -rf     %{buildroot}
mkdir -p   %{buildroot}%{php_home}
cp -pr PHP %{buildroot}%{php_home}/PHP


%if %{with_tests}
%check
# Use generated autoloader
sed -e 's:vendor/autoload.php:PHP/Token/Stream/Autoload.php:' \
    -i tests/bootstrap.php

# Run tests
phpunit  \
   --bootstrap tests/bootstrap.php \
   tests
%endif


%clean
rm -rf %{buildroot}


%post
if [ -x %{_bindir}/pear ]; then
   %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
      %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE
%doc README.md composer.json
%{php_home}/PHP


%changelog
* Sun Jan 18 2015 Remi Collet <remi@fedoraproject.org> - 1.4.0-1
- Update to 1.3.0

* Sun Aug 31 2014 Remi Collet <remi@fedoraproject.org> - 1.3.0-1
- Update to 1.3.0
- enable tests during build

* Wed Jun 25 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-5
- composer dependencies

* Wed Apr 30 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-3
- cleanup pear registry

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-2
- sources from github

* Mon Mar 03 2014 Remi Collet <remi@fedoraproject.org> - 1.2.2-1
- Update to 1.2.2

* Fri Sep 13 2013 Remi Collet <remi@fedoraproject.org> - 1.2.1-1
- Update to 1.2.1

* Mon Aug 05 2013 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Update to 1.2.0

* Mon Jul 29 2013 Remi Collet <remi@fedoraproject.org> - 1.1.7-1
- Update to 1.1.7

* Sat Oct  6 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.5-1
- upstream 1.1.5

* Mon Sep 24 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.4-1
- upstream 1.1.4

* Thu Feb 23 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.3-1
- upstream 1.1.3

* Mon Jan 16 2012 Remi Collet <RPMS@FamilleCollet.com> - 1.1.2-1
- upstream 1.1.2

* Fri Nov 11 2011 Remi Collet <remi@fedoraproject.org> - 1.1.1-1
- upstream 1.1.1, rebuild for remi repository

* Thu Nov 10 2011 Christof Damian <christof@damian.net> - 1.1.1-1
- upstream 1.1.1

* Tue Nov 01 2011 Remi Collet <remi@fedoraproject.org> - 1.1.0-1
- upstream 1.1.0
- no more phptok script in bindir

* Sun Dec  5 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.0.1-1
- rebuild for remi repository

* Sat Dec  4 2010 Christof Damian <christof@damian.net> - 1.0.1-1
- upstream 1.0.1

* Sun Sep 26 2010 Christof Damian <christof@damian.net> - 1.0.0-1
- upstream 1.0.0 final 

* Sat Jul 31 2010 Christof Damian <christof@damian.net> - 1.0.0-1.RC1
- upstream 1.0.0RC1

* Mon Jun 21 2010 Christof Damian <christof@damian.net> - 1.0.0-1.beta1
- upstream 1.0.0beta1
- included phptok script
- macros for version workaround

* Tue Feb 23 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.1-2
- rebuild for remi repository

* Tue Feb 23 2010 Christof Damian <christof@damian.net> - 0.9.1-2
- fix spelling

* Thu Feb 4 2010 Christof Damian <christof@damian.net> 0.9.1-1
- initial packaging

