%define kmod_name		ionic
%define kmod_vendor		redhat
%define kmod_rpm_name		kmod-redhat-ionic
%define kmod_driver_version	4.18.0.210_dup8.2
%define kmod_driver_epoch	%{nil}
%define kmod_rpm_release	2
%define kmod_kernel_version	4.18.0-193.el8
%define kmod_kernel_version_min	%{nil}
%define kmod_kernel_version_dep	%{nil}
%define kmod_kbuild_dir		drivers/net/ethernet/pensando/ionic
%define kmod_dependencies       %{nil}
%define kmod_dist_build_deps	%{nil}
%define kmod_build_dependencies	%{nil}
%define kmod_devel_package	0
%define kmod_devel_src_paths	%{nil}
%define kmod_install_path	extra/kmod-redhat-ionic
%define kernel_pkg		kernel
%define kernel_devel_pkg	kernel-devel
%define kernel_modules_pkg	kernel-modules

%{!?dist: %define dist .el8_2}
%{!?make_build: %define make_build make}

%if "%{kmod_kernel_version_dep}" == ""
%define kmod_kernel_version_dep %{kmod_kernel_version}
%endif

%if "%{kmod_dist_build_deps}" == ""
%if (0%{?rhel} > 7) || (0%{?centos} > 7)
%define kmod_dist_build_deps redhat-rpm-config kernel-abi-whitelists elfutils-libelf-devel kernel-rpm-macros kmod
%else
%define kmod_dist_build_deps redhat-rpm-config kernel-abi-whitelists
%endif
%endif

Source0:	%{kmod_name}-%{kmod_vendor}-%{kmod_driver_version}.tar.bz2
# Source code patches
Patch0:	0000-drivers_ionic_only_Remove_inclusion_of_vermagic_.patch
Patch1:	0001-ionic_Use_debugfs_create_bool__to_export_bool.patch
Patch2:	0002-ionic_support_longer_tx_sg_lists.patch
Patch3:	0003-ionic_updates_to_ionic_FW_api_description.patch
Patch4:	0004-ionic_protect_vf_calls_from_fw_reset.patch
Patch5:	0005-ionic_add_support_for_more_xcvr_types.patch
Patch6:	0006-ionic_shorter_dev_cmd_wait_time.patch
Patch7:	0007-ionic_reset_device_at_probe.patch
Patch8:	0008-ionic_ionic_intr_free_parameter_change.patch
Patch9:	0009-ionic_more_ionic_name_tweaks.patch
Patch10:	0010-ionic_add_more_ethtool_stats.patch
Patch11:	0011-ionic_wait_on_queue_start_until_after_IFF_UP.patch
Patch12:	0012-ionic_remove_support_for_mgmt_device.patch
Patch13:	0013-ionic_export_features_for_vlans_to_use.patch
Patch14:	0014-ionic_no_link_check_while_resetting_queues.patch
Patch15:	0015-ionic_add_pcie_print_link_status.patch
Patch16:	0016-ionic_tame_the_watchdog_timer_on_reconfig.patch
Patch17:	0017-ionic-update-the-queue-count-on-open.patch
Patch18:	9000-Makefile-CONFIG_IONIC.patch
Patch19:	9001-add-ionic_backport_compat-h.patch
Patch20:	9002-SFF8024-enum.patch
Patch21:	9003-add-dynamic_hex_dump.patch
Patch22:	9004-Revert-netdrv-netdev-pass-the-stuck-queue-to-the-timeout-ha.patch
Patch23:	9005-add-devlink-constants.patch
Patch24:	9006-Revert-netdrv-ionic-let-core-reject-the-unsupported-coalesc.patch
Patch25:	9007-Revert-netdrv-ionic-use-new-helper-tcp_v6_gso_csum_prep.patch
Patch26:	9008-module-version.patch

%define findpat %( echo "%""P" )
%define __find_requires /usr/lib/rpm/redhat/find-requires.ksyms
%define __find_provides /usr/lib/rpm/redhat/find-provides.ksyms %{kmod_name} %{?epoch:%{epoch}:}%{version}-%{release}
%define sbindir %( if [ -d "/sbin" -a \! -h "/sbin" ]; then echo "/sbin"; else echo %{_sbindir}; fi )
%define dup_state_dir %{_localstatedir}/lib/rpm-state/kmod-dups
%define kver_state_dir %{dup_state_dir}/kver
%define kver_state_file %{kver_state_dir}/%{kmod_kernel_version}.%(arch)
%define dup_module_list %{dup_state_dir}/rpm-kmod-%{kmod_name}-modules

Name:		kmod-redhat-ionic
Version:	%{kmod_driver_version}
Release:	%{kmod_rpm_release}%{?dist}
%if "%{kmod_driver_epoch}" != ""
Epoch:		%{kmod_driver_epoch}
%endif
Summary:	ionic kernel module for Driver Update Program
Group:		System/Kernel
License:	GPLv2
URL:		https://www.kernel.org/
BuildRoot:	%(mktemp -ud %{_tmppath}/%{name}-%{version}-%{release}-XXXXXX)
BuildRequires:	%kernel_devel_pkg = %kmod_kernel_version
%if "%{kmod_dist_build_deps}" != ""
BuildRequires:	%{kmod_dist_build_deps}
%endif
ExclusiveArch:	x86_64
%global kernel_source() /usr/src/kernels/%{kmod_kernel_version}.$(arch)

%global _use_internal_dependency_generator 0
%if "%{?kmod_kernel_version_min}" != ""
Provides:	%kernel_modules_pkg >= %{kmod_kernel_version_min}.%{_target_cpu}
%else
Provides:	%kernel_modules_pkg = %{kmod_kernel_version_dep}.%{_target_cpu}
%endif
Provides:	kmod-%{kmod_name} = %{?epoch:%{epoch}:}%{version}-%{release}
Requires(post):	%{sbindir}/weak-modules
Requires(postun):	%{sbindir}/weak-modules
Requires:	kernel >= 4.18.0-193.el8

Requires:	kernel < 4.18.0-194.el8
%if 0
Requires: firmware(%{kmod_name}) = ENTER_FIRMWARE_VERSION
%endif
%if "%{kmod_build_dependencies}" != ""
BuildRequires:  %{kmod_build_dependencies}
%endif
%if "%{kmod_dependencies}" != ""
Requires:       %{kmod_dependencies}
%endif
# if there are multiple kmods for the same driver from different vendors,
# they should conflict with each other.
Conflicts:	kmod-%{kmod_name}

%description
ionic kernel module for Driver Update Program

%if 0

%package -n kmod-redhat-ionic-firmware
Version:	ENTER_FIRMWARE_VERSION
Summary:	ionic firmware for Driver Update Program
Provides:	firmware(%{kmod_name}) = ENTER_FIRMWARE_VERSION
%if "%{kmod_kernel_version_min}" != ""
Provides:	%kernel_modules_pkg >= %{kmod_kernel_version_min}.%{_target_cpu}
%else
Provides:	%kernel_modules_pkg = %{kmod_kernel_version_dep}.%{_target_cpu}
%endif
%description -n  kmod-redhat-ionic-firmware
ionic firmware for Driver Update Program


%files -n kmod-redhat-ionic-firmware
%defattr(644,root,root,755)
%{FIRMWARE_FILES}

%endif

# Development package
%if 0%{kmod_devel_package}
%package -n kmod-redhat-ionic-devel
Version:	%{kmod_driver_version}
Requires:	kernel >= 4.18.0-193.el8

Requires:	kernel < 4.18.0-194.el8
Summary:	ionic development files for Driver Update Program

%description -n  kmod-redhat-ionic-devel
ionic development files for Driver Update Program


%files -n kmod-redhat-ionic-devel
%defattr(644,root,root,755)
/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/
%endif

%post
modules=( $(find /lib/modules/%{kmod_kernel_version}.%(arch)/%{kmod_install_path} | grep '\.ko$') )
printf '%s\n' "${modules[@]}" | %{sbindir}/weak-modules --add-modules --no-initramfs

mkdir -p "%{kver_state_dir}"
touch "%{kver_state_file}"

exit 0

%posttrans
# We have to re-implement part of weak-modules here because it doesn't allow
# calling initramfs regeneration separately
if [ -f "%{kver_state_file}" ]; then
	kver_base="%{kmod_kernel_version_dep}"
	kvers=$(ls -d "/lib/modules/${kver_base%%.*}"*)

	for k_dir in $kvers; do
		k="${k_dir#/lib/modules/}"

		tmp_initramfs="/boot/initramfs-$k.tmp"
		dst_initramfs="/boot/initramfs-$k.img"

		# The same check as in weak-modules: we assume that the kernel present
		# if the symvers file exists.
		if [ -e "/boot/symvers-$k.gz" ]; then
			/usr/bin/dracut -f "$tmp_initramfs" "$k" || exit 1
			cmp -s "$tmp_initramfs" "$dst_initramfs"
			if [ "$?" = 1 ]; then
				mv "$tmp_initramfs" "$dst_initramfs"
			else
				rm -f "$tmp_initramfs"
			fi
		fi
	done

	rm -f "%{kver_state_file}"
	rmdir "%{kver_state_dir}" 2> /dev/null
fi

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0

%preun
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
	mkdir -p "%{kver_state_dir}"
	touch "%{kver_state_file}"
fi

mkdir -p "%{dup_state_dir}"
rpm -ql kmod-redhat-ionic-%{kmod_driver_version}-%{kmod_rpm_release}%{?dist}.$(arch) | \
	grep '\.ko$' > "%{dup_module_list}"

%postun
if rpm -q --filetriggers kmod 2> /dev/null| grep -q "Trigger for weak-modules call on kmod removal"; then
	initramfs_opt="--no-initramfs"
else
	initramfs_opt=""
fi

modules=( $(cat "%{dup_module_list}") )
rm -f "%{dup_module_list}"
printf '%s\n' "${modules[@]}" | %{sbindir}/weak-modules --remove-modules $initramfs_opt

rmdir "%{dup_state_dir}" 2> /dev/null

exit 0

%files
%defattr(644,root,root,755)
/lib/modules/%{kmod_kernel_version}.%(arch)
/etc/depmod.d/%{kmod_name}.conf
%doc /usr/share/doc/%{kmod_rpm_name}/greylist.txt
%doc /usr/share/doc/kmod-redhat-ionic/README.interface_naming
%doc /usr/share/doc/kmod-redhat-ionic/examples/81-pensando-net.rules
%doc /usr/share/doc/kmod-redhat-ionic/examples/10-ionic.link

%prep
%setup -n %{kmod_name}-%{kmod_vendor}-%{kmod_driver_version}

%patch0 -p1
%patch1 -p1
%patch2 -p1
%patch3 -p1
%patch4 -p1
%patch5 -p1
%patch6 -p1
%patch7 -p1
%patch8 -p1
%patch9 -p1
%patch10 -p1
%patch11 -p1
%patch12 -p1
%patch13 -p1
%patch14 -p1
%patch15 -p1
%patch16 -p1
%patch17 -p1
%patch18 -p1
%patch19 -p1
%patch20 -p1
%patch21 -p1
%patch22 -p1
%patch23 -p1
%patch24 -p1
%patch25 -p1
%patch26 -p1
set -- *
mkdir source
mv "$@" source/
mkdir obj

%build
rm -rf obj
cp -r source obj

PWD_PATH="$PWD"
%if "%{workaround_no_pwd_rel_path}" != "1"
PWD_PATH=$(realpath --relative-to="%{kernel_source}" . 2>/dev/null || echo "$PWD")
%endif
%{make_build} -C %{kernel_source} V=1 M="$PWD_PATH/obj/%{kmod_kbuild_dir}" \
	NOSTDINC_FLAGS="-I$PWD_PATH/obj/include -I$PWD_PATH/obj/include/uapi %{nil}" \
	EXTRA_CFLAGS="%{nil}" \
	%{nil}
# mark modules executable so that strip-to-file can strip them
find obj/%{kmod_kbuild_dir} -name "*.ko" -type f -exec chmod u+x '{}' +

whitelist="/lib/modules/kabi-current/kabi_whitelist_%{_target_cpu}"
for modules in $( find obj/%{kmod_kbuild_dir} -name "*.ko" -type f -printf "%{findpat}\n" | sed 's|\.ko$||' | sort -u ) ; do
	# update depmod.conf
	module_weak_path=$(echo "$modules" | sed 's/[\/]*[^\/]*$//')
	if [ -z "$module_weak_path" ]; then
		module_weak_path=%{name}
	else
		module_weak_path=%{name}/$module_weak_path
	fi
	echo "override $(echo $modules | sed 's/.*\///')" \
	     "$(echo "%{kmod_kernel_version_dep}" |
	        sed 's/\.[^\.]*$//;
		     s/\([.+?^$\/\\|()\[]\|\]\)/\\\0/g').*" \
		     "weak-updates/$module_weak_path" >> source/depmod.conf

	# update greylist
	nm -u obj/%{kmod_kbuild_dir}/$modules.ko | sed 's/.*U //' |  sed 's/^\.//' | sort -u | while read -r symbol; do
		grep -q "^\s*$symbol\$" $whitelist || echo "$symbol" >> source/greylist
	done
done
sort -u source/greylist | uniq > source/greylist.txt

%install
export INSTALL_MOD_PATH=$RPM_BUILD_ROOT
export INSTALL_MOD_DIR=%{kmod_install_path}
PWD_PATH="$PWD"
%if "%{workaround_no_pwd_rel_path}" != "1"
PWD_PATH=$(realpath --relative-to="%{kernel_source}" . 2>/dev/null || echo "$PWD")
%endif
make -C %{kernel_source} modules_install \
	M=$PWD_PATH/obj/%{kmod_kbuild_dir}
# Cleanup unnecessary kernel-generated module dependency files.
find $INSTALL_MOD_PATH/lib/modules -iname 'modules.*' -exec rm {} \;

install -m 644 -D source/depmod.conf $RPM_BUILD_ROOT/etc/depmod.d/%{kmod_name}.conf
install -m 644 -D source/greylist.txt $RPM_BUILD_ROOT/usr/share/doc/%{kmod_rpm_name}/greylist.txt
%if 0
%{FIRMWARE_FILES_INSTALL}
%endif
%if 0%{kmod_devel_package}
install -m 644 -D $PWD/obj/%{kmod_kbuild_dir}/Module.symvers $RPM_BUILD_ROOT/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/build/Module.symvers

if [ -n "%{kmod_devel_src_paths}" ]; then
	for i in %{kmod_devel_src_paths}; do
		mkdir -p "$RPM_BUILD_ROOT/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/build/$(dirname "$i")"
		cp -rv "$PWD/source/$i" \
			"$RPM_BUILD_ROOT/lib/modules/%{kmod_rpm_name}-%{kmod_driver_version}/build/$i"
	done
fi
%endif
install -m 664 -D source/extra//usr/share/doc/kmod-redhat-ionic/README.interface_naming $RPM_BUILD_ROOT//usr/share/doc/kmod-redhat-ionic/README.interface_naming

install -m 664 -D source/extra//usr/share/doc/kmod-redhat-ionic/examples/81-pensando-net.rules $RPM_BUILD_ROOT//usr/share/doc/kmod-redhat-ionic/examples/81-pensando-net.rules

install -m 664 -D source/extra//usr/share/doc/kmod-redhat-ionic/examples/10-ionic.link $RPM_BUILD_ROOT//usr/share/doc/kmod-redhat-ionic/examples/10-ionic.link


%clean
rm -rf $RPM_BUILD_ROOT

%changelog
* Thu Jul 16 2020 Eugene Syromiatnikov <esyr@redhat.com> 4.18.0.210_dup8.2-2
- Bump release due to "Package build kmod-redhat-ionic-4.18.0.210_dup8.2-1.el8_2
  kept gated because not onboarded to gating".

* Thu Jul 16 2020 Eugene Syromiatnikov <esyr@redhat.com> 4.18.0.210_dup8.2-1
- 2f22e260c6b75f2acb86bd91292dc8c66f56c481
- ionic kernel module for Driver Update Program
- Resolves: #bz1851940
