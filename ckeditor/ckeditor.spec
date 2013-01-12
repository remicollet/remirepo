Name:		ckeditor
Version:	3.6.4
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

%description
CKEditor is a text editor to be used inside web pages. It's a WYSIWYG editor,
which means that the text being edited on it looks as similar as possible to
the results users have when publishing it. It brings to the web common editing
features found on desktop editing applications like Microsoft Word and
OpenOffice.


%prep
%setup -q -n %{name}


%build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/%{name}
cp -rp * $RPM_BUILD_ROOT%{_datadir}/%{name}
chmod +x $RPM_BUILD_ROOT%{_datadir}/%{name}/_samples/adobeair/run.sh
mkdir -p $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d
install -p -m 0644 %{SOURCE1} $RPM_BUILD_ROOT%{_sysconfdir}/httpd/conf.d

%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc CHANGES.html INSTALL.html LICENSE.html
%config(noreplace) %{_sysconfdir}/httpd/conf.d/%{name}.conf
%{_datadir}/%{name}


%changelog
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
