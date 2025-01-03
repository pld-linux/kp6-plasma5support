#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeplasmaver	6.2.5
%define		qtver		5.15.2
%define		kpname		plasma5support
%define		kf6ver		5.39.0

Summary:	plasma 5 support
Name:		kp6-%{kpname}
Version:	6.2.5
Release:	1
License:	LGPL v2.1+
Group:		X11/Libraries
Source0:	https://download.kde.org/stable/plasma/%{kdeplasmaver}/%{kpname}-%{version}.tar.xz
# Source0-md5:	921083a3dbe054da9bbffe3ba075ac25
URL:		http://www.kde.org/
BuildRequires:	Qt6Core-devel >= 5.15.0
BuildRequires:	Qt6Gui-devel >= 5.15.0
BuildRequires:	cmake >= 3.16.0
BuildRequires:	gettext-devel
BuildRequires:	kf6-extra-cmake-modules >= 5.82
BuildRequires:	kf6-kauth-devel >= 5.82
BuildRequires:	kf6-kcoreaddons-devel >= 5.85.0
BuildRequires:	kf6-kdbusaddons-devel >= 5.82
BuildRequires:	kf6-kdeclarative-devel >= 5.82
BuildRequires:	kf6-ki18n-devel >= 5.82
BuildRequires:	kf6-kio-devel >= 5.82
BuildRequires:	kf6-knotifications-devel >= 5.82
BuildRequires:	kf6-kservice-devel >= 5.85.0
BuildRequires:	kf6-solid-devel >= 5.85.0
BuildRequires:	kp6-libksysguard-devel
BuildRequires:	ninja
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.164
BuildRequires:	xz
Obsoletes:	kp5-%{kpname} < %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		qt6dir		%{_libdir}/qt6

%description
plasma 5 support

%package devel
Summary:	Header files for %{kpname} development
Summary(pl.UTF-8):	Pliki nagłówkowe dla programistów używających %{kpname}
Group:		X11/Development/Libraries
Requires:	%{name} = %{version}-%{release}
Obsoletes:	kp5-%{kpname}-devel < %{version}

%description devel
Header files for %{kpname} development.

%description devel -l pl.UTF-8
Pliki nagłówkowe dla programistów używających %{kpname}.

%prep
%setup -q -n %{kpname}-%{version}

%build
%cmake -B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir}
%ninja_build -C build

%if %{with tests}
ctest
%endif

%install
rm -rf $RPM_BUILD_ROOT
%ninja_install -C build

%find_lang libplasma5support --all-name

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f libplasma5support.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libPlasma5Support.so.*.*
%ghost %{_libdir}/libPlasma5Support.so.6
%dir %{_libdir}/qt6/qml/org/kde/plasma/plasma5support
%{_libdir}/qt6/qml/org/kde/plasma/plasma5support/kde-qmlmodule.version
%attr(755,root,root) %{_libdir}/qt6/qml/org/kde/plasma/plasma5support/libplasma5supportplugin.so
%{_libdir}/qt6/qml/org/kde/plasma/plasma5support/plasma5supportplugin.qmltypes
%{_libdir}/qt6/qml/org/kde/plasma/plasma5support/qmldir
%dir %{_libdir}/qt6/plugins/plasma5support
%dir %{_libdir}/qt6/plugins/plasma5support/dataengine
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma5support/dataengine/plasma_engine_devicenotifications.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma5support/dataengine/plasma_engine_keystate.so
%dir %{_datadir}/plasma5support
%dir %{_datadir}/plasma5support/services
%{_datadir}/plasma5support/services/dataengineservice.operations
%{_datadir}/plasma5support/services/plasmoidservice.operations
%{_datadir}/plasma5support/services/storage.operations
%{_datadir}/qlogging-categories6/plasma5support.categories
%{_datadir}/qlogging-categories6/plasma5support.renamecategories
%{_datadir}/plasma5support/services/modifierkeystate.operations
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma5support/dataengine/plasma_engine_hotplug.so
%attr(755,root,root) %{_libdir}/qt6/plugins/plasma5support/dataengine/plasma_engine_soliddevice.so
%{_datadir}/plasma5support/services/hotplug.operations
%{_datadir}/plasma5support/services/soliddevice.operations


%files devel
%defattr(644,root,root,755)
%{_includedir}/Plasma5Support
%{_libdir}/cmake/Plasma5Support
%{_libdir}/libPlasma5Support.so
