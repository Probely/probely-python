from typing import Any, Dict, Generator, List, Optional

from probely.exceptions import ProbelyObjectNotFound, ProbelyRequestFailed
from probely.settings import PROBELY_API_PAGE_SIZE


class RetrieveMixin:
    def get(self, id: str) -> Any:
        """
        Retrieve a single resource by ID.
        """
        url = f"{self.resource_url}/{id}"
        resp_status_code, resp_content = self.api_client.get(url)

        if resp_status_code == 404:
            raise ProbelyObjectNotFound(id=id)

        if resp_status_code != 200:
            raise ProbelyRequestFailed(reason=resp_content)

        deserialized_data = self.model.serializer_class(**resp_content)
        return self.model(deserialized_data)

    def get_multiple(self, ids: List[str]) -> List[Any]:
        """
        Retrieve multiple resources by their IDs.
        """
        return [self.get(id) for id in ids]


class ListMixin:
    """
    Mixin providing a 'list' method to retrieve a list of resources based on filters.
    """

    def list(
        self, filters: Optional[Dict] = None, ordering: str = "-last_found"
    ) -> Generator[Any, None, None]:
        filters = filters or {}
        page = 1

        while True:
            params = {
                "ordering": ordering,
                "length": PROBELY_API_PAGE_SIZE,
                "page": page,
                **filters,
            }
            resp_status_code, resp_content = self.api_client.get(
                self.resource_url, query_params=params
            )

            if resp_status_code != 200:
                raise ProbelyRequestFailed(reason=resp_content)

            results = resp_content.get("results", [])
            total_pages_count = resp_content.get("page_total", 1)

            for item in results:
                deserialized_data = self.model.serializer_class(**item)
                yield self.model(deserialized_data)

            if page >= total_pages_count:
                break

            page += 1
