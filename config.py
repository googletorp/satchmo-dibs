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
    BooleanValue(PAYMENT_GROUP,
        'LIVE',
        description=_("Accept real payments"),
        help_text=_("False if you want to be in test mode"),
        default=False,
        ordering=1
    ),

    StringValue(PAYMENT_GROUP,
        'MERCHANT',
        description=_("DIBS merchant key"),
        hidden=False,
        default = '',
        ordering=5
    ),

    StringValue(PAYMENT_GROUP,
        'MD51',
        description=_("DIBS MD5 key 1"),
        hidden=False,
        default = '',
        ordering=6
    ),

    StringValue(PAYMENT_GROUP,
        'MD52',
        description=_("DIBS MD5 key 2"),
        hidden=False,
        default = '',
        ordering=6
    ),

    BooleanValue(PAYMENT_GROUP, 
        'SSL', 
        description=_("Use SSL for the module checkout pages?"), 
        default=False,
        ordering=7
    ),

    ModuleValue(PAYMENT_GROUP,
        'MODULE',
        description=_('Implementation module'),
        hidden=True,
        default = 'payment.modules.dibs',
        ordering=7
    ),

    StringValue(PAYMENT_GROUP,
        'KEY',
        description=_("Module key"),
        hidden=True,
        default = 'DIBS'
    ),

    StringValue(PAYMENT_GROUP,
        'LABEL',
        description=_('English name for this group on the checkout screens'),
        default = 'Credit cards',
        help_text = _('This will be passed to the translation utility'),
        ordering=7
    ),

    StringValue(PAYMENT_GROUP,
        'URL_BASE',
        description=_('The url base used for constructing urlpatterns which will use this module'),
        default = '^creditcard/',
        ordering=7
    ),

    MultipleStringValue(PAYMENT_GROUP,
        'CREDITCHOICES',
        description=_('Available credit cards'),
        choices = (
            (('Dankort','Dankort')),
            (('VISA/Dankort','VISA/Dankort')),
            (('Visa','Visa')),
            (('Mastercard','Mastercard')),
            (('Discover','Discover')),
            (('American Express', 'American Express'))
        ),
        default = ('Dankort', 'VISA/Dankort', 'Visa', 'Mastercard', 'Discover', 'American Express'),
        ordering=2
    ),
        
    BooleanValue(PAYMENT_GROUP,
        'CAPTURE',
        description=_('Capture Payment immediately?'),
        default=True,
        help_text=_('IMPORTANT: If false, a capture attempt will be made when the order is marked as shipped."'),
        ordering=1
    ),

    BooleanValue(PAYMENT_GROUP,
        'EXTRA_LOGGING',
        description=_("Verbose logs"),
        help_text=_("Add extensive logs during post."),
        default=False,
        ordering=7
    ),

    StringValue(PAYMENT_GROUP,
        'CURRENCY',
        description=_('Select shop currency used for payments.'),
        choices = (
            (('208', 'Danish Crowns (DKK)')),
            (('978', 'Euro (EUR)')),
            (('840', 'US Dollar (USD)')),
            (('826', 'English Pound (GBP)')),
            (('752', 'Swedish Kroner (SEK)')),
            (('036', 'Australian Dollar (AUD)')),
            (('124', 'Canadian Dollar (CAD)')),
            (('352', 'Icelandic Kroner (ISK)')),
            (('392', 'Japanese Yen (JPY)')),
            (('554', 'New Zealand Dollar (NZD)')),
            (('578', 'Norwegian Kroner (NOK)')),
            (('756', 'Swiss Franc (CHF)')),
            (('949', 'Turkish Lire (TRY)'))
        ),
        default = '208',
        ordering=2
    ),

    StringValue(PAYMENT_GROUP,
        'ORDERID_PREFIX',
        description=_("DIBS orderid prefix"),
        default = '',
        ordering=4
    ),

    StringValue(PAYMENT_GROUP,
        'ORDERID_SUFIX',
        description=_("DIBS orderid suffix"),
        hidden=False,
        default = '',
        ordering=4
    ),

    StringValue(PAYMENT_GROUP,
        'LANG',
        description=_("Language of DIBS flexwin"),
        default='da',
        choices= (
            (('da', 'Danish')),
            (('sv', 'Swedish')),
            (('no', 'Norwegian')),
            (('en', 'English')),
            (('nl', 'Dutch')),
            (('de', 'German')),
            (('fr', 'French')),
            (('fi', 'Finnish')),
           (('es', 'Spanish')),
            (('it', 'Italian')),
            (('fo', 'Faroese')),
            (('pl', 'Polish')),
            ),
        ordering=3
    ),

    StringValue(PAYMENT_GROUP,
        'COLOR',
        description=_("The colour of the DIBS flexwin"),
        default='blue',
        choices=(
            (('blue', 'Blue')),
            (('gray', 'Gray')),
            (('sand', 'Sand'))
            ),
        ordering=3
    ),
)
