"""Simple wrapper for standard checkout as implemented in payment.views"""

import md5
import urllib

from django.http import HttpResponseRedirect, HttpResponse
from django.core.urlresolvers import reverse
from django.views.decorators.cache import never_cache

from livesettings import config_get_group
from payment.views import confirm, payship
from satchmo_store.shop.models import Order
from payment.views.confirm import ConfirmController

    
dibs = config_get_group('PAYMENT_DIBS')
    
def pay_ship_info(request):
    return payship.simple_pay_ship_info(request, dibs, 'shop/checkout/base_pay_ship.html')
pay_ship_info = never_cache(pay_ship_info)

def confirm_info(request):
    if request.method == 'GET':
        return confirm.credit_confirm_info(request, dibs)
    controller = ConfirmController(request, dibs)
    test = controller.confirm(True)
    # Getting the settings and the order object.
    settings = config_get_group('PAYMENT_DIBS')
    order = Order.objects.from_request(request)

    # Preparing the data that we are sending to DIBS
    # Order total to be sent to DIBS must be an int specified in cents or
    # equivalent.
    order_total = int(order.total * 100)
    if settings['LIVE'].value:
        order_id = order.id
    else:
        order_id = 'TEST-%s' % order.id

    # Create md5 hash to make payment secure:
    md5_key_1 = md5.new(settings['MD51'].value + 'merchant=%s&orderid=%s&currency=%s&amount=%s' % (settings['MERCHANT'].value, order_id, settings['CURRENCY'].value, order_total)).hexdigest()
    md5_key = md5.new(settings['MD52'].value + md5_key_1).hexdigest()

    # Create the cancel and accept url, based on the request to get the host
    # and reverse to get the url.
    cancelurl = 'http://' + request.META['HTTP_HOST'] + reverse('satchmo_checkout-step1')
    accepturl = 'http://' + request.META['HTTP_HOST'] + reverse('DIBS_satchmo_checkout-success')
    callbackurl = 'http://' + request.META['HTTP_HOST'] + reverse('DIBS_satchmo_checkout-step4') + '?order_id=' + str(order.id)

    data = [
        ('merchant', settings['MERCHANT'].value),
        ('amount', order_total),
        ('currency', settings['CURRENCY'].value),
        ('orderid', order_id),
        ('accepturl', accepturl),
        ('cancelurl', cancelurl),
        ('callbackurl', callbackurl),
        #('uniqueoid', 'yes'),
        ('lang', settings['LANG'].value),
        ('md5key', md5_key),
        ('calcfee', 'yes')
        # Currently not implemented in the flex window.
        # ('delivery1', order.ship_addressee),
        # ('delivery2', order.ship_street1),
        # ('delivery3',  order.ship_postal_code + ' ' +  order.ship_city)
        ]

    if settings['CAPTURE'].value:
        data.append(('capturenow', 'yes'))
    if not settings['LIVE'].value:
        data.append(('test', 'yes'))

    send_data = urllib.urlencode(data)
    return HttpResponseRedirect('https://payment.architrade.com/paymentweb/start.action?' + send_data)
confirm_info = never_cache(confirm_info)

def paid(request):
    if request.GET.has_key('order_id'):
        order_id = int(request.GET['order_id'])
        controller = ConfirmController(request, dibs)
        try:
            order = Order.objects.get(pk=order_id)
            controller.processor.prepare_data(order)
            return HttpResponse('Succes')
        except Order.DoesNotExist:
            return HttpResponse('Failure')