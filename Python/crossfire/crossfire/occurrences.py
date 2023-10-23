from asyncio import Semaphore, gather, sleep
from urllib.parse import urlencode

from httpx import ReadTimeout
from tqdm import tqdm

try:
    from pandas import concat
except ImportError:
    pass

try:
    from geopandas import GeoDataFrame
except ImportError:
    pass

from crossfire.errors import CrossfireError
from crossfire.logger import Logger
from crossfire.parser import RetryAfterError

logger = Logger(__name__)

TYPE_OCCURRENCES = {"all", "withVictim", "withoutVictim"}


class UnknownTypeOccurrenceError(CrossfireError):
    def __init__(self, type_occurrence):
        message = (
            f"Unknown type_occurrence `{type_occurrence}`. "
            f"Valid formats are: {', '.join(TYPE_OCCURRENCES)}"
        )
        super().__init__(message)


class Occurrences:
    MAX_PARALLEL_REQUESTS = 16

    def __init__(
        self,
        client,
        id_state,
        id_cities=None,
        limit=None,
        type_occurrence="all",
        max_parallel_requests=None,
        format=None,
    ):
        if type_occurrence not in TYPE_OCCURRENCES:
            raise UnknownTypeOccurrenceError(type_occurrence)

        self.client = client
        self.format = format
        self.limit = limit
        self.params = {"idState": id_state, "typeOccurrence": type_occurrence}
        if id_cities:
            self.params["idCities"] = id_cities

        self.semaphore = Semaphore(max_parallel_requests or self.MAX_PARALLEL_REQUESTS)
        self.total_pages = None
        self.progress_bar = None

    async def page(self, number):
        params = self.params.copy()
        params["page"] = number
        query = urlencode(params, doseq=True)
        url = f"{self.client.URL}/occurrences?{query}"

        failed = False
        async with self.semaphore:
            try:
                occurrences, metadata = await self.client.get(url)
            except (ReadTimeout, RetryAfterError) as err:
                failed = True
                wait = getattr(err, "retry_after", 1)

        if failed:
            logger.debug(
                f"Too many requests. Waiting {wait}s before retrying page {number}"
            )
            await sleep(wait)
            return await self.page(url)

        if not self.total_pages:
            self.total_pages = metadata.page_count
            self.progress_bar.total = metadata.page_count

        self.progress_bar.update(1)
        return occurrences

    async def __call__(self):
        self.progress_bar = tqdm(desc="Loading pages", unit="page")

        data = Accumulator()
        data.merge(await self.page(1))

        if self.total_pages > 1:
            requests = tuple(self.page(n) for n in range(2, self.total_pages + 1))
            pages = await gather(*requests)
            data.merge(*pages)

        return data()


class Accumulator:
    def __init__(self, *pages):
        self.data = None
        self.is_gdf = False

    def save_first(self, *pages):
        self.data, *remaining = pages
        if isinstance(self.data, GeoDataFrame):
            self.is_gdf = True
        return self if not remaining else self.merge(remaining)

    def merge(self, *pages):
        if self.data is None:
            return self.save_first(*pages)

        if isinstance(self.data, list):
            for page in pages:
                self.data.extend(page)
            return self

        dfs = [self.data] + list(pages)
        self.data = concat(dfs, ignore_index=True)
        return self

    def __call__(self):
        if self.is_gdf:
            return GeoDataFrame(self.data)

        return self.data
