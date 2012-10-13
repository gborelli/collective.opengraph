collective.opengraph
====================

This package is a part of the Plone's collective.fg bundle. It adds the opengraph metadata to your HTML head section.

Supported metadata:
 * og:site_name name of the site
 * og:url url of the webpage
 * og:title title of the webpage
 * og:description description of the webpage
 * og:image your webpage image (either 'image' field of your context or collective.contentleadimage one)

from the control panel you can manage following settings:
- the default og:type 
- which content types should be opengraph metadata aware


Customization
-------------

One of the goals of this package is to allow developers extend the default metadata definition.
It's availabe threw IOpengrapMetatags adapter::

	from collective.opengraph.interfaces IOpengraphMetatags
	from collective.opengraph.viewlets import ATMetatags

        class MyATMetatags(ATMetatags):

	    implements(IOpengrapMetatags)

	    @property
	    def metatags(self):
		tags = super(MyATMetatags, self).metatags
                tags.update({'og:newtype': 'custom value'})
                return tags


You can also customize existing og values::

	from collective.opengraph.interfaces IOpengraphMetatags
	from collective.opengraph.viewlets import ATMetatags

        class AnotherMetatags(ATMetatags):

	    implements(IOpengrapMetatags)

	    @property
            def title(self):
                return '%s - Lorem ipsum' % self.context.Title()
