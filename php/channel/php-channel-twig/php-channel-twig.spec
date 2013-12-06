%{?scl:         %scl_package        php-channel-twig}
%{!?__pear:     %global __pear      %{_bindir}/pear}
%global pear_channel pear.twig-project.org

Name:             %{?scl_prefix}php-channel-twig
Version:          1.3
Release:          1%{?dist}
Summary:          Adds %{pear_channel} channel to PEAR

Group:            Development/Libraries
License:          Public Domain
URL:              http://%{pear_channel}
Source0:          http://%{pear_channel}/channel.xml

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    %{?scl_prefix}php-pear(PEAR)

Requires:         %{?scl_prefix}php-pear(PEAR)
Requires(post):   %{__pear}
Requires(postun): %{__pear}

Provides:         %{?scl_prefix}php-channel(%{pear_channel})

%description
This package adds the %{pear_channel} channel which allows PEAR packages
from this channel to be installed.


%prep
%setup -q -c -T


%build
# Empty build section, nothing to build


%install
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{SOURCE0} $RPM_BUILD_ROOT%{pear_xmldir}/%{name}.xml


%post
if [ $1 -eq  1 ] ; then
   %{__pear} channel-add %{pear_xmldir}/%{name}.xml > /dev/null || :
else
   %{__pear} channel-update %{pear_xmldir}/%{name}.xml > /dev/null || :
fi


%postun
if [ $1 -eq 0 ] ; then
   %{__pear} channel-delete %{pear_channel} > /dev/null || :
fi


%files
%defattr(-,root,root,-)
%{pear_xmldir}/%{name}.xml


%changelog
* Fri Dec  6 2013 Remi Collet <rcollet@redhat.com> 1.3-1
- adapt for SCL

* Wed Nov 14 2012 Remi Collet <RPMS@FamilleCollet.com> 1.3-1
- backport for remi repository

* Tue Nov 13 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.3-1
- Updated version to match channel REST version
- Removed version from virtual provide

* Fri Jul 20 2012 Fedora Release Engineering <rel-eng@lists.fedoraproject.org> - 1.0-4
- Rebuilt for https://fedoraproject.org/wiki/Fedora_18_Mass_Rebuild

* Sat Jun 09 2012 Remi Collet <RPMS@FamilleCollet.com> 1.0-3
- rebuild for remi repository

* Sat Jun  9 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-3
- Changed license from BSD to Public Domain
- Removed "BuildRequires: php-pear >= 1:1.4.9-1.2"
- Removed cleaning buildroot from %%install section
- Removed %%clean section

* Sun May 20 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-2
- %%global instead of %%define
- Removed BuildRoot
- Removed %%defattr from %%files section
- Minor syntax update in %%post section

* Fri Apr 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1
- Initial package
