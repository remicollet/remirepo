%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}

%global pear_channel pear.doctrine-project.org
%global pear_name    %(echo %{name} | sed -e 's/^php-doctrine-//' -e 's/-/_/g')

Name:             php-doctrine-DoctrineCommon
Version:          2.3.0
Release:          2%{?dist}
Summary:          Doctrine Common PHP Extensions

Group:            Development/Libraries
# License clarification from upstream since both MIT and LGPL are found:
# https://groups.google.com/d/topic/doctrine-dev/BNd84oKdOP0/discussion
License:          MIT
URL:              http://www.doctrine-project.org/projects/common.html
Source0:          http://%{pear_channel}/get/%{pear_name}-%{version}.tgz

BuildArch:        noarch
BuildRequires:    php-pear(PEAR)
BuildRequires:    php-channel(%{pear_channel})

Requires:         php-common >= 5.3.2
Requires:         php-pear(PEAR)
Requires:         php-channel(%{pear_channel})
Requires(post):   %{__pear}
Requires(postun): %{__pear}
# phpci requires
Requires:         php-ctype
Requires:         php-date
Requires:         php-json
Requires:         php-pcre
Requires:         php-reflection
Requires:         php-spl
Requires:         php-tokenizer

Provides:         php-pear(%{pear_channel}/%{pear_name}) = %{version}

%description
The Doctrine Common project is a library that provides extensions to core
PHP functionality.

Optional dependencies:
* APC (for Doctrine\Common\Cache\ApcCache)
* memcache (for Doctrine\Common\Cache\MemcacheCache)
* memcached (for Doctrine\Common\Cache\MemcachedCache)
* XCache (for Doctrine\Common\Cache\XcacheCache)


%prep
%setup -q -c

# Fix package.xml for LICENSE file to have role="doc" instead of role="data"
# *** http://www.doctrine-project.org/jira/browse/DCOM-102
sed '/LICENSE/s/role="data"/role="doc"/' \
    -i package.xml

# package.xml is version 2.0
mv package.xml %{pear_name}-%{version}/%{name}.xml


%build
# Empty build section, nothing required


%install
cd %{pear_name}-%{version}
%{__pear} install --nodeps --packagingroot %{buildroot} %{name}.xml

# Clean up unnecessary files
rm -rf %{buildroot}%{pear_metadir}/.??*

# Install XML package description
mkdir -p %{buildroot}%{pear_xmldir}
install -pm 644 %{name}.xml %{buildroot}%{pear_xmldir}


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :


%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        %{pear_channel}/%{pear_name} >/dev/null || :
fi


%files
%doc %{pear_docdir}/%{pear_name}
%{pear_xmldir}/%{name}.xml
%dir %{pear_phpdir}/Doctrine
     %{pear_phpdir}/Doctrine/Common


%changelog
* Tue Dec 18 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.0-2
- Updated description

* Tue Nov 27 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.3.0-1
- Updated to upstream version 2.3.0
- Updated license from LGPLv2 to MIT
- Added "%%global pear_metadir" and usage in %%install
- Changed RPM_BUILD_ROOT to %%{buildroot}

* Wed Jul 4 2012 Shawn Iwinski <shawn.iwinski@gmail.com> 2.2.2-1
- Initial package
