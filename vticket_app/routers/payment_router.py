from rest_framework.routers import SimpleRouter

from vticket_app.views.payment_view import PaymentView

router = SimpleRouter(False)
router.register("payment", PaymentView, "payment")

urls = router.urls