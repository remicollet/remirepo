#
# RPM spec file for php-aws-sdk
#
# Copyright (c) 2013-2014 Joseph Marrero <jmarrero@fedoraproject.org>
#                         Gregor Tätzner <brummbq@fedoraproject.org>
#                         Shawn Iwinski <shawn.iwinski@gmail.com>
#
# License: MIT
# http://opensource.org/licenses/MIT
#
# Please preserve changelog entries
#

%global github_owner     aws
%global github_name      aws-sdk-php
%global github_version   2.7.6
%global github_commit    26df03201f01d81dc6e7f903285b3f4bdaaca7d4

%global composer_vendor  aws
%global composer_project aws-sdk-php

%global pear_channel     pear.amazonwebservices.com
%global pear_name        sdk

# "php": ">=5.3.3"
%global php_min_ver      5.3.3
# "guzzle/guzzle": "~3.7"
%global guzzle_min_ver   3.7
%global guzzle_max_ver   4.0
# "doctrine/cache": "~1.0"
%global cache_min_ver    1.0
%global cache_max_ver    2.0
# "monolog/monolog": "~1.4"
%global monolog_min_ver  1.4
%global monolog_max_ver  2.0
# "symfony/yaml": "~2.1"
%global yaml_min_ver     2.1
%global yaml_max_ver     3.0

Name:      php-aws-sdk
Version:   %{github_version}
Release:   1%{?dist}
Summary:   Amazon Web Services framework for PHP

Group:     Development/Libraries
License:   ASL 2.0
URL:       http://aws.amazon.com/sdk-for-php/
Source0:   https://github.com/%{github_owner}/%{github_name}/archive/%{github_commit}/%{name}-%{github_version}-%{github_commit}.tar.gz

BuildRoot: %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch: noarch

# composer.json
Requires:  php(language)     >= %{php_min_ver}
Requires:  php-guzzle-Guzzle >= %{guzzle_min_ver}
Requires:  php-guzzle-Guzzle <  %{guzzle_max_ver}
# composer.json: optional
Requires:  php-openssl
# phpcompatinfo (computed from version 2.7.1)
Requires:  php-curl
Requires:  php-date
Requires:  php-hash
Requires:  php-json
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-session
Requires:  php-simplexml
Requires:  php-spl

# Optional package version checks
Conflicts: php-composer(doctrine/cache)  <  %{cache_min_ver}
Conflicts: php-composer(doctrine/cache)  >= %{cache_max_ver}
Conflicts: php-composer(monolog/monolog) <  %{monolog_min_ver}
Conflicts: php-composer(monolog/monolog) >= %{monolog_max_ver}
Conflicts: php-symfony-yaml              <  %{yaml_min_ver}
Conflicts: php-symfony-yaml              >= %{yaml_max_ver}

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:  php-pear(%{pear_channel}/%{pear_name}) = %{version}

# This pkg was the only one in this channel so the channel is no longer needed
Obsoletes: php-channel-aws

%description
Amazon Web Services SDK for PHP enables developers to build solutions for
Amazon Simple Storage Service (Amazon S3), Amazon Elastic Compute Cloud
(Amazon EC2), Amazon SimpleDB, and more.

Optional:
* APC (php-pecl-apcu):
      Allows service description opcode caching, request and response caching,
      and credentials caching
* Doctrine Cache (php-doctrine-cache):
      Adds support for caching of credentials and responses
* Monolog (php-Monolog):
      Adds support for logging HTTP requests and responses
* Symfony YAML (php-symfony-yaml):
      Eases the ability to write manifests for creating jobs in AWS
      Import/Export


%prep
%setup -qn %{github_name}-%{github_commit}

# Fix rpmlint issue:
#     W: spurious-executable-perm /usr/share/doc/php-aws-sdk/composer.json
chmod a-x composer.json


%build
# Empty build section, most likely nothing required.


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/AWSSDKforPHP
cp -pr src/* %{buildroot}%{_datadir}/php/
# Compat direcory structure with old PEAR pkg
ln -s ../Aws %{buildroot}%{_datadir}/php/AWSSDKforPHP/Aws


%check
# Tests skipped because "Guzzle\Tests\GuzzleTestCase" is not provided by the
# php-guzzle-Guzzle package


%post
# Unregister PEAR pkg (ignore errors if it was not registered)
if [ -x %{_bindir}/pear ]; then
    %{_bindir}/pear uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{!?_licensedir:%global license %%doc}
%license LICENSE.md
%doc NOTICE.md composer.json
%{_datadir}/php/Aws
%{_datadir}/php/AWSSDKforPHP


%changelog
* Fri Nov 21 2014 Remi Collet <remi@fedoraproject.org> - 2.7.6-1
- Update to 2.7.6

* Fri Nov 14 2014 Remi Collet <remi@fedoraproject.org> - 2.7.5-1
- Update to 2.7.5

* Fri Nov  7 2014 Remi Collet <remi@fedoraproject.org> - 2.7.3-1
- Update to 2.7.3

* Sat Oct 25 2014 Remi Collet <remi@fedoraproject.org> - 2.7.2-1
- Update to 2.7.2

* Mon Oct 20 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.7.1-1
- Updated to 2.7.1 (BZ #1151012)
- Doctrine Cache, Monolog, and Symfony YAML are now optional

* Tue Sep 23 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.6.16-1
- Updated to 2.6.16 (BZ #1142985)

* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> - 2.6.15-1
- Update to 2.6.15

* Sun Aug 17 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.6.15-2
- Obsolete php-channel-aws
- Compat direcory structure with old PEAR pkg

* Sat Aug 16 2014 Remi Collet <remi@fedoraproject.org> - 2.6.15-1
- update to 2.6.15
- sync with rawhide
- add link for compatibility with old pear package

* Fri Aug 15 2014 Shawn Iwinski <shawn.iwinski@gmail.com> - 2.6.15-1
- Updated to 2.6.15 (BZ #1126610)
- PEAR install changed to Composer-ish install

* Tue Aug 12 2014 Remi Collet <remi@fedoraproject.org> - 2.6.14-1
- Update to 2.6.14

* Fri Aug 01 2014 Remi Collet <remi@fedoraproject.org> - 2.6.13-1
- Update to 2.6.13

* Thu Jul 17 2014 Remi Collet <remi@fedoraproject.org> - 2.6.12-1
- Update to 2.6.12

* Fri Jul 11 2014 Remi Collet <remi@fedoraproject.org> - 2.6.11-1
- Update to 2.6.11

* Mon Jul 07 2014 Remi Collet <remi@fedoraproject.org> - 2.6.10-1
- Update to 2.6.10

* Fri Jun 27 2014 Remi Collet <remi@fedoraproject.org> - 2.6.9-1
- Update to 2.6.9

* Mon Jun 23 2014 Remi Collet <remi@fedoraproject.org> - 2.6.8-1
- Update to 2.6.8

* Fri May 30 2014 Remi Collet <remi@fedoraproject.org> - 2.6.6-1
- Update to 2.6.6

* Mon May 26 2014 Remi Collet <remi@fedoraproject.org> - 2.6.5-1
- Update to 2.6.5

* Thu May 22 2014 Remi Collet <remi@fedoraproject.org> - 2.6.4-1
- Update to 2.6.4

* Thu May 15 2014 Remi Collet <remi@fedoraproject.org> - 2.6.3-1
- Update to 2.6.3

* Wed May 07 2014 Remi Collet <remi@fedoraproject.org> - 2.6.2-1
- Update to 2.6.2

* Tue Apr 29 2014 Remi Collet <remi@fedoraproject.org> - 2.6.1-1
- Update to 2.6.1

* Wed Apr 23 2014 Remi Collet <remi@fedoraproject.org> - 2.6.0-1
- Update to 2.6.0

* Fri Mar 21 2014 Remi Collet <remi@fedoraproject.org> - 2.5.4-1
- Update to 2.5.4

* Fri Feb 28 2014 Remi Collet <remi@fedoraproject.org> - 2.5.3-1
- Update to 2.5.3

* Thu Jan 30 2014 Remi Collet <remi@fedoraproject.org> - 2.5.2-1
- Update to 2.5.2

* Fri Jan 10 2014 Remi Collet <remi@fedoraproject.org> - 2.5.1-1
- Update to 2.5.1

* Thu Jan  2 2014 Remi Collet <remi@fedoraproject.org> - 2.5.0-2
- backport rawhide change for remi rep

* Mon Dec 30 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-2
- add php-Monolog-dynamo dependency
- update naming on dependency php-symfony-yaml
- fix max version require on guzzle dependency

* Mon Dec 30 2013 Remi Collet <remi@fedoraproject.org> - 2.5.0-1
- backport 2.5.0 for remi repo

* Sun Dec 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.5.0-1
- update to latest upstrean version

* Mon Nov 18 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.10-1
- update to latest upstream version
- add php-symfony2-Yaml(version2) and php-Monolog
- remove dependency php-symfony2-YAML(version1)
- set version contraint for php-guzzle-Guzzle dependency

* Mon Sep 09 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.5-2
- add guzzle dependency.
- remove aws.phar file

* Thu Sep 05 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 2.4.5-1
- Update to 2.4.5

* Sat May 04 2013 Remi Collet <remi@fedoraproject.org> - 1.6.2-4
- backport 1.6.2 for remi repo

* Wed May 01 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-4
- Add dependencies
- Add license clarification
* Tue Apr 30 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-3
- Fix Source, remove empty folder _doc
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-2
- Fix License, Fix Description, move doc files
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-1
- initial package
