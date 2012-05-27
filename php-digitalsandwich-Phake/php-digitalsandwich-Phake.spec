%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Phake
%global channel pear.digitalsandwich.com

Name:           php-digitalsandwich-Phake
Version:        1.0.2
Release:        1%{?dist}
Summary:        Phake is a PHP mocking framework that is based on Mockito

Group:          Development/Libraries
License:        BSD
URL:            http://digitalsandwich.com/
Source0:        http://pear.digitalsandwich.com/get/%{pear_name}-%{version}.tgz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
BuildRequires:  php-pear >= 1:1.4.0
BuildRequires:  php-channel(%{channel})
Requires:       php-channel(%{channel})
Requires:       php-common >= 5.2.3
Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:       php-pear(%{channel}/%{pear_name}) = %{version}


%description
Phake is a framework for PHP that aims to provide mock objects, test doubles 
and method stubs.

Phake was inspired by a lack of flexibility and ease of use in the current 
mocking frameworks combined with a recent experience with Mockito for Java.

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
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
%{__rm} -rf $RPM_BUILD_ROOT%{pear_phpdir}/.??*

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
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Phake
%{pear_phpdir}/Phake.php

%changelog
* Wed May  2 2012 Christof Damian <christof@damian.net> - 1.0.2-1
- initial release (1.0.2)


