%{!?pear_metadir: %global pear_metadir %{pear_phpdir}}
%{!?__pear: %{expand: %%global __pear %{_bindir}/pear}}
%global pear_name Horde_Service_Weather

Name:           php-horde-Horde-Service-Weather
Version:        2.0.4
Release:        1%{?dist}
Summary:        Horde Weather Provider

Group:          Development/Libraries
License:        BSD-2-Clause
URL:            http://pear.horde.org/package/Horde_Service_Weather
Source0:        http://pear.horde.org/get/%{pear_name}-%{version}.tgz

BuildRoot:      %{_tmppath}/%{name}-%{version}-%{release}-root-%(%{__id_u} -n)
BuildArch:      noarch
BuildRequires:  php-pear(PEAR)

Requires(post): %{__pear}
Requires(postun): %{__pear}
Requires:       php-pear(PEAR)
Requires:       php-pear(pear.horde.org/Horde_Date) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Date) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Exception) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Exception) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Http) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Http) < 3.0.0alpha1
Requires:       php-pear(pear.horde.org/Horde_Url) >= 2.0.0
Requires:       php-pear(pear.horde.org/Horde_Url) < 3.0.0alpha1
Requires:       php-pear(PEAR) >= 1.7.0
Provides:       php-pear(pear.horde.org/Horde_Service_Weather) = %{version}
BuildRequires:  php-channel(pear.horde.org)
Requires:       php-channel(pear.horde.org)

%description
Set of classes that provide an abstraction to various online weather
service providers. Includes drivers for WeatherUnderground,
WorldWeatherOnline, and Google Weather.

%prep
%setup -q -c
[ -f package2.xml ] || mv package.xml package2.xml
mv package2.xml %{pear_name}-%{version}/%{name}.xml

cd %{pear_name}-%{version}


%build
cd %{pear_name}-%{version}
# Empty build section, most likely nothing required.


%install
cd %{pear_name}-%{version}
rm -rf $RPM_BUILD_ROOT
%{__pear} install --nodeps --packagingroot $RPM_BUILD_ROOT %{name}.xml

# Clean up unnecessary files
rm -rf $RPM_BUILD_ROOT%{pear_metadir}/.??*

# Install XML package description
mkdir -p $RPM_BUILD_ROOT%{pear_xmldir}
install -pm 644 %{name}.xml $RPM_BUILD_ROOT%{pear_xmldir}


%clean
rm -rf $RPM_BUILD_ROOT


%post
%{__pear} install --nodeps --soft --force --register-only \
    %{pear_xmldir}/%{name}.xml >/dev/null || :

%postun
if [ $1 -eq 0 ] ; then
    %{__pear} uninstall --nodeps --ignore-errors --register-only \
        pear.horde.org/%{pear_name} >/dev/null || :
fi


%files
%defattr(-,root,root,-)
%doc %{pear_docdir}/%{pear_name}


%{pear_xmldir}/%{name}.xml
# Expand this as needed to avoid owning dirs owned by our dependencies
# and to avoid unowned dirs
%{pear_phpdir}/Horde/Service/Weather/Current/Base.php
%{pear_phpdir}/Horde/Service/Weather/Current/WeatherUnderground.php
%{pear_phpdir}/Horde/Service/Weather/Current/Wwo.php
%{pear_phpdir}/Horde/Service/Weather/Exception/InvalidProperty.php
%{pear_phpdir}/Horde/Service/Weather/Forecast/Base.php
%{pear_phpdir}/Horde/Service/Weather/Forecast/WeatherUnderground.php
%{pear_phpdir}/Horde/Service/Weather/Forecast/Wwo.php
%{pear_phpdir}/Horde/Service/Weather/Period/Base.php
%{pear_phpdir}/Horde/Service/Weather/Period/WeatherUnderground.php
%{pear_phpdir}/Horde/Service/Weather/Period/Wwo.php
%{pear_phpdir}/Horde/Service/Weather/Base.php
%{pear_phpdir}/Horde/Service/Weather/Exception.php
%{pear_phpdir}/Horde/Service/Weather/Station.php
%{pear_phpdir}/Horde/Service/Weather/Translation.php
%{pear_phpdir}/Horde/Service/Weather/WeatherUnderground.php
%{pear_phpdir}/Horde/Service/Weather/WeatherUnderground_Strings.php
%{pear_phpdir}/Horde/Service/Weather/Wwo.php
%{pear_phpdir}/Horde/Service/Weather/Wwo_Strings.php
%{pear_phpdir}/Horde/Service/Weather.php
%{pear_datadir}/Horde_Service_Weather
%{pear_testdir}/Horde_Service_Weather


%changelog
