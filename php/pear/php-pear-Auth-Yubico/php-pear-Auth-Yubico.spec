%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name	Auth_Yubico
%global channel		__uri

Name:		php-pear-Auth-Yubico
Version:	2.4
Release:	1%{?dist}
Summary:	Authentication class for verifying Yubico OTP tokens

Group:		Development/Libraries
License:	BSD
URL:		http://php-yubico.googlecode.com/
Source0:	http://php-yubico.googlecode.com/files/Auth_Yubico-%{version}.tgz
Patch1:		php-pear-Auth-Yubico-2.3.channel.patch
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildArch:	noarch
BuildRequires:	php-pear >= 1:1.4.9-1.2

Requires:	php-pear(PEAR) >= 1.4.0
Requires(post):		%{__pear}
Requires(postun):	%{__pear}

Provides:	php-pear(%{channel}/%{pear_name}) = %{version}


%description
  The Yubico authentication PHP class provides an easy way to integrate the
Yubikey into your existing PHP-based user authentication infrastructure.


#-------------------------------------------------------------------------------
%prep
#-------------------------------------------------------------------------------

%setup -q -n Auth_Yubico-%{version}
%patch1 -p 1

#	Fix end of line encoding.

for file in Modhex_Calculator.php Modhex.php
do	sed -i -e 's/\r$//' "example/${file}"
done


#-------------------------------------------------------------------------------
%build
#-------------------------------------------------------------------------------

#	Nothing to do.


#-------------------------------------------------------------------------------
%install
#-------------------------------------------------------------------------------

rm -rf "${RPM_BUILD_ROOT}"

%{__pear} install --nodeps				\
				--packagingroot "${RPM_BUILD_ROOT}"	\
				package.xml

#	Clean up unnecessary files.

rm -rf "${RPM_BUILD_ROOT}%{pear_phpdir}/".??*

#	Install XML package description.

mkdir -p "${RPM_BUILD_ROOT}%{pear_xmldir}"
install -p -m 644 package.xml "${RPM_BUILD_ROOT}%{pear_xmldir}/%{name}.xml"


#-------------------------------------------------------------------------------
%clean
#-------------------------------------------------------------------------------

rm -rf "${RPM_BUILD_ROOT}"


#-------------------------------------------------------------------------------
%post
#-------------------------------------------------------------------------------

%{__pear} install --nodeps --soft --force --register-only		\
	"%{pear_xmldir}/%{name}.xml" > /dev/null || :


#-------------------------------------------------------------------------------
%postun
#-------------------------------------------------------------------------------

if [ "${1}" -eq "0" ]
then	%{__pear} uninstall --nodeps --ignore-errors --register-only	\
		"%{channel}/%{pear_name}" > /dev/null || :
fi


#-------------------------------------------------------------------------------
%files
#-------------------------------------------------------------------------------

%defattr(-, root, root, -)
%doc NEWS README COPYING
%doc example demo.php
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Auth


#-------------------------------------------------------------------------------
%changelog
#-------------------------------------------------------------------------------
* Sat Mar 31 2012 Remi Collet <RPMS@FamilleCollet.com> - 2.4.1
- upstream 2.4, rebuild for remi repository

* Wed Mar 28 2012 Patrick Monnerat <pm@datasphere.ch> 2.4-1
- New upstream release: dvorak keyboard support.

* Thu Feb 24 2011 Remi Collet <RPMS@FamilleCollet.com> - 2.3-2
- rebuild for remi repo

* Mon Feb 21 2011 Patrick Monnerat <pm@datasphere.ch> 2.3-2
- Some spec file adjustments:
  https://bugzilla.redhat.com/show_bug.cgi?id=675122#c1

* Thu Feb  3 2011 Patrick Monnerat <pm@datasphere.ch> 2.3-1
- Initial rpm packaging.
- Patch "channel" to change package channel in XML description file.
