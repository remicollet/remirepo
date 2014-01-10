%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-aws-//' -e 's/-/_/g')
%global channelname pear.amazonwebservices.com

Name:		php-aws-sdk
Version:	2.5.1
Release:	1%{?dist}
Summary:	Amazon Web Services framework for PHP
Group:		Development/Libraries

License:	ASL 2.0
URL:		http://aws.amazon.com/sdkforphp/
Source0:	http://pear.amazonwebservices.com/get/sdk-%{version}.tgz

BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root
BuildArch:	noarch
BuildRequires:	php-pear(PEAR)
BuildRequires:	php-channel(%{channelname})

Requires(post):		%{__pear}
Requires(postun):	%{__pear}

Requires:	php(language) >= 5.2
Requires:	php-pear(PEAR)
Requires:	php-channel(%{channelname})
Requires:	php-pdo
Requires:	php-reflection
Requires:	php-spl
Requires:	php-simplexml
Requires:	php-ctype
Requires:	php-curl
Requires:	php-date
Requires:	php-dom
Requires:	php-hash
Requires:	php-json
Requires:	php-libxml
Requires:	php-mbstring
Requires:	php-openssl
Requires:	php-pcre
Requires:	php-session
Requires:	php-sqlite3
Requires:	php-Monolog
Requires:	php-Monolog-dynamo
Requires:	php-symfony-yaml
Requires:	php-guzzle-Guzzle >= 3.7.0
Requires:	php-guzzle-Guzzle < 3.9.0
Provides:	php-pear(%{pear_name}) = %{version}
Provides:	php-pear(%{channelname}/%{pear_name}) = %{version}

%description
Amazon Web Services SDK for PHP enables developers to build solutions for
Amazon Simple Storage Service (Amazon S3), Amazon Elastic Compute Cloud
(Amazon EC2), Amazon SimpleDB, and more.


%prep
%setup -q -c

# fix doc roles
sed -e '/aws.phar/d' \
    package.xml >%{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
	%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/AWSSDKforPHP/


%changelog
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
