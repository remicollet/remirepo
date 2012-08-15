%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name XML_RPC

Name:           php-pear-XML-RPC
Version:        1.5.5
Release:        2%{?dist}
Summary:        PHP implementation of the XML-RPC protocol

Group:          Development/Libraries
# PHP License version 3.0.1
# http://pear.php.net/bugs/19368 request for License file.
License:        PHP
URL:            http://pear.php.net/package/XML_RPC
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.9.4-9
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
# previous version have XML_RPC bundled
Requires:       php-pear >= 1:1.9.4-9
Requires:       php-pear(PEAR)
# extensions detected by phpci
Requires:       php-date, php-mbstring, php-pcre
# also requires php-xml, which is provided by php-common, not php-xml

Provides:       php-pear(%{pear_name}) = %{version}

%description
A PEAR-ified version of Useful Inc's XML-RPC for PHP.

It has support for HTTP/HTTPS transport, proxies and authentication.


%prep
%setup -q -c
cd %{pear_name}-%{version}
# package.xml is V1, package2.xml is V2
mv ../package2.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf %{buildroot}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_phpdir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%clean
rm -rf %{buildroot}


# use posttrans to register after removal of php-pear bundled version
# and of /usr/share/pear/.registry/xml_rpc.reg
%posttrans
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.php.net/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/XML/RPC
%{pear_phpdir}/XML/RPC.php
# this are not real unit tests, can't be run in rpmbuild
%{pear_testdir}/%{pear_name}


%changelog
* Wed Aug 15 2012 Remi Collet <remi@fedoraproject.org> - 1.5.5-2
- rebuilt for new pear_testdir
- fix typo in comment
- add BR php-pear(PEAR)

* Mon Aug 13 2012 Remi Collet <remi@fedoraproject.org> - 1.5.5-1
- Version 1.5.5 (stable), API 1.5.0 (stable)
- Initial RPM

