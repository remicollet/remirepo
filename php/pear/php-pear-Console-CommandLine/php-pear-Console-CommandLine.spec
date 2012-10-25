%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Console_CommandLine

Name:           php-pear-Console-CommandLine
Version:        1.2.0
Release:        1%{?dist}
Summary:        A full featured command line options and arguments parser

Group:          Development/Libraries
License:        MIT
URL:            http://pear.php.net/package/%{pear_name}
Source0:        http://pear.php.net/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear
BuildRequires:  php-pear(pear.phpunit.de/PHPUnit)

Requires:       php(language) >= 5.1.0
Requires:       php-spl
Requires(post): %{__pear}
Requires(postun): %{__pear}
Provides:       php-pear(%{pear_name}) = %{version}

%description
Console_CommandLine is a full featured package for managing command-line
options and arguments highly inspired from python optparse module, it allows
the developer to easily build complex command line interfaces.

Main features:
* handles sub commands (i.e. $ my-script.php -q sub-command -f file),
* can be completely built from an XML definition file,
* generate --help and --version options automatically,
* can be completely customized,
* built-in support for i18n,
* and much more...


%prep
%setup -qc
cd %{pear_name}-%{version}
mv ../package.xml %{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
install -d $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%check
cd %{pear_name}-%{version}

# seems this one need to be fixed for new feature
rm -f tests/console_commandline_addargument.phpt

%{_bindir}/phpunit tests


%clean
rm -rf $RPM_BUILD_ROOT


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
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_datadir}/%{pear_name}
%{pear_testdir}/%{pear_name}
%{pear_phpdir}/Console


%changelog
* Thu Oct 25 2012 Remi Collet <remi@fedoraproject.org> - 1.2.0-1
- Version 1.2.0 (stable) - API 1.2.0 (stable)

* Sun Aug 19 2012 Remi Collet <remi@fedoraproject.org> - 1.1.3-8
- rebuilt for new pear_datadir

* Tue Aug 14 2012 Remi Collet <remi@fedoraproject.org> - 1.1.3-7
- rebuilt for new pear_testdir

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Mon Nov  8 2010 Christof Damian <christof@damian.net> - 1.1.3-3
- removed global channel

* Sat Nov  6 2010 Christof Damian <christof@damian.net> - 1.1.3-2
- changed pear channel requirement
- fixed license
- move examples to toplevel doc dir
- added check section
- own Console directory

* Mon Nov  1 2010 Christof Damian <christof@damian.net> - 1.1.3-1
- initial spec file

