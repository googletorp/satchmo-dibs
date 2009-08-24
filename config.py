from livesettings import *
from django.utils.translation import ugettext_lazy as _

# this is so that the translation utility will pick up the string
gettext = lambda s: s

PAYMENT_MODULES = config_get('PAYMENT', 'MODULES')
PAYMENT_MODULES.add_choice(('PAYMENT_DIBS', _('DIBS payment module')))

PAYMENT_GROUP = ConfigurationGroup('PAYMENT_DIBS',
    _('DIBS payment module settings'),
    requires=PAYMENT_MODULES,
    ordering = 100)

config_register_list(
    StringValue(PAYMENT_GROUP,
        'MERCHANT',
        description=_("DIBS merchant key"),
        hidden=False,
        default = ''),

    StringValue(PAYMENT_GROUP,
        'MD51',
        description=_("DIBS MD5 key 1"),
        hidden=False,
        default = ''),

    StringValue(PAYMENT_GROUP,
        'MD52',
        description=_("DIBS MD5 key 2"),
        hidden=False,
        default = ''),

    BooleanValue(PAYMENT_GROUP, 
        'SSL', 
        description=_("Use SSL for the module checkout pages?"), 
        default=False),
        
    BooleanValue(PAYMENT_GROUP, 
        'LIVE', 
        description=_("Accept real payments"),
        help_text=_("False if you want to be in test mode"),
        default=False),
        
    ModuleValue(PAYMENT_GROUP,
        'MODULE',
        description=_('Implementation module'),
        hidden=True,
        default = 'payment.modules.dibs'),

    StringValue(PAYMENT_GROUP,
        'KEY',
        description=_("Module key"),
        hidden=True,
        default = 'DIBS'),

    StringValue(PAYMENT_GROUP,
        'LABEL',
        description=_('English name for this group on the checkout screens'),
        default = 'Credit card',
        help_text = _('This will be passed to the translation utility')),

    StringValue(PAYMENT_GROUP,
        'URL_BASE',
        description=_('The url base used for constructing urlpatterns which will use this module'),
        default = '^credit/'),

    MultipleStringValue(PAYMENT_GROUP,
        'CREDITCHOICES',
        description=_('Available credit cards'),
        choices = (
            (('Dankort','Dankort')),
            (('VISA/Dankort','VISA/Dankort')),
            (('Visa','Visa')),
            (('Mastercard','Mastercard')),
            (('Discover','Discover')),
            (('American Express', 'American Express'))),
        default = ('Dankort', 'VISA/Dankort', 'Visa', 'Mastercard', 'Discover', 'American Express')),
        
    BooleanValue(PAYMENT_GROUP,
        'CAPTURE',
        description=_('Capture Payment immediately?'),
        default=True,
        help_text=_('IMPORTANT: If false, a capture attempt will be made when the order is marked as shipped."')),

    BooleanValue(PAYMENT_GROUP,
        'EXTRA_LOGGING',
        description=_("Verbose logs"),
        help_text=_("Add extensive logs during post."),
        default=False)
)
