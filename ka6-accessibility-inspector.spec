#
# Conditional build:
%bcond_with	tests		# build with tests
%define		kdeappsver	26.08.0
%define		kframever	6.11
%define		qtver		6.8
%define		kaname		accessibility-inspector
Summary:	Accessibility inspector
Summary(pl.UTF-8):	Inspektor dostępności
Name:		ka6-%{kaname}
Version:	26.08.0
Release:	1
License:	GPL v2+/LGPL v2.1+
Group:		X11/Applications
Source0:	https://download.kde.org/stable/release-service/%{kdeappsver}/src/%{kaname}-%{version}.tar.xz
# Source0-md5:	68f003791df19b8b7ce29c41f6018dd6
URL:		https://kde.org
BuildRequires:	Qt6Core-devel >= %{qtver}
BuildRequires:	Qt6Gui-devel
BuildRequires:	cmake >= 3.20
BuildRequires:	kf6-kconfigwidgets-devel >= %{kframever}
BuildRequires:	kf6-kcoreaddons-devel >= %{kframever}
BuildRequires:	kf6-kcrash-devel >= %{kframever}
BuildRequires:	kf6-kdbusaddons-devel >= %{kframever}
BuildRequires:	kf6-kguiaddons-devel >= %{kframever}
BuildRequires:	kf6-ki18n-devel >= %{kframever}
BuildRequires:	kf6-kxmlgui-devel >= %{kframever}
BuildRequires:	libqaccessibilityclient-qt6-devel >= 0.6.0
BuildRequires:	qt6-build >= %{qtver}
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	tar >= 1:1.22
BuildRequires:	xz
Requires(post,postun):	desktop-file-utils
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Inspect your application's accessibility tree.

%description -l pl.UTF-8
Sprawdź drzewo dostępności swojej aplikacji.

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

%post
/sbin/ldconfig
%update_desktop_database_post

%postun
/sbin/ldconfig
%update_desktop_database_postun


%files -f %{kaname}.lang
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/accessibilityinspector
%ghost %{_libdir}/libaccessibilityinspector.so.1
%{_libdir}/libaccessibilityinspector.so.*.*
%{_desktopdir}/org.kde.accessibilityinspector.desktop
%{_iconsdir}/hicolor/scalable/apps/org.kde.accessibilityinspector.svg
%{_datadir}/metainfo/org.kde.accessibilityinspector.metainfo.xml
%{_datadir}/qlogging-categories6/accessibilityinspector.categories
