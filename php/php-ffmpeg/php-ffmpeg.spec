%global ext_name   ffmpeg
%global svn        678

Name:           php-ffmpeg
Version:        0.7.0
%if 0%{?svn}
Release:        0.1.svn%{svn}%{?dist}
%else
Release:        1%{?dist}
%endif
Summary:        Extension to manipulate movie in PHP

Group:          Development/Languages
License:        GPLv2
URL:            http://ffmpeg-php.sourceforge.net/
%if 0%{?svn}
# svn export -r 678 https://ffmpeg-php.svn.sourceforge.net/svnroot/ffmpeg-php/trunk/ffmpeg-php ffmpeg-php-svn678
# tar cjf ffmpeg-php-svn678.tbz2 ffmpeg-php-svn678
Source0:        ffmpeg-php-svn%{svn}.tbz2
%else
Source0:        http://downloads.sourceforge.net/%{name}/ffmpeg-php-%{version}.tbz2
%endif

# Fix include path
Patch0:         php-ffmpeg-incl.patch
# Fix PHP 5.4 build
Patch1:         php-ffmpeg-php54.patch


BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildRequires:  ffmpeg-devel >= 0.10, php-devel, php-gd
Obsoletes:      ffmpeg-php < %{version}
Provides:       ffmpeg-php = %{version}-%{release}

Requires:       php-gd%{?_isa}
Requires:       php(zend-abi) = %{php_zend_api}
Requires:       php(api) = %{php_core_api}

# Filter private shared object
%{?filter_provides_in: %filter_provides_in %{_libdir}/.*\.so$}
%{?filter_setup}


%description
ffmpeg-php is an extension for PHP that adds an easy to use, object-oriented
API for accessing and retrieving information from video and audio files. 
It has methods for returning frames from movie files as images that can be 
manipulated using PHP's image functions. This works well for automatically 
creating thumbnail images from movies. ffmpeg-php is also useful for reporting
the duration and bitrate of audio files (mp3, wma...). ffmpeg-php can access
many of the video formats supported by ffmpeg (mov, avi, mpg, wmv...).


%prep
%setup -q -c
mv ffmpeg* %{ext_name}-nts

cd %{ext_name}-nts
%patch0 -p1 -b .incl
%patch1 -p1 -b .php54

# Sanity check, really often broken
extver=$(sed -n '/#define FFMPEG_PHP_VERSION/{s/.* "//;s/".*$//;p}' ffmpeg-php.c)
if test "x${extver}" != "x%{version}"; then
   : Error: Upstream extension version is ${extver}, expecting %{version}.
   exit 1
fi

# we will use include from php-devel
rm gd.h gd_io.h

cd ..
cat > %{ext_name}.ini << 'EOF'
; --- Enable %{name} extension module
extension=%{ext_name}.so

; --- options for %{name}
;ffmpeg.allow_persistent = 0
;ffmpeg.show_warnings = 0
EOF

# duplicate for ZTS build
cp -r %{ext_name}-nts %{ext_name}-zts


%build
cd %{ext_name}-nts
phpize
%configure \
    --with-libdir=%{_lib} \
    --with-ffmpeg=%{_includedir}/ffmpeg \
    --with-php-config=%{_bindir}/php-config
make %{?_smp_mflags}

cd ../%{ext_name}-zts
zts-phpize
%configure \
    --with-libdir=%{_lib} \
    --with-ffmpeg=%{_includedir}/ffmpeg \
    --with-php-config=%{_bindir}/zts-php-config
make %{?_smp_mflags}


%install
rm -rf %{buildroot}
# Install the NTS stuff
make -C %{ext_name}-nts install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ext_name}.ini %{buildroot}%{php_inidir}/%{ext_name}.ini

# Install the ZTS stuff
make -C %{ext_name}-zts install INSTALL_ROOT=%{buildroot}
install -D -m 644 %{ext_name}.ini %{buildroot}%{php_ztsinidir}/%{ext_name}.ini


%check
# simple module load test
%{__php} --no-php-ini \
    --define extension_dir=%{ext_name}-nts/modules \
    --define extension=%{ext_name}.so \
    --modules | grep %{ext_name}

%{__ztsphp} --no-php-ini \
    --define extension_dir=%{ext_name}-zts/modules \
    --define extension=%{ext_name}.so \
    --modules | grep %{ext_name}



%clean
rm -rf %{buildroot}


%files
%defattr(-,root,root,-)
%doc %{ext_name}-nts/{ChangeLog,CREDITS,EXPERIMENTAL,LICENSE,TODO,test_ffmpeg.php}

%config(noreplace) %{php_inidir}/%{ext_name}.ini
%{php_extdir}/%{ext_name}.so

%config(noreplace) %{php_ztsinidir}/%{ext_name}.ini
%{php_ztsextdir}/%{ext_name}.so


%changelog
* Mon Sep 17 2010 Remi Collet <rpms@famillecollet.com> 0.7.0-0.1.svn678
- update to 0.7.0 svn snapshot revision 678
- add patch for php 5.4
- add ZTS extension
- cleanup spec
- build with ffmpeg 0.10

* Sun Mar 21 2010 Remi Collet <rpms@famillecollet.com> 0.6.3-0.1.svn676
- update to 0.6.3 svn snapshot revision 676

* Wed Apr 23 2008 Remi Collet <rpms@famillecollet.com> 0.5.2.1-1
- update to 0.5.1.1

* Thu Nov 15 2007 Remi Collet <rpms@famillecollet.com> 0.5.1-2
- F8 rebuild

* Mon Aug 27 2007 Remi Collet <rpms@famillecollet.com> 0.5.1-2
- rename from ffmpeg-php to php-ffmpeg
- fix License

* Sat Jul 07 2007 Remi Collet <rpms@famillecollet.com> 0.5.1-1
- initial SPEC

