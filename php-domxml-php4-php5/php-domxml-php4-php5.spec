%global libname domxml-php4-php5

Name:           php-%{libname}
Version:        1.21.1
Release:        1%{?dist}
Summary:        XML transition from PHP4 domxml to PHP5 dom module
Summary(fr):    Transition du XML de PHP4 domxml à PHP5 dom

Group:          Development/Libraries
License:        LGPLv3
URL:            http://alexandre.alapetite.fr/doc-alex/domxml-php4-php5
# wget -N http://alexandre.alapetite.fr/doc-alex/domxml-php4-php5/domxml-php4-to-php5.php.txt -O domxml-php4-to-php5.php
# grep Version domxml-php4-to-php5.php
# tar czf domxml-php4-php5-1.21.1.tar.gz domxml-php4-to-php5.php
Source0:        %{libname}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch

Requires:       php-xml >= 5.1

%description
XML transition from PHP4 domxml to PHP5 dom module.

%description -l fr
Transition du XML de PHP4 domxml à PHP5 dom.


%prep
%setup -qc

sed -i -e 's/\r//' *.php


%build
# nothing to build


%install
rm -rf $RPM_BUILD_ROOT
%{__install} -d $RPM_BUILD_ROOT%{_datadir}/php/%{libname}
%{__install} -pm 0644 *.php $RPM_BUILD_ROOT%{_datadir}/php/%{libname}


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%{_datadir}/php/%{libname}


%changelog
* Sun Mar 14 2010 Remi Collet <Fedora@FamilleCollet.com> - 1.21.1-1
- rename to php-domxml-php4-php5

* Mon Dec 21 2009 Eric "Sparks" Christensen <sparks@fedoraproject.org> - 1.21.1-1
- Initial package.
