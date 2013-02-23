SUBDIRS := xfwm4 garcon xfce4-settings-qubes

help:
	@echo "make rpms        -- generate binary rpm packages"
	@echo "make srpms       -- generate source rpm packages"

%:
	@for dir in $(SUBDIRS); do \
	    $(MAKE) -C $$dir $* || exit 1;\
	done
