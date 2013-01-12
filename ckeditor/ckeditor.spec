Name:		ckeditor
Version:	3.6.6
Release:	1%{?dist}
Summary:	WYSIWYG text editor to be used inside web pages

Group:		Applications/Internet
License:	GPLv2+ or LGPLv2+ or MPLv1.1+
URL:		http://ckeditor.com/
Source0:	http://download.cksource.com/CKEditor/CKEditor/CKEditor%20%{version}/ckeditor_%{version}.tar.gz
Source1:	%{name}.conf

BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch

Requires:	httpd
Requires:	php-common


%description
CKEditor is a text editor to be used inside web pages. It's a WYSIWYG editor,
which means that the text being edited on it looks as similar as possible to
the results users have when publishing it. It brings to the web common editing
features found on desktop editing applications like Microsoft Word and
OpenOffice.


%prep
%setup -q -c

# uneeded files
rm  -f %{name}/.htaccess
rm  -f %{name}/INSTALL.html
rm -rf %{name}/_source

# documentation
mkdir doc
mv %{name}/{CHANGES,LICENSE}.html doc/
mv %{name}/_samples doc/

# PHP Library
mkdir php
mv %{name}/*php php/


%build
# Nothing to build


%install
rm -rf %{buildroot}

# PHP
mkdir -p %{buildroot}%{_datadir}/php/%{name}
cp -p php/ckeditor_php5.php %{buildroot}%{_datadir}/php/%{name}/ckeditor.php

# Javascript
cp -rp %{name} %{buildroot}%{_datadir}/%{name}

# Apache
mkdir -p %{buildroot}%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE1} %{buildroot}%{_sysconfdir}/httpd/conf.d


%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc doc/*
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}
%{_datadir}/php/%{name}


%changelog
* Sat Jan 13 2013 Remi Collet <RPMS@FamilleCollet.com> - 3.6.6-1
- backport for remi repo
- update to 3.6.6
- move _samples in doc
- don't package _source
- move php library to /usr/share/php

* Fri Sep 14 2012 Orion Poplawski <orion@cora.nwra.com> 3.6.4-1
- Update to 3.6.4

* Wed Jul 18 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 3.6.3-2
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Fri Apr 27 2012 Orion Poplawski <orion@cora.nwra.com> 3.6.3-1
- Update to 3.6.3

* Mon Jan 23 2012 Orion Poplawski <orion@cora.nwra.com> 3.6.2-2
- Make %%doc line explicit

* Tue Oct 25 2011 Orion Poplawski <orion@cora.nwra.com> 3.6.2-1
- Update to 3.6.2

* Wed Aug 3 2011 Orion Poplawski <orion@cora.nwra.com> 3.6.1-1
- Update to 3.6.1

* Wed Oct 6 2010 Orion Poplawski <orion@cora.nwra.com> 3.4.1-1
- Initial package
