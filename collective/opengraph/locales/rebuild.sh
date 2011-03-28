#!/bin/bash
cd "`dirname $0`/.."
PRODUCT=collective.opengraph
i18ndude rebuild-pot --pot locales/${PRODUCT}.pot --create $PRODUCT  .
i18ndude sync --pot locales/${PRODUCT}.pot locales/*/LC_MESSAGES/${PRODUCT}.po

    
