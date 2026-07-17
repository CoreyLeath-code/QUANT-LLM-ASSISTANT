# Production readiness

## SLOs and alerts

For an orchestrated CLI deployment, target 99% successful research jobs excluding upstream
provider outages. Alert on a 5-minute error ratio above 5%, p95 provider latency above 8 seconds,
any credential-validation failure spike, sustained throttling, or benchmark latency above 250 ms.
Never attach prompts, provider payloads, or credentials to telemetry.

## Rollout and rollback

Build an immutable image tagged with the commit SHA. Promote through a non-production job using
stubbed credentials, then run one allowlisted-symbol canary with read-only provider keys. Increase
traffic only after error and latency checks. Roll back by restoring the prior immutable image; no
database migration is involved. The repository intentionally contains no automatic deployment or
release workflow because an environment, registry, approval policy, and secret store have not been
specified.

## Incident response

On suspected key exposure: revoke the key, stop affected jobs, rotate the secret, review provider
audit logs, and redeploy. On erroneous model output: retain redacted request metadata, suspend the
affected model/version, and reproduce with fixed inputs. Never present generated output as verified
financial advice. On data-contract failures: fail closed and investigate upstream schema/version
changes before re-enabling the feed.

## Remaining constraints

The backtester is deliberately simple: one unit of exposure, no transaction costs, slippage,
corporate actions, market calendars, liquidity constraints, or portfolio accounting. It is suitable
for deterministic examples, not investment decisions. A network service would additionally need
authentication, authorization, quotas, request IDs, structured telemetry, and abuse controls.
