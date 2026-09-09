-- GCC Regulatory Control Mapping Schema
--
-- Design decision: crosswalks are stored once per unordered control pair.
-- source_control_id must always be less than target_control_id. This prevents
-- duplicate bidirectional rows such as A->B and B->A while still allowing the
-- application to query mappings in either direction.
--
-- Design decision: framework versions are separate framework records.
-- Example: NCA ECC 1-2018 and NCA ECC 2-2024 would each have their own row.
-- Controls therefore remain historically traceable to the exact framework version.
--
-- Design decision: orphan controls require no special placeholder mapping.
-- A control with no equivalent simply has no row in crosswalks. This preserves
-- the distinction between "not yet mapped" and "no valid equivalent" through
-- analyst rationale and reporting logic.

DROP TABLE IF EXISTS control_overlays CASCADE;
DROP TABLE IF EXISTS crosswalks CASCADE;
DROP TABLE IF EXISTS controls CASCADE;
DROP TABLE IF EXISTS overlays CASCADE;
DROP TABLE IF EXISTS frameworks CASCADE;
DROP TYPE IF EXISTS mapping_strength_enum;

CREATE TYPE mapping_strength_enum AS ENUM (
    'exact',
    'partial',
    'related'
);

CREATE TABLE frameworks (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    version VARCHAR(50) NOT NULL,
    jurisdiction VARCHAR(100) NOT NULL,
    authority VARCHAR(200) NOT NULL,
    UNIQUE (name, version)
);

CREATE TABLE controls (
    id SERIAL PRIMARY KEY,
    framework_id INTEGER NOT NULL
        REFERENCES frameworks(id)
        ON DELETE CASCADE,
    control_ref VARCHAR(100) NOT NULL,
    domain VARCHAR(200) NOT NULL,
    title VARCHAR(300) NOT NULL,
    description TEXT NOT NULL,
    control_type VARCHAR(100),
    UNIQUE (framework_id, control_ref)
);

CREATE TABLE crosswalks (
    source_control_id INTEGER NOT NULL
        REFERENCES controls(id)
        ON DELETE CASCADE,
    target_control_id INTEGER NOT NULL
        REFERENCES controls(id)
        ON DELETE CASCADE,
    mapping_strength mapping_strength_enum NOT NULL,
    rationale TEXT NOT NULL,
    PRIMARY KEY (
        source_control_id,
        target_control_id
    ),
    CHECK (
        source_control_id < target_control_id
    )
);

CREATE TABLE overlays (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    description TEXT NOT NULL,
    trigger_condition TEXT NOT NULL
);

CREATE TABLE control_overlays (
    control_id INTEGER NOT NULL
        REFERENCES controls(id)
        ON DELETE CASCADE,
    overlay_id INTEGER NOT NULL
        REFERENCES overlays(id)
        ON DELETE CASCADE,
    PRIMARY KEY (
        control_id,
        overlay_id
    )
);

CREATE INDEX idx_controls_control_ref
    ON controls(control_ref);

CREATE INDEX idx_controls_framework_id
    ON controls(framework_id);

CREATE INDEX idx_controls_domain
    ON controls(domain);

CREATE INDEX idx_crosswalks_source
    ON crosswalks(source_control_id);

CREATE INDEX idx_crosswalks_target
    ON crosswalks(target_control_id);

CREATE INDEX idx_control_overlays_control
    ON control_overlays(control_id);

CREATE INDEX idx_control_overlays_overlay
    ON control_overlays(overlay_id);

INSERT INTO overlays (
    name,
    description,
    trigger_condition
)
VALUES
(
    'data_residency',
    'Requires regulated or sensitive data to remain within an approved national jurisdiction.',
    'Control text references in-country storage, national data residency, domestic processing, or restrictions on cross-border data transfer.'
),
(
    'arabic_logging',
    'Requires Arabic-language or Arabic-readable logging, reporting, or audit evidence.',
    'Control text references Arabic-language audit logs, Arabic reporting, or local-language audit evidence.'
),
(
    'national_cert_reporting',
    'Requires incidents to be reported to a national cybersecurity authority or national CERT.',
    'Control text references mandatory notification to a national CERT, regulator, or cybersecurity authority within a specified timeline.'
),
(
    'local_hosting_mandate',
    'Requires systems, services, or regulated workloads to be hosted locally or within an approved national environment.',
    'Control text references local hosting, domestic cloud regions, in-country infrastructure, or regulator-approved hosting locations.'
);
