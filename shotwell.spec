#
# Conditional build:
%bcond_with	apport	# Ubuntu apport hook
%bcond_without	opencv	# faces detection using OpenCV
%bcond_with	unity	# Ubuntu Unity integration
#
Summary:	Photo manager for GNOME
Summary(pl.UTF-8):	Zarządca zdjęć dla GNOME
Name:		shotwell
Version:	0.32.10
Release:	1
License:	LGPL v2+ and CC-BY-SA
Group:		X11/Applications
Source0:	https://download.gnome.org/sources/shotwell/0.32/%{name}-%{version}.tar.xz
# Source0-md5:	30c7a0e4ef83e770af40e5e5c2304075
Patch0:		%{name}-unity.patch
URL:		https://wiki.gnome.org/Apps/Shotwell
BuildRequires:	cairo-devel
BuildRequires:	gcr-devel >= 3
BuildRequires:	gcr-ui-devel >= 3
BuildRequires:	gdk-pixbuf2-devel >= 2.0
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	gexiv2-devel >= 0.12.3
BuildRequires:	glib2-devel >= 1:2.40.0
BuildRequires:	gstreamer-devel >= 1.20
BuildRequires:	gstreamer-plugins-base-devel >= 1.20
BuildRequires:	gtk+3-devel >= 3.22
BuildRequires:	gtk-webkit4.1-devel >= 2.26
BuildRequires:	json-glib-devel >= 1.0
BuildRequires:	libexif-devel >= 1:0.6.16
BuildRequires:	libgee-devel >= 0.8.5
BuildRequires:	libgphoto2-devel >= 2.5.0
BuildRequires:	libportal-devel >= 0.5
BuildRequires:	libportal-gtk3-devel >= 0.5
BuildRequires:	libraw-devel >= 0.14.7-2
BuildRequires:	libsecret-devel
BuildRequires:	libsoup3-devel >= 3.0
%{?with_unity:BuildRequires:	libunity-devel}
BuildRequires:	libwebp-devel
BuildRequires:	libxml2-devel >= 1:2.6.32
BuildRequires:	meson >= 0.59.0
BuildRequires:	ninja >= 1.5
%{?with_opencv:BuildRequires:	opencv-devel >= 1:3.4.0}
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	rpmbuild(macros) >= 1.736
BuildRequires:	sqlite3-devel >= 3.5.9
BuildRequires:	tar >= 1:1.22
BuildRequires:	udev-glib-devel >= 1:145
BuildRequires:	vala >= 2:0.28.0
BuildRequires:	vala-gcr >= 3
BuildRequires:	vala-gcr-ui >= 3
BuildRequires:	vala-gexiv2 >= 0.12.3
BuildRequires:	vala-libgee >= 0.8.5
BuildRequires:	vala-libportal >= 0.5
BuildRequires:	vala-libportal-gtk3 >= 0.5
BuildRequires:	vala-libsecret
%{?with_unity:BuildRequires:	vala-libunity}
BuildRequires:	xz
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.40.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	gexiv2 >= 0.12.3
Requires:	glib2 >= 1:2.40.0
Requires:	gtk+3 >= 3.22
Requires:	gtk-webkit4.1 >= 2.26
Requires:	hicolor-icon-theme
Requires:	json-glib >= 1.0
Requires:	libexif >= 1:0.6.16
Requires:	libgee >= 0.8.5
Requires:	libgphoto2 >= 2.5.0
Requires:	libraw >= 0.14.7-2
Requires:	libsoup3 >= 3.0
Requires:	libxml2 >= 1:2.6.32
%{?with_opencv:Requires:	opencv >= 1:3.4.0}
Requires:	sqlite3 >= 3.5.9
Requires:	udev-glib >= 1:145
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Shotwell is a digital photo organizer designed for the GNOME desktop
environment. It allows you to import photos from disk or camera,
organize them in various ways, view them in full-window or fullscreen
mode, and export them to share with others.

%description -l pl.UTF-8
Shotwell to organizator zdjęć cyfrowych, zaprojektowany dla środowiska
graficznego GNOME. Pozwala importować zdjęcia z dysku lub aparatu,
organizować je na różne sposoby, przeglądać w trybie okienkowym lub
pełnoekranowym oraz eksportować, aby podzielić się nimi z innymi.

%prep
%setup -q
%patch0 -p1

%build
%meson build \
	--default-library=shared \
	%{?with_opencv:-Dface_detection=true} \
	%{!?with_apport:-Dinstall_apport_hook=false} \
	%{?with_unity:-Dunity_support=true}

%ninja_build -C build

%install
rm -rf $RPM_BUILD_ROOT

%ninja_install -C build

# API not exported, so no need for development symlinks
%{__rm} $RPM_BUILD_ROOT%{_libdir}/libshotwell-*.so

# not supported by glibc (as of 2.37)
%{__rm} -r $RPM_BUILD_ROOT%{_localedir}/ie

%find_lang shotwell --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
/sbin/ldconfig
%update_icon_cache hicolor
%update_desktop_database
%glib_compile_schemas

%postun
/sbin/ldconfig
%update_icon_cache hicolor
%update_desktop_database_postun
%glib_compile_schemas

%files -f shotwell.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING MAINTAINERS NEWS README.md THANKS
%attr(755,root,root) %{_bindir}/shotwell
%attr(755,root,root) %{_libdir}/libshotwell-authenticator.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshotwell-authenticator.so.0
%attr(755,root,root) %{_libdir}/libshotwell-plugin-common.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshotwell-plugin-common.so.0
%attr(755,root,root) %{_libdir}/libshotwell-plugin-dev-1.0.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libshotwell-plugin-dev-1.0.so.0
%if "%{_libexecdir}" != "%{_libdir}"
%dir %{_libexecdir}/%{name}
%endif
%attr(755,root,root) %{_libexecdir}/%{name}/shotwell-authenticator
%if %{with opencv}
%attr(755,root,root) %{_libexecdir}/%{name}/shotwell-facedetect
%endif
%attr(755,root,root) %{_libexecdir}/%{name}/shotwell-settings-migrator
%attr(755,root,root) %{_libexecdir}/%{name}/shotwell-video-metadata-handler
%attr(755,root,root) %{_libexecdir}/%{name}/shotwell-video-thumbnailer
%dir %{_libdir}/%{name}
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/builtin
%attr(755,root,root) %{_libdir}/%{name}/plugins/builtin/libshotwell-publishing.so
%attr(755,root,root) %{_libdir}/%{name}/plugins/builtin/libshotwell-transitions.so
%if %{with opencv}
%dir %{_datadir}/%{name}
%{_datadir}/%{name}/facedetect
%{_datadir}/dbus-1/services/org.gnome.Shotwell.Faces1.service
%endif
%if %{with apport}
%{_datadir}/apport/package-hooks/shotwell.py
%endif
%{_datadir}/glib-2.0/schemas/org.gnome.shotwell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.gnome.shotwell-extras.gschema.xml
%{_datadir}/glib-2.0/schemas/org.yorba.shotwell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.yorba.shotwell-extras.gschema.xml
%{_datadir}/metainfo/org.gnome.Shotwell.appdata.xml
%{_desktopdir}/org.gnome.Shotwell.desktop
%{_desktopdir}/org.gnome.Shotwell-Viewer.desktop
%{_desktopdir}/org.gnome.Shotwell.Auth.desktop
%{_iconsdir}/hicolor/*x*/apps/org.gnome.Shotwell.png
%{_iconsdir}/hicolor/scalable/apps/org.gnome.Shotwell.svg
%{_iconsdir}/hicolor/symbolic/apps/org.gnome.Shotwell-symbolic.svg
%{_mandir}/man1/shotwell.1*
