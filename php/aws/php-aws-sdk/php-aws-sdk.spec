%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name %(echo %{name} | sed -e 's/^php-aws-//' -e 's/-/_/g')
%global channelname pear.amazonwebservices.com

Name:		php-aws-sdk
Version:	1.6.2
Release:	4%{?dist}
Summary:	Amazon Web Services framework for PHP

#The entire source code is ASL 2.0 except lib/cachecore/, lib/requestcore/, lib/yaml/ which are BSD and lib/dom/ which is MIT
License:	ASL 2.0 and BSD and MIT
URL:		http://aws.amazon.com/sdkforphp/
Source0:	http://pear.amazonwebservices.com/get/sdk-%{version}.tgz

BuildArch:	noarch
BuildRequires:	php-pear(PEAR)
BuildRequires:	php-channel(%{channelname})

Requires(post):		%{__pear}
Requires(postun):	%{__pear}

Requires:	php-common >= 5.2
Requires:	php-pear(PEAR)
Requires:	php-channel(%{channelname})
Requires:	php-xml
Requires:	php-mbstring
Requires:	php-pdo
Requires:	php-pecl-apc
Requires:	php-pecl-memcache
Requires:	php-pecl-memcached
Requires:	php-xcache

Provides:	php-pear(%{pear_name}) = %{version}
Provides:	php-pear(%{channelname}/%{pear_name}) = %{version}

%description
Amazon Web Services SDK for PHP enables developers to build solutions for 
Amazon Simple Storage Service (Amazon S3), Amazon Elastic Compute Cloud 
(Amazon EC2), Amazon SimpleDB, and more.


%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%if 0%{?rhel}
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*
%else
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*
%endif

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

 
mv $RPM_BUILD_ROOT%{pear_phpdir}/AWSSDKforPHP/_samples $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/
mv $RPM_BUILD_ROOT%{pear_phpdir}/AWSSDKforPHP/_compatibility_test $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/
mv $RPM_BUILD_ROOT%{pear_phpdir}/AWSSDKforPHP/_docs/* $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/_docs/
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/AWSSDKforPHP/_docs/

%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
	%{pear_name} >/dev/null || :
fi


%files
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/AWSSDKforPHP/


%changelog
* Wed May 01 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-4
- Add dependencies
- Add license clarification
* Tue Apr 30 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-3
- Fix Source, remove empty folder _doc 
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-2
- Fix License, Fix Description, move doc files
* Mon Apr 29 2013 Joseph Marrero <jmarrero@fedoraproject.org> - 1.6.2-1
- initial package
