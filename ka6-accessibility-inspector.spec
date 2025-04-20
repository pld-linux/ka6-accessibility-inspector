#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	25.04.0
%define		kframever	6.8
%define		qtver		6.8
%define		kaname		accessibility-inspector
Summary:	Accessibility inspector
Name:		ka6-%{kaname}
Version:	25.04.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	0bcec41083852314e96d2836d79a02b2
URL:		https://kde.org
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	libqaccessibilityclient-qt6-devel >= 0.6.0
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Inspect your application's accessibility tree.

%prep
%setup -q -n %{kaname}-%{version}

%build
%cmake \
	-B build \
	-G Ninja \
	%{!?with_tests:-DBUILD_TESTING=OFF} \
	-DKDE_INSTALL_DOCBUNDLEDIR=%{_kdedocdir} \
	-DKDE_INSTALL_USE_QT_SYS_PATHS=ON

%ninja_build -C build

%if %{with tests}
ctest --test-dir build
%endif

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

%find_lang %{kaname} --all-name --with-kde

%clean
rm -rf $RPM_BUILD_ROOT

%post -p /sbin/ldconfig
%postun -p /sbin/ldconfig

%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/accessibilityinspector
%ghost %{_libdir}/libaccessibilityinspector.so.1
%attr(755,root,root) %{_libdir}/libaccessibilityinspector.so.*.*
%{_desktopdir}/org.kde.accessibilityinspector.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.accessibilityinspector.svg
%{_datadir}/metainfo/org.kde.accessibilityinspector.metainfo.xml
%{_datadir}/qlogging-categories6/accessibilityinspector.categories
