"""Cliente da Google Ads API para KeywordPlanIdeaService.GenerateKeywordIdeas.

Usa a biblioteca oficial `google-ads`. As credenciais vêm exclusivamente de variáveis
de ambiente; a lib é importada de forma preguiçosa para que o fallback manual funcione
mesmo sem ela instalada.
"""
from __future__ import annotations

import importlib.util
import os
import re
import time
from dataclasses import dataclass, field

REQUIRED_ENV = (
    "GOOGLE_ADS_DEVELOPER_TOKEN",
    "GOOGLE_ADS_CLIENT_ID",
    "GOOGLE_ADS_CLIENT_SECRET",
    "GOOGLE_ADS_REFRESH_TOKEN",
    "GOOGLE_ADS_LOGIN_CUSTOMER_ID",
)
# Conta consultada. Se ausente, usa a própria conta de login (MCC ou conta simples).
OPTIONAL_CUSTOMER_ENV = "GOOGLE_ADS_CUSTOMER_ID"

MAX_SEEDS_PER_REQUEST = 20  # limite da API para keyword_seed.keywords
PAUSE_BETWEEN_REQUESTS_S = 1.5
MAX_RETRIES = 3


class KeywordResearchError(RuntimeError):
    pass


@dataclass
class CredentialsStatus:
    missing_env: list[str] = field(default_factory=list)
    library_installed: bool = False

    @property
    def ok(self) -> bool:
        return not self.missing_env and self.library_installed

    @property
    def reason(self) -> str:
        parts = []
        if self.missing_env:
            parts.append("variáveis ausentes: " + ", ".join(self.missing_env))
        if not self.library_installed:
            parts.append("biblioteca 'google-ads' não instalada (pip install google-ads)")
        return "; ".join(parts) or "ok"


def credentials_status() -> CredentialsStatus:
    try:
        installed = importlib.util.find_spec("google.ads.googleads") is not None
    except ModuleNotFoundError:
        installed = False
    return CredentialsStatus(
        missing_env=[k for k in REQUIRED_ENV if not os.environ.get(k, "").strip()],
        library_installed=installed,
    )


def _digits(value: str) -> str:
    return re.sub(r"\D", "", value or "")


def _micros_to_currency(micros: int) -> float:
    return round((micros or 0) / 1_000_000, 2)


COMPETITION_FROM_API = {"LOW": "BAIXA", "MEDIUM": "MEDIA", "HIGH": "ALTA"}


class KeywordPlannerClient:
    def __init__(self, language_constant_id: int, geo_target_constant_ids: list[int]):
        status = credentials_status()
        if not status.ok:
            raise KeywordResearchError(status.reason)

        from google.ads.googleads.client import GoogleAdsClient

        login_customer_id = _digits(os.environ["GOOGLE_ADS_LOGIN_CUSTOMER_ID"])
        self.customer_id = _digits(os.environ.get(OPTIONAL_CUSTOMER_ENV, "")) or login_customer_id
        self.language_constant_id = language_constant_id
        self.geo_target_constant_ids = geo_target_constant_ids
        self.client = GoogleAdsClient.load_from_dict(
            {
                "developer_token": os.environ["GOOGLE_ADS_DEVELOPER_TOKEN"],
                "client_id": os.environ["GOOGLE_ADS_CLIENT_ID"],
                "client_secret": os.environ["GOOGLE_ADS_CLIENT_SECRET"],
                "refresh_token": os.environ["GOOGLE_ADS_REFRESH_TOKEN"],
                "login_customer_id": login_customer_id,
                "use_proto_plus": True,
            }
        )

    def _build_request(self, seeds: list[str]):
        gas = self.client.get_service("GoogleAdsService")
        request = self.client.get_type("GenerateKeywordIdeasRequest")
        request.customer_id = self.customer_id
        request.language = gas.language_constant_path(self.language_constant_id)
        request.geo_target_constants.extend(gas.geo_target_constant_path(g) for g in self.geo_target_constant_ids)
        request.include_adult_keywords = False
        request.keyword_plan_network = self.client.enums.KeywordPlanNetworkEnum.GOOGLE_SEARCH
        request.keyword_seed.keywords.extend(seeds)
        return request

    def generate_keyword_ideas(self, seeds: list[str]) -> list[dict]:
        """Retorna ideias com {termo, volume_mensal, cpc_medio, concorrencia, cpc_baixo, cpc_alto}."""
        from google.ads.googleads.errors import GoogleAdsException

        service = self.client.get_service("KeywordPlanIdeaService")
        ideas: list[dict] = []
        batches = [seeds[i : i + MAX_SEEDS_PER_REQUEST] for i in range(0, len(seeds), MAX_SEEDS_PER_REQUEST)]

        for index, batch in enumerate(batches):
            if index:
                time.sleep(PAUSE_BETWEEN_REQUESTS_S)
            for attempt in range(1, MAX_RETRIES + 1):
                try:
                    response = service.generate_keyword_ideas(request=self._build_request(batch))
                    for idea in response:
                        metrics = idea.keyword_idea_metrics
                        low = _micros_to_currency(metrics.low_top_of_page_bid_micros)
                        high = _micros_to_currency(metrics.high_top_of_page_bid_micros)
                        ideas.append(
                            {
                                "termo": idea.text,
                                "volume_mensal": int(metrics.avg_monthly_searches or 0),
                                "cpc_baixo": low,
                                "cpc_alto": high,
                                "cpc_medio": round((low + high) / 2, 2),
                                "concorrencia": COMPETITION_FROM_API.get(metrics.competition.name, "DESCONHECIDA"),
                            }
                        )
                    break
                except GoogleAdsException as ex:
                    codes = {e.error_code.WhichOneof("error_code") for e in ex.failure.errors}
                    retryable = "quota_error" in codes or "internal_error" in codes
                    if retryable and attempt < MAX_RETRIES:
                        time.sleep(PAUSE_BETWEEN_REQUESTS_S * 2**attempt)
                        continue
                    details = "; ".join(e.message for e in ex.failure.errors)
                    raise KeywordResearchError(f"Google Ads API ({ex.request_id}): {details}") from ex
        return ideas
