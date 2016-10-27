#
# Conditional build:
%bcond_with	unity	# Ubuntu Unity integration
#
Summary:	Photo manager for GNOME
Summary(pl.UTF-8):	Zarządca zdjęć dla GNOME
Name:		shotwell
Version:	0.24.1
Release:	2
License:	LGPL v2+ and CC-BY-SA
Group:		X11/Applications
Source0:	http://ftp.gnome.org/pub/GNOME/sources/shotwell/0.24/%{name}-%{version}.tar.xz
# Source0-md5:	b53b86424564d2f94d56621b1a10a8a4
Patch0:		%{name}-link.patch
Patch1:		%{name}-gitversion.patch
URL:		https://wiki.gnome.org/Apps/Shotwell
BuildRequires:	appstream-glib-devel
BuildRequires:	atk-devel
BuildRequires:	autoconf >= 2.69
BuildRequires:	automake >= 1:1.11
BuildRequires:	gettext-tools >= 0.19.7
BuildRequires:	gexiv2-devel >= 0.4.90
BuildRequires:	glib2-devel >= 1:2.32.0
BuildRequires:	gnome-doc-utils
BuildRequires:	gstreamer-devel >= 1.0.0
BuildRequires:	gstreamer-plugins-base-devel >= 1.0.0
BuildRequires:	gtk+3-devel >= 3.12.2
BuildRequires:	gtk-webkit4-devel
BuildRequires:	json-glib-devel >= 0.6.16
BuildRequires:	libexif-devel >= 1:0.6.16
BuildRequires:	libgee-devel >= 0.8.5
BuildRequires:	libgphoto2-devel >= 2.5.0
BuildRequires:	libraw-devel >= 0.14.7-2
BuildRequires:	libsoup-devel >= 2.26.0
BuildRequires:	libtool >= 2:2.2
%{?with_unity:BuildRequires:	libunity-devel}
BuildRequires:	libxml2-devel >= 1:2.6.32
BuildRequires:	pkgconfig >= 1:0.22
BuildRequires:	rest-devel >= 0.7
BuildRequires:	rpmbuild(macros) >= 1.311
BuildRequires:	sqlite3-devel >= 3.5.9
BuildRequires:	udev-glib-devel >= 1:145
BuildRequires:	vala >= 2:0.28.0
BuildRequires:	vala-gexiv2 >= 0.4.90
BuildRequires:	vala-libgee >= 0.8.5
BuildRequires:	yelp-tools
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	glib2 >= 1:2.32.0
Requires(post,postun):	gtk-update-icon-cache
Requires(post,postun):	hicolor-icon-theme
Requires:	glib2 >= 1:2.32.0
Requires:	gtk+3 >= 3.12.2
Requires:	gtk-webkit4
Requires:	hicolor-icon-theme
Requires:	libexif >= 1:0.6.16
Requires:	libgphoto2 >= 2.5.0
Requires:	libraw >= 0.14.7-2
Requires:	libsoup >= 2.26.0
Requires:	libxml2 >= 1:2.6.32
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
%patch1 -p1

# force rebuild without _GITVERSION
%{__rm} src/Resources.c

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
%configure \
	--disable-schemas-compile \
	--disable-silent-rules \
	%{?with_unity:--enable-unity-support}
%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

%{__rm} $RPM_BUILD_ROOT%{_libdir}/*.{a,la}
%{__rm} $RPM_BUILD_ROOT%{_libdir}/%{name}/plugins/builtin/*.la

%find_lang shotwell --with-gnome

%clean
rm -rf $RPM_BUILD_ROOT

%post
%update_icon_cache hicolor
%update_desktop_database
%glib_compile_schemas

%postun
%update_icon_cache hicolor
%update_desktop_database_postun
%glib_compile_schemas

%files -f shotwell.lang
%defattr(644,root,root,755)
%doc AUTHORS COPYING NEWS README THANKS
%attr(755,root,root) %{_bindir}/shotwell
%attr(755,root,root) %{_libdir}/libshotwell-plugin-common.so*
%{_desktopdir}/%{name}-viewer.desktop
%{_desktopdir}/%{name}.desktop
%dir %{_libdir}/%{name}
%attr(755,root,root) %{_libdir}/shotwell/shotwell-settings-migrator
%attr(755,root,root) %{_libdir}/shotwell/shotwell-video-thumbnailer
%{_datadir}/appdata/shotwell.appdata.xml
%{_datadir}/%{name}
%{_datadir}/glib-2.0/schemas/org.yorba.shotwell.gschema.xml
%{_datadir}/glib-2.0/schemas/org.yorba.shotwell-extras.gschema.xml
%dir %{_libdir}/%{name}/plugins
%dir %{_libdir}/%{name}/plugins/builtin
%attr(755,root,root) %{_libdir}/%{name}/plugins/builtin/*.so
%{_iconsdir}/hicolor/*x*/apps/shotwell.png
%{_iconsdir}/hicolor/symbolic/apps/shotwell-symbolic.svg
%{_mandir}/man1/shotwell.1*
