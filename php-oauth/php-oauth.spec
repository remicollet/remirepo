%define realname oauth
%define svnrevision svn1262

Name:           php-oauth
Version:        1.0
Release:        0.9.%{svnrevision}%{?dist}
Summary:        PHP Authentication library for desktop to web applications

Group:          Development/Libraries
License:        MIT
URL:            http://code.google.com/p/oauth/

# Package tarball not present. To compress:
# svn export -r 1262 http://oauth.googlecode.com/svn/code/php/ oauth
# tar -czf php-oauth-1.0.tar.gz oauth
Source0:        %{name}-%{version}.tar.gz
BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:      noarch
Requires:       php

%description
An open protocol to allow API authentication in a simple and standard
method from desktop and web applications.

%prep
%setup -qn %{realname}
mv OAuth_TestServer.php example

%build
# Empty build


%install
rm -rf $RPM_BUILD_ROOT
mkdir -p $RPM_BUILD_ROOT%{_datadir}/php/%{realname}
install -p -m 644 OAuth.php $RPM_BUILD_ROOT%{_datadir}/php/%{realname}/


%clean
rm -rf $RPM_BUILD_ROOT


%files
%defattr(-,root,root,-)
%doc doc example
%{_datadir}/php/%{realname}


%changelog
* Fri Aug 19 2011 F. Kooman <fkooman@tuxed.net> - 1.0-0.9.svn1262
- update to svn1262
- move test server class to examples

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.8.svn592
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jul 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.7.svn592
- Rebuilt for https://fedoraproject.org/wiki/Fedora_12_Mass_Rebuild

* Thu Feb 26 2009 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-0.6.svn592
- Rebuilt for https://fedoraproject.org/wiki/Fedora_11_Mass_Rebuild

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.0-0.5.svn592
 - Changed release field

* Sat Aug 23 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.0-4.svn592
 - Updated tarball export info and updated tarball (Peter Lemenkov)

* Sun Jul 13 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.0-3.svn592
 - Corrected srpm release, correct svn link

* Sat Jul 12 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.0-2
 - Corrected spec and package name

* Fri Jul 11 2008 Rakesh Pandit <rakesh@fedoraproject.org> 1.0-1
 - Initial packages
