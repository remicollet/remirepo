%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Mockery
%global channel pear.survivethedeepend.com

Name:           php-deepend-Mockery
Version:        0.7.2
Release:        1%{?dist}
Summary:        Mockery is a simple but flexible PHP mock object framework

Group:          Development/Libraries
License:        BSD
URL:            http://github.com/padraic/mockery
Source0:        http://pear.survivethedeepend.com/get/%{pear_name}-%{version}.tgz
Source1:        http://github.com/padraic/mockery/blob/master/LICENSE
Source2:        http://github.com/padraic/mockery/blob/master/README.markdown

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.9-1.2
BuildRequires:  php-channel(%{channel})
Requires:       php-channel(%{channel})
Requires:       php-common >= 5.3.2
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
Mockery is a simple but flexible PHP mock object framework for use in unit 
testing. It is inspired by Ruby's flexmock and Java's Mockito, borrowing 
elements from both of their APIs.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
%{__mv} package2.xml %{pear_name}-%{version}/%{name}.xml
cd %{pear_name}-%{version}

%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__rm} -rf $RPM_BUILD_ROOT docdir
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%{__rm} -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

# Install XML package description
%{__mkdir} -p $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}

mkdir docdir
%{__cp} %{SOURCE1} %{SOURCE2} docdir


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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Mockery.php
%{pear_phpdir}/Mockery
%doc %{pear_name}-%{version}/docdir/*

%changelog
* Sun Mar 04 2012 Remi Collet <RPMS@FamilleCollet.com> - 0.7.2-1
- upstream 0.7.2, rebuild for remi repository

* Sun Mar  4 2012 Christof Damian <christof@damian.net> - 0.7.2-1
- upstream 0.7.2

* Wed Jul 27 2010 Remi Collet <RPMS@FamilleCollet.com> - 0.6.3-2
- rebuild for remi repository

* Tue Jul 27 2010 Christof Damian <christof@damian.net> - 0.6.3-2
- add license and readme file from github

* Fri May 28 2010 Christof Damian <christof@damian.net> - 0.6.0-1
- initial packaging


