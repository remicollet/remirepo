%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Net_SSH2

Name:           php-phpseclib-net-ssh2
Version:        0.3.5
Release:        3%{?dist}
Summary:        Pure-PHP implementation of SSHv2

Group:          Development/Libraries
License:        MIT
URL:            http://phpseclib.sourceforge.net/
Source0:        http://phpseclib.sourceforge.net/get/%{pear_name}-%{version}.tgz
# From Debian, thanks to David Prévot, adjust for rename of Blowfish
# library to avoid conflict with php-pear-Crypt-Blowfish
Patch0:         php-phpseclib-Net-SSH2-Crypt_Blowfish_conflict.patch

BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pear(phpseclib.sourceforge.net/Math_BigInteger) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Random) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Hash) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_TripleDES) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_RC4) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_AES) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Twofish) >= 0.3.0
Requires:       php-pear(phpseclib.sourceforge.net/Crypt_Blowfish) >= 0.3.0
Provides:       php-pear(phpseclib.sourceforge.net/Net_SSH2) = %{version}
BuildRequires:  php-channel(phpseclib.sourceforge.net)
Requires:       php-channel(phpseclib.sourceforge.net)
# phpcompatinfo, generated from 0.3.5
Requires:       php-pcre
Requires:       php-xml

%description
Pure-PHP implementation of SSHv2.

%prep
%setup -q -c
pushd %{pear_name}-%{version}
# Fix line endings of file we're about to patch
sed -e 's/\r//' -i SSH2.php
%patch0 -p2
# Drop md5sum of patched file from the PEAR manifest (or else it'll complain)
sed -e '/SSH2.php/s/md5sum="[^"]*"//' \
    ../package.xml >%{name}.xml


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        phpseclib.sourceforge.net/%{pear_name} >/dev/null || :
fi


%files
%{pear_xmldir}/%{name}.xml
%{pear_phpdir}/Net


%changelog
* Thu Jan 16 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-3
- fix up the patch for crypt_blowfish rename per review

* Sat Jan  4 2014 Adam Williamson <awilliam@redhat.com> - 0.3.5-2
- various review style cleanups

* Tue Dec 31 2013 Adam Williamson <awilliam@redhat.com> - 0.3.5-1
- initial package (generated with pear make-rpm-spec)
