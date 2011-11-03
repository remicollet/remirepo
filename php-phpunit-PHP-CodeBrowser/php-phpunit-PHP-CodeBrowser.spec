%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name PHP_CodeBrowser
%global channel pear.phpunit.de

Name:           php-phpunit-PHP-CodeBrowser
Version:        1.0.0
Release:        1%{?dist}
Summary:        PHP_CodeBrowser for integration in Hudson and CruiseControl

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/mayflowergmbh/PHP_CodeBrowser
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.8.1
BuildRequires:  php-channel(%{channel})
Requires:       php-common >= 5.2.6
Requires:       php-channel(%{channel})
Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(Console_CommandLine) >= 1.1.3
Requires:       php-pear(pear.phpunit.de/File_Iterator) >= 1.2.1
Requires:       php-pear(Log) >= 1.12.1
Requires:       php-pear(pear.phpunit.de/PHPUnit) >= 3.4.0
Requires:       php-pear(PHP_CodeSniffer) >= 1.2.0
Requires:       php-pear(PhpDocumentor) >= 1.4.3

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
PHP_CodeBrowser generates a HTML view for code browsing with highlighted and 
colored errors, parsed from XML reports generated from code-sniffer or 
phpunit.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}

# Create a "localized" php.ini to avoid build warning
cp /etc/php.ini .
echo "date.timezone=UTC" >>php.ini

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT docdir
PHPRC=./php.ini %{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%{__rm} -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*


# Move documentation
mkdir -p docdir
mv -v $RPM_BUILD_ROOT%{pear_docdir}/%{pear_name}/* docdir

# Install XML package description
%{__mkdir} -p $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
%{__rm} -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{channel}/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_name}-%{version}/docdir/*
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/%{pear_name}
%{pear_datadir}/%{pear_name}
%{_bindir}/phpcb


%changelog
* Mon Dec 20 2010 Remi Collet <RPMS@FamilleCollet.com> - 1.0.0-1
- rebuild for remi repository

* Tue Dec 14 2010 Christof Damian <christof@damian.net> - 1.0.0-1
- upstream 1.0.0 (stable)

* Wed Nov 10 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.9.1-3
- rebuild for remi repository

* Mon Nov  8 2010 Christof Damian <christof@damian.net> - 0.9.1-3
- more requires as suggested by reviewer

* Sat Nov  6 2010 Christof Damian <christof@damian.net> - 0.9.1-2
- changed requires for main pear packages
- moved docs

* Mon Nov  1 2010 Christof Damian <christof@damian.net> - 0.9.1-1
- initial spec file

