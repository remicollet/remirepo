%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_channel pear.pirum-project.org

Name:             php-channel-pirum
Version:          1.0
Release:          1%{?dist}
Summary:          Adds %{pear_channel} channel to PEAR

Group:            Development/Libraries
License:          Public Domain
URL:              http://%{pear_channel}
Source0:          http://%{pear_channel}/channel.xml

BuildRoot:        %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:        noarch
BuildRequires:    php-pear(PEAR)

Requires:         php-pear(PEAR)
Requires(post):   %{__pear}
Requires(postun): %{__pear}

Provides:         php-channel(%{pear_channel}) = %{version}

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
* Fri Nov  9 2012 Remi Collet <rpms@famillecollet.com> - 1.0-1
- backport for remi repo

* Sun Jun 17 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 1.0-1
- Initial package
