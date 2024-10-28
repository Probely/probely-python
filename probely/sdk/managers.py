from probely.sdk.mixins import ListMixin, RetrieveMixin
from probely.settings import (
    PROBELY_API_FINDINGS_URL,
)

from .models import Finding


class SdkBaseManager:
    @property
    def api_client(self):
        from probely.sdk.client import ProbelyAPIClient

        return ProbelyAPIClient


class FindingManager(RetrieveMixin, ListMixin, SdkBaseManager):
    resource_url = PROBELY_API_FINDINGS_URL
    model = Finding
