from dataclasses import dataclass


@dataclass
class PaymentProviderResponse:
    status: str
    reference: str | None = None
    message: str = ""


class BasePaymentProvider:
    provider_name = "base"

    def initialize(self, payment):
        raise NotImplementedError("Provider initialize must be implemented.")

    def verify(self, payment):
        raise NotImplementedError("Provider verify must be implemented.")
