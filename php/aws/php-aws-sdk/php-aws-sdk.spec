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
%global github_version   2.6.16
%global github_commit    36434f2cd96ea78844478d897fb568a1866bce5a

%global composer_vendor  aws
%global composer_project aws-sdk-php

%global pear_channel     pear.amazonwebservices.com
%global pear_name        sdk

# "php": ">=5.3.3"
%global php_min_ver      5.3.3
# "guzzle/guzzle": ">=3.7.0,<=3.9.9"
%global guzzle_min_ver   3.7.0
%global guzzle_max_ver   3.9.9

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
Requires:  php-composer(doctrine/cache)
Requires:  php-composer(monolog/monolog)
Requires:  php-openssl
Requires:  php-symfony-yaml
# phpcompatinfo (computed from version 2.6.15)
Requires:  php-curl
Requires:  php-date
Requires:  php-hash
Requires:  php-json
Requires:  php-openssl
Requires:  php-pcre
Requires:  php-reflection
Requires:  php-session
Requires:  php-simplexml
Requires:  php-spl

# Composer
Provides:  php-composer(%{composer_vendor}/%{composer_project}) = %{version}
# PEAR
Provides:  php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
Amazon Web Services SDK for PHP enables developers to build solutions for
Amazon Simple Storage Service (Amazon S3), Amazon Elastic Compute Cloud
(Amazon EC2), Amazon SimpleDB, and more.


%prep
%setup -qn %{github_name}-%{github_commit}

# Fix rpmlint issues:
#     W: spurious-executable-perm /usr/share/doc/php-aws-sdk/composer.json
#     E: script-without-shebang /usr/share/php/Aws/DynamoDb/Model/BatchRequest/WriteRequestBatchTransfer.php
chmod a-x composer.json src/Aws/DynamoDb/Model/BatchRequest/WriteRequestBatchTransfer.php


%build
# Empty build section, most likely nothing required.


%install
mkdir -pm 0755 %{buildroot}%{_datadir}/php/AWSSDKforPHP/
cp -pr src/* %{buildroot}%{_datadir}/php/
# compat with old pear package
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
%doc CHANGELOG.md README.md UPGRADING.md composer.json
%{_datadir}/php/Aws
%{_datadir}/php/AWSSDKforPHP


%changelog
* Fri Sep 12 2014 Remi Collet <remi@fedoraproject.org> - 2.6.15-1
- Update to 2.6.15

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
