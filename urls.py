from django.conf.urls.defaults import *
from livesettings import config_value, config_get_group

config = config_get_group('PAYMENT_DUMMY')

urlpatterns = patterns('',
     (r'^$', 'payment.modules.dibs.views.pay_ship_info', {'SSL':config.SSL.value}, 'DIBS_satchmo_checkout-step2'),
     (r'^confirm/$', 'payment.modules.dibs.views.confirm_info', {'SSL':config.SSL.value}, 'DIBS_satchmo_checkout-step3'),
     (r'^success/$', 'payment.views.checkout.success', {'SSL':config.SSL.value}, 'DIBS_satchmo_checkout-success'),
)
