%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}

Name:		php-channel-swift
Version:	1.3
Release:	6%{?dist}
Summary:	Adds swift mailer project channel to PEAR

Group:		Development/Languages
License:	LGPLv3
URL:		http://www.swiftmailer.org/
Source0:	http://pear.swiftmailer.org/channel.xml
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)

BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2
Requires:	php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}

Provides:	php-channel(pear.swiftmailer.org)

%description
This package adds the swift mailer channel which allows
PEAR packages from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
%{__rm} -rf $RPM_BUILD_ROOT
%{__mkdir_p} $RPM_BUILD_ROOT%{pear_xmldir}
%{__install} -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml


%clean
%{__rm} -rf $RPM_BUILD_ROOT

%post
if [ $1 -eq  1 ] ; then
	%{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
	%{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null ||:
fi


%postun
if [ $1 -eq 0 ] ; then
	%{__pear} channel-delete pear.swiftmailer.org > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/*


%changelog
* Thu Feb 14 2013 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-6
- Rebuilt for https://fedoraproject.org/wiki/Fedora_19_Mass_Rebuild

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-5
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jan 14 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_17_Mass_Rebuild

* Wed Feb 09 2011 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.3-3
- Rebuilt for https://fedoraproject.org/wiki/Fedora_15_Mass_Rebuild

* Sun Jan 24 2010 Christof Damian <christof@damian.net> 1.3-2
- forgot to rename the channel xml in post

* Sun Jan 24 2010 Christof Damian <christof@damian.net> 1.3-1
- removed php-cli requirement, which is covered by php-pear requirement
- changed name of channel xml name
- using rest version as version now

* Tue Dec 1 2009 Christof Damian <christof@damian.net> - 1.0.0-1
- initial release
