.SILENT:

MAKEFLAGS += --no-print-directory

QMK_USERSPACE := $(patsubst %/,%,$(dir $(shell realpath "$(lastword $(MAKEFILE_LIST))")))
ifeq ($(QMK_USERSPACE),)
    QMK_USERSPACE := $(shell pwd)
endif

PYTHON ?= python3

QMK_FIRMWARE_ROOT = $(shell qmk config -ro user.qmk_home | cut -d= -f2 | sed -e 's@^None$$@@g')

.PHONY: diagrams
diagrams:
	$(PYTHON) scripts/generate_layer_diagrams.py

%:
	test -n "$(QMK_FIRMWARE_ROOT)" || { echo 'Cannot determine qmk_firmware location. `qmk config -ro user.qmk_home` is not set'; exit 2; }
	+$(MAKE) -C $(QMK_FIRMWARE_ROOT) $(MAKECMDGOALS) QMK_USERSPACE=$(QMK_USERSPACE)
