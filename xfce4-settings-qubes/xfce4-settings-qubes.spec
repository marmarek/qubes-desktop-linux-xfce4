%if 0%{?qubes_builder}
%define _sourcedir %(pwd)/xfce4-settings-qubes
%endif

Name:		xfce4-settings-qubes
Version:	1.5
Release:	1%{?dist}
Summary:	Default Xfce4 panel settings for Qubes

Group:		User Interface/Desktops
License:	GPLv2+
URL:		http://www.qubes-os.org/
Source0:	xfce4-panel-qubes-default.xml
Source1:	inhibit-systemd-power-handling.desktop
Source2:	xsettings.xml
Source3:	xfwm4.xml
Source4:	xfce4-desktop.xml

Requires:	qubes-artwork
Requires:	xfce4-panel
Requires(post):	xfce4-panel

%description
%{summary}

%prep

%build


%install
install -m 644 -D %{SOURCE0} %{buildroot}%{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes
install -m 644 -D %{SOURCE1} %{buildroot}%{_sysconfdir}/xdg/autostart/inhibit-systemd-power-handling.desktop
install -m 644 -D %{SOURCE2} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes
install -m 644 -D %{SOURCE3} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
install -m 644 -D %{SOURCE4} %{buildroot}%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml

%define settings_replace() \
origfile="`echo %{1} | sed 's/\.qubes$//'`"\
backupfile="`echo %{1} | sed s/\.qubes$/\.xfce4/`"\
if [ -r "$origfile" -a ! -r "$backupfile" ]; then\
	mv -f "$origfile" "$backupfile"\
fi\
cp -f "%{1}" "$origfile"\
%{nil}

%triggerin -- xfce4-panel
%settings_replace %{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes

%triggerin -- xfce4-settings
%settings_replace %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes

%triggerin -- xscreensaver-base

conffile=/etc/xscreensaver/XScreenSaver.ad.tail

if ! grep -q "! Qubes options begin" $conffile; then
    ( echo -e "! Qubes options begin - do not edit\n! Qubes options end"; cat $conffile) > $conffile.tmp
    mv $conffile.tmp $conffile
fi

sed -e '/! Qubes options begin/,/! Qubes options end/c \
! Qubes options begin - do not edit\
*newLoginCommand:\
! Qubes options end' -i $conffile

update-xscreensaver-hacks

%postun
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes"
REPLACEFILE="${REPLACEFILE} %{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes"
if [ $1 -lt 1 ]; then
	for file in ${REPLACEFILE}; do
		origfile="`echo $file | sed 's/\.qubes$//'`"
		backupfile="`echo $file | sed 's/\.qubes$/\.xfce4/'`"
		mv -f "$backupfile" "$origfile"
	done
fi

%files
%{_sysconfdir}/xdg/autostart/inhibit-systemd-power-handling.desktop
%{_sysconfdir}/xdg/xfce4/panel/default.xml.qubes
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xsettings.xml.qubes
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfwm4.xml
%{_sysconfdir}/xdg/xfce4/xfconf/xfce-perchannel-xml/xfce4-desktop.xml


%changelog

