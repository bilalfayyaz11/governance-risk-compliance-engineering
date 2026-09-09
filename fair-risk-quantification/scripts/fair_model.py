#!/usr/bin/env python3

from dataclasses import dataclass
from typing import Callable, Dict

import numpy as np
from scipy.special import expit
from scipy.stats import beta as beta_dist


DEFAULT_SEED = 42


@dataclass
class FairNode:
    name: str
    dist_type: str
    params: dict
    seed: int | None = None

    def _rng(self) -> np.random.Generator:
        return np.random.default_rng(
            self.seed
        )

    @staticmethod
    def _sample_pert(
        rng: np.random.Generator,
        minimum: float,
        mode: float,
        maximum: float,
        n: int,
        lamb: float = 4.0,
    ) -> np.ndarray:
        """
        Sample from a Beta-PERT distribution.

        PERT mean:
            (min + lambda*mode + max) / (lambda + 2)

        Beta reparameterization:
            alpha = 1 + lambda * (mode-min)/(max-min)
            beta  = 1 + lambda * (max-mode)/(max-min)

        Output is rescaled from [0,1] to [min,max].
        """
        if maximum < minimum:
            raise ValueError(
                f"{maximum=} must be >= {minimum=}"
            )

        if not (
            minimum <= mode <= maximum
        ):
            raise ValueError(
                "PERT mode must lie between min and max"
            )

        if maximum == minimum:
            return np.full(
                n,
                minimum,
                dtype=float,
            )

        alpha = (
            1.0
            + lamb
            * (
                (mode - minimum)
                / (maximum - minimum)
            )
        )

        beta_param = (
            1.0
            + lamb
            * (
                (maximum - mode)
                / (maximum - minimum)
            )
        )

        samples = beta_dist.rvs(
            alpha,
            beta_param,
            size=n,
            random_state=rng,
        )

        return (
            minimum
            + samples
            * (
                maximum
                - minimum
            )
        )

    @staticmethod
    def _lognormal_from_quantiles(
        rng: np.random.Generator,
        minimum: float,
        mode_like: float,
        maximum: float,
        n: int,
    ) -> np.ndarray:
        """
        Build a practical right-skewed lognormal approximation.

        The supplied minimum and maximum are treated approximately
        as lower/upper calibration bounds, while mode_like anchors
        the central tendency.

        Samples are clipped to the supplied physical bounds.
        """
        if minimum <= 0:
            minimum = 1e-9

        if mode_like <= 0:
            raise ValueError(
                "Lognormal center must be > 0"
            )

        if maximum <= minimum:
            return np.full(
                n,
                minimum,
                dtype=float,
            )

        lower_log = np.log(
            minimum
        )

        upper_log = np.log(
            maximum
        )

        sigma = max(
            (
                upper_log
                - lower_log
            )
            / 4.0,
            1e-6,
        )

        mu = np.log(
            mode_like
        )

        samples = rng.lognormal(
            mean=mu,
            sigma=sigma,
            size=n,
        )

        return np.clip(
            samples,
            minimum,
            maximum,
        )

    def sample(
        self,
        n: int,
    ) -> np.ndarray:
        if n <= 0:
            raise ValueError(
                "n must be positive"
            )

        rng = self._rng()

        dist_type = (
            self.dist_type
            .strip()
            .lower()
        )

        if dist_type == "pert":
            values = self._sample_pert(
                rng=rng,
                minimum=float(
                    self.params["min"]
                ),
                mode=float(
                    self.params["mode"]
                ),
                maximum=float(
                    self.params["max"]
                ),
                n=n,
                lamb=float(
                    self.params.get(
                        "lambda",
                        4.0,
                    )
                ),
            )

        elif dist_type == "lognormal":
            values = (
                self._lognormal_from_quantiles(
                    rng=rng,
                    minimum=float(
                        self.params["min"]
                    ),
                    mode_like=float(
                        self.params[
                            "mode"
                        ]
                    ),
                    maximum=float(
                        self.params["max"]
                    ),
                    n=n,
                )
            )

        elif dist_type == "poisson":
            lam = float(
                self.params["lam"]
            )

            if lam < 0:
                raise ValueError(
                    "Poisson lambda must be >= 0"
                )

            values = rng.poisson(
                lam=lam,
                size=n,
            ).astype(float)

        elif dist_type == "beta":
            alpha = float(
                self.params["alpha"]
            )

            beta_param = float(
                self.params["beta"]
            )

            minimum = float(
                self.params.get(
                    "min",
                    0.0,
                )
            )

            maximum = float(
                self.params.get(
                    "max",
                    1.0,
                )
            )

            base = rng.beta(
                alpha,
                beta_param,
                size=n,
            )

            values = (
                minimum
                + base
                * (
                    maximum
                    - minimum
                )
            )

        elif dist_type == "constant":
            values = np.full(
                n,
                float(
                    self.params["value"]
                ),
                dtype=float,
            )

        else:
            raise ValueError(
                f"Unsupported distribution: {self.dist_type}"
            )

        return np.nan_to_num(
            values,
            nan=0.0,
            posinf=0.0,
            neginf=0.0,
        )


def derive_vulnerability(
    threat_capability: np.ndarray,
    control_strength: np.ndarray,
) -> np.ndarray:
    """
    Convert Threat Capability vs Control Strength into a
    bounded probability of successful compromise.

    Difference is normalized to approximately [-5,5]
    before logistic transformation.

    TC == CS gives vulnerability near 0.50.
    Stronger controls reduce vulnerability.
    Stronger threat capability increases vulnerability.
    """
    if (
        threat_capability.shape
        != control_strength.shape
    ):
        raise ValueError(
            "TC and CS arrays must have matching shapes"
        )

    delta = (
        threat_capability
        - control_strength
    )

    scaled_delta = (
        delta
        / 10.0
    )

    vulnerability = expit(
        scaled_delta
    )

    return np.clip(
        vulnerability,
        0.001,
        0.999,
    )


def build_risk_model(
    nodes: Dict[str, FairNode],
) -> Callable[[int], np.ndarray]:
    """
    Compose FAIR factors into vectorized ALE samples.

    LEF:
        TEF × Vulnerability

    Primary Loss:
        Incident Response
        + System Recovery
        + Legal / Notification

    Secondary Loss:
        Conditional secondary-loss event
        × (
            Regulatory
            + Reputation / Attrition
            + Third-Party Dispute
        )

    LM:
        Primary Loss + Secondary Loss

    ALE:
        LEF × LM
    """

    required = {
        "tef",
        "threat_capability",
        "control_strength",
        "primary_incident_response",
        "primary_system_recovery",
        "primary_legal_notification",
        "secondary_probability",
        "secondary_regulatory",
        "secondary_reputation",
        "secondary_third_party",
    }

    missing = (
        required
        - set(nodes)
    )

    if missing:
        raise ValueError(
            "Missing FAIR nodes: "
            + ", ".join(
                sorted(missing)
            )
        )

    def model(
        n: int,
    ) -> np.ndarray:
        tef = np.clip(
            nodes["tef"].sample(n),
            0.0,
            None,
        )

        threat_capability = np.clip(
            nodes[
                "threat_capability"
            ].sample(n),
            0.0,
            100.0,
        )

        control_strength = np.clip(
            nodes[
                "control_strength"
            ].sample(n),
            0.0,
            100.0,
        )

        vulnerability = derive_vulnerability(
            threat_capability,
            control_strength,
        )

        lef = np.clip(
            tef
            * vulnerability,
            0.0,
            None,
        )

        primary = (
            np.clip(
                nodes[
                    "primary_incident_response"
                ].sample(n),
                0.0,
                None,
            )
            +
            np.clip(
                nodes[
                    "primary_system_recovery"
                ].sample(n),
                0.0,
                None,
            )
            +
            np.clip(
                nodes[
                    "primary_legal_notification"
                ].sample(n),
                0.0,
                None,
            )
        )

        secondary_probability = np.clip(
            nodes[
                "secondary_probability"
            ].sample(n),
            0.0,
            1.0,
        )

        secondary_occurs = (
            np.random.default_rng(
                DEFAULT_SEED + 100
            )
            .random(n)
            < secondary_probability
        )

        secondary_magnitude = (
            np.clip(
                nodes[
                    "secondary_regulatory"
                ].sample(n),
                0.0,
                None,
            )
            +
            np.clip(
                nodes[
                    "secondary_reputation"
                ].sample(n),
                0.0,
                None,
            )
            +
            np.clip(
                nodes[
                    "secondary_third_party"
                ].sample(n),
                0.0,
                None,
            )
        )

        secondary = (
            secondary_occurs.astype(float)
            * secondary_magnitude
        )

        loss_magnitude = np.clip(
            primary
            + secondary,
            0.0,
            None,
        )

        ale = np.clip(
            lef
            * loss_magnitude,
            0.0,
            None,
        )

        return ale

    return model


def build_default_nodes(
    control_strength_multiplier: float = 1.0,
) -> Dict[str, FairNode]:
    """
    Construct the baseline scenario.

    control_strength_multiplier can be used later for
    sensitivity analysis.

    Example:
        1.20 = 20% stronger control estimates
    """
    cs_min = min(
        100.0,
        50.0
        * control_strength_multiplier,
    )

    cs_mode = min(
        100.0,
        72.0
        * control_strength_multiplier,
    )

    cs_max = min(
        100.0,
        92.0
        * control_strength_multiplier,
    )

    return {
        "tef": FairNode(
            name="Threat Event Frequency",
            dist_type="pert",
            params={
                "min": 1,
                "mode": 4,
                "max": 12,
            },
            seed=DEFAULT_SEED + 1,
        ),

        "threat_capability": FairNode(
            name="Threat Capability",
            dist_type="pert",
            params={
                "min": 45,
                "mode": 70,
                "max": 95,
            },
            seed=DEFAULT_SEED + 2,
        ),

        "control_strength": FairNode(
            name="Control Strength",
            dist_type="pert",
            params={
                "min": cs_min,
                "mode": cs_mode,
                "max": cs_max,
            },
            seed=DEFAULT_SEED + 3,
        ),

        "primary_incident_response": FairNode(
            name="Primary Loss - Incident Response",
            dist_type="pert",
            params={
                "min": 75000,
                "mode": 220000,
                "max": 900000,
            },
            seed=DEFAULT_SEED + 4,
        ),

        "primary_system_recovery": FairNode(
            name="Primary Loss - System Recovery",
            dist_type="pert",
            params={
                "min": 40000,
                "mode": 130000,
                "max": 600000,
            },
            seed=DEFAULT_SEED + 5,
        ),

        "primary_legal_notification": FairNode(
            name="Primary Loss - Legal and Notification",
            dist_type="pert",
            params={
                "min": 50000,
                "mode": 175000,
                "max": 700000,
            },
            seed=DEFAULT_SEED + 6,
        ),

        "secondary_probability": FairNode(
            name="Secondary Loss Probability",
            dist_type="pert",
            params={
                "min": 0.20,
                "mode": 0.55,
                "max": 0.90,
            },
            seed=DEFAULT_SEED + 7,
        ),

        "secondary_regulatory": FairNode(
            name="Secondary Loss - Regulatory",
            dist_type="lognormal",
            params={
                "min": 100000,
                "mode": 650000,
                "max": 4000000,
            },
            seed=DEFAULT_SEED + 8,
        ),

        "secondary_reputation": FairNode(
            name="Secondary Loss - Reputation and Attrition",
            dist_type="lognormal",
            params={
                "min": 150000,
                "mode": 900000,
                "max": 6000000,
            },
            seed=DEFAULT_SEED + 9,
        ),

        "secondary_third_party": FairNode(
            name="Secondary Loss - Third-Party Dispute",
            dist_type="lognormal",
            params={
                "min": 50000,
                "mode": 300000,
                "max": 1800000,
            },
            seed=DEFAULT_SEED + 10,
        ),
    }


def summarize_samples(
    samples: np.ndarray,
) -> dict:
    return {
        "count":
            int(
                samples.size
            ),

        "mean":
            float(
                np.mean(samples)
            ),

        "p10":
            float(
                np.percentile(
                    samples,
                    10,
                )
            ),

        "p50":
            float(
                np.percentile(
                    samples,
                    50,
                )
            ),

        "p90":
            float(
                np.percentile(
                    samples,
                    90,
                )
            ),

        "p95":
            float(
                np.percentile(
                    samples,
                    95,
                )
            ),

        "p99":
            float(
                np.percentile(
                    samples,
                    99,
                )
            ),

        "max":
            float(
                np.max(samples)
            ),
    }


def main() -> None:
    nodes = build_default_nodes()

    model = build_risk_model(
        nodes
    )

    samples = model(
        50000
    )

    summary = summarize_samples(
        samples
    )

    print(
        "FAIR MODEL SMOKE TEST"
    )

    print(
        "=" * 60
    )

    for key, value in summary.items():
        if key == "count":
            print(
                f"{key}: {value}"
            )
        else:
            print(
                f"{key}: ${value:,.2f}"
            )


if __name__ == "__main__":
    main()
