%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name     PHP_TokenStream
%global channel       pear.phpunit.de

Name:           php-phpunit-PHP-TokenStream
Version:        1.1.3
Release:        1%{?dist}
Summary:        Wrapper around PHP tokenizer extension

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/sebastianbergmann/php-token-stream
Source0:        http://pear.phpunit.de/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.9.4
BuildRequires:  php-channel(%{channel})
Requires:       php-channel(%{channel})
Requires:       php-common >= 5.2.7
Requires:       php-tokenizer
Requires:       php-pear(components.ez.no/ConsoleTools) >= 1.6 
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
Wrapper around PHP tokenizer extension.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
rm -rf $RPM_BUILD_ROOT
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


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
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/PHP

%changelog
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

