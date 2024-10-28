from __future__ import annotations

from datetime import time
from enum import Enum
from typing import Dict, List, Literal, Optional, Union

from pydantic import (
    AnyUrl,
    AwareDatetime,
    BaseModel,
    EmailStr,
    Field,
)
from typing_extensions import Annotated


class NameValue(BaseModel):
    name: str
    value: str


class Severity(int, Enum):
    low = 10
    medium = 20
    high = 30


class OtpDigits(int, Enum):
    six = 6
    seven = 7
    eight = 8


class OtpAlgorithm(str, Enum):
    SHA1 = "SHA1"
    SHA256 = "SHA256"
    SHA512 = "SHA512"


class OTPTypes(str, Enum):
    TOTP = "totp"
    OTHER = "other"


class MediaType(str, Enum):
    application_json = "application/json"
    application_x_www_form_urlencoded = "application/x-www-form-urlencoded"


class VerificationMethod(str, Enum):
    file = "file"
    back_office = "back_office"
    existing_domain = "existing_domain"
    dns_txt = "dns_txt"
    dns = "dns"
    dns_cname = "dns_cname"
    meta_tag = "meta_tag"
    whitelist = "whitelist"
    email = "email"
    aws_route53 = "aws_route53"
    cloudflare = "cloudflare"
    waved = "waved"


class FindingState(str, Enum):
    notfixed = "notfixed"
    invalid = "invalid"
    accepted = "accepted"
    fixed = "fixed"


class InsertionPoint(str, Enum):
    cookie = "cookie"
    parameter = "parameter"
    arbitrary_url_param = "arbitrary_url_param"
    header = "header"
    url_folder = "url_folder"
    url_filename = "url_filename"
    json_parameter = "json_parameter"
    request_body = "request_body"
    multipart_parameter = "multipart_parameter"
    graphql_parameter = "graphql_parameter"
    non_standard_parameter = "non_standard_parameter"
    field_ = ""


class LogoutCondition(str, Enum):
    any = "any"
    all = "all"


class BasicAuth(BaseModel):
    username: Annotated[str, Field(max_length=255)]
    password: Annotated[str, Field(max_length=255)]


class TargetTypeEnum(str, Enum):
    api = "api"
    web = "single"


class ReportFileformat(str, Enum):
    pdf = "pdf"
    docx = "docx"


class ApiSchemaType(str, Enum):
    openapi = "openapi"
    postman = "postman"


class TokenParameterLocation(str, Enum):
    cookie = "cookie"
    header = "header"


class RequestResponsePairMarkdown(BaseModel):
    request: str
    response: str


class Method(str, Enum):
    get = "get"
    post = "post"
    delete = "delete"
    put = "put"
    patch = "patch"
    head = "head"
    trace = "trace"
    options = "options"
    debug = "debug"
    track = "track"
    dns = "dns"
    dns_soa = "dns_soa"
    dns_a = "dns_a"
    dns_aaaa = "dns_aaaa"
    dns_cname = "dns_cname"


class Framework(BaseModel):
    id: Annotated[
        str, Field(description="A unique Base58 value identifying this object.")
    ]
    name: Annotated[
        str,
        Field(
            description=(
                'Name of the technology.  For example, "PHP, "SQLite", "Python",'
                ' "Apache", or "Wordpress".  The maximum lenght is 255 characters.'
            ),
            max_length=255,
            title="Framework Name",
        ),
    ]
    desc: Annotated[
        str,
        Field(
            description='Description of the technology.  Defaults to "".',
            title="Framework Description",
        ),
    ]


class APIScanSettings(BaseModel):
    api_schema_type: Annotated[
        ApiSchemaType,
        Field(description=("Type of schema that defines the API.")),
    ] = ApiSchemaType.openapi
    api_schema_url: Annotated[
        Optional[AnyUrl],
        Field(description="URL to retrieve the API schema from.", max_length=2048),
    ] = None
    api_schema_file: Optional[str] = None
    custom_api_parameters: Annotated[
        List[NameValue], Field(description="Custom values for certain API parameters.")
    ]
    media_type: Annotated[
        MediaType,
        Field(description=("Format of the payload.")),
    ] = MediaType.application_json
    api_login_url: Annotated[
        Union[AnyUrl, Literal[""]],
        Field(
            description=("URL to make the authentication request to the API."),
        ),
    ]
    api_login_payload: Annotated[
        str,
        Field(
            description=("\Payload to send in the authentication request."),
            max_length=4096,
        ),
    ]
    api_login_enabled: bool = False
    api_login_token_field: Annotated[
        str,
        Field(
            description=(
                "Field containing the authentication token in the response to the"
                " authentication request."
            ),
            max_length=256,
        ),
    ]
    token_prefix: Annotated[
        str,
        Field(
            description=(
                "Prefix to add to the authentication token. "
                "For example, Bearer or JWT."
            ),
            max_length=16,
        ),
    ]
    token_parameter_name: Annotated[
        str,
        Field(
            description=(
                "Parameter name to send the authentication token. "
                "For example, `Authorization`."
            ),
            max_length=256,
        ),
    ]
    token_parameter_location: Annotated[
        Union[TokenParameterLocation, Literal[""]],
        Field(
            description=(
                "Where to send the parameter name with the authentication token and the prefix."
            )
        ),
    ]


class SimpleUser(BaseModel):
    id: Annotated[
        str, Field(description="A unique Base58 value identifying this object.")
    ]
    email: Annotated[
        EmailStr,
        Field(description="Email of the user.", max_length=254, title="Email address"),
    ] = None
    name: Annotated[str, Field(description="Name of the user.", max_length=60)]


class ScopeLabel(BaseModel):
    id: Annotated[
        str, Field(description="A unique Base58 value identifying this object.")
    ]
    name: Annotated[
        str,
        Field(
            description=("Name of the label. The maximum length is 255 characters."),
            max_length=255,
        ),
    ]
    color: Annotated[
        str,
        Field(
            description=("Color of the label"),
            pattern="^[a-zA-Z0-9#_-]*$",
        ),
    ]
    changed_by: Annotated[SimpleUser, Field(description="User who last made changes.")]
    changed: Annotated[
        AwareDatetime,
        Field(
            description=(
                "Date and time of the last change, in ISO 8601 UTC format.  For"
                ' example, "2023-08-09T13:27.43.8208302".'
            )
        ),
    ]


class FindingLabel(ScopeLabel):
    pass


class BlackoutPeriod(BaseModel):
    begin: Annotated[
        time,
        Field(
            description=(
                "Time of when the blackout period starts, in ISO 8601 UTC format. "
                ' For example, "13:27".'
            )
        ),
    ]
    cease: Annotated[
        time,
        Field(
            description=(
                "Time of when the blackout period ceases, in ISO 8601 UTC format. "
                ' For example, "13:27".'
            )
        ),
    ]
    weekdays: List[int]
    enabled: Annotated[
        bool,
        Field(description="If true, the blackout period is enabled."),
    ]
    timezone: Annotated[str, Field(max_length=64)] = "UTC"
    changed: Annotated[
        AwareDatetime,
        Field(
            description=(
                "Date and time of the last change, in ISO 8601 UTC format.  For"
                ' example, "2023-08-09T13:27.43.8208302".'
            )
        ),
    ]
    changed_by: Annotated[SimpleUser, Field(description="User who last made changes.")]


class SimpleVulnerabilityDefinition(BaseModel):
    id: str
    name: Annotated[
        str,
        Field(
            description=("Name of the vulnerability."),
            max_length=255,
        ),
    ] = None
    desc: Annotated[
        Optional[str], Field(description="Description of the vulnerability.")
    ] = None


class ScanningAgent(BaseModel):
    id: str
    name: Annotated[str, Field(max_length=255)]
    installer_generated: bool
    online: bool
    fallback: bool
    rx_bytes: int
    tx_bytes: int
    latest_handshake: int


class SimpleTeam(BaseModel):
    id: Annotated[
        str,
        Field(description="A unique Base58 value identifying this object."),
    ]
    name: Annotated[str, Field(max_length=255)]


class Target(BaseModel):
    id: Annotated[
        str, Field(description="A unique Base58 value identifying this object.")
    ]
    name: Annotated[
        str,
        Field(
            description=("Name of the target or extra host."),
            max_length=255,
        ),
    ]
    desc: Annotated[Optional[str], Field(description="Description of the target.")] = (
        None
    )
    url: Annotated[AnyUrl, Field(description="URL of the target.")]
    host: Annotated[str, Field(description="Hostname of the target.")]
    has_form_login: Annotated[
        bool,
        Field(
            description=(
                "If true, the target authentication is done through a login form."
            )
        ),
    ] = False
    form_login_url: Annotated[
        Union[AnyUrl, Literal[""]],
        Field(description="URL of the login form of the target."),
    ]
    form_login_check_pattern: Annotated[
        str,
        Field(
            description=("Pattern to check a successful login."),
            max_length=255,
        ),
    ]
    form_login: Annotated[
        Optional[List[NameValue]],
        Field(description="Field and value pairs to fill the login form."),
    ] = None
    logout_detection_enabled: Annotated[
        bool,
        Field(
            description=(
                "If true, detects any undesired logouts that may occur during scans"
                " to log back in. "
                "Requires `check_session_url` and `logout_detectors` to be defined."
            )
        ),
    ] = False
    has_sequence_login: Annotated[
        bool,
        Field(
            description=(
                "If true, the target authentication is done "
                "through a recorded login sequence."
            )
        ),
    ] = False
    has_sequence_navigation: bool
    has_basic_auth: Annotated[
        bool,
        Field(
            description=(
                "If true, the target authentication is done "
                "through username and password credentials."
            )
        ),
    ] = False
    basic_auth: Annotated[
        BasicAuth,
        Field(description="Username and password credentials for the basic auth."),
    ]
    headers: Annotated[List[NameValue], Field(description="Custom headers to send.")]
    cookies: Annotated[List[NameValue], Field(description="Custom cookies to send.")]
    whitelist: Annotated[
        List, Field(description=("Additional paths to crawl and scan."))
    ] = list()
    blacklist: Annotated[
        List,
        Field(
            description=(
                "URLs to avoid scanning. "
                "The blacklist takes precedence over the whitelist."
            )
        ),
    ] = list()
    changed: Annotated[
        AwareDatetime,
        Field(
            description=(
                "Date and time of the last change, in ISO 8601 UTC format.  For"
                ' example, "2023-08-09T13:27.43.8208302".'
            )
        ),
    ]
    changed_by: Annotated[SimpleUser, Field(description="User who last made changes.")]
    auth_enabled: Annotated[
        bool,
        Field(
            description=("If true, the target has authentication.  Defaults to false.")
        ),
    ] = False
    logout_condition: Annotated[
        LogoutCondition,
        Field(
            description=("Type of combination of the logout conditions."), max_length=3
        ),
    ] = LogoutCondition.any
    check_session_url: Annotated[str, Field(description="URL to check session.")] = ""
    has_otp: Annotated[
        bool,
        Field(description=("If true, the target has two-factor authentication (2FA).")),
    ] = False
    otp_secret: Annotated[
        str,
        Field(
            description=(
                "The seed/secret obtained when the QR code is displayed to be scanned"
                " by the third-party authenticator (TPA) app installed on the phone"
                " (e.g., Google Authenticator, 1Password, Authy, Microsoft"
                " Authenticator, etc.)."
            )
        ),
    ] = ""
    otp_algorithm: Annotated[
        OtpAlgorithm,
        Field(
            description=(
                "Secure hash algorithm (SHA) to generate the one-time password (OTP)."
            ),
            max_length=12,
        ),
    ] = OtpAlgorithm.SHA1
    otp_digits: Annotated[
        OtpDigits,
        Field(description=("Number of digits of the one-time password (OTP)")),
    ] = 6
    otp_field: Annotated[
        str,
        Field(
            description=(
                "CSS selector of the HTML element in the page to enter the one-time"
                " password (OTP). For example, a text input field."
            )
        ),
    ] = ""
    otp_submit: Annotated[
        str,
        Field(
            description=(
                "CSS selector of the HTML element in the page to submit the one-time"
                " password (OTP). For example, a button."
            )
        ),
    ] = ""
    otp_login_sequence_totp_value: Annotated[
        str,
        Field(
            description=(
                "One-time password (OTP) obtained at the time when the login sequence"
                " was recorded, i.e., the time-based one-time password (TOTP). "
                ' Defaults to "".'
            ),
            max_length=8,
        ),
    ] = ""
    otp_type: Annotated[
        OTPTypes,
        Field(description="Type of one-time password (OTP) technology", max_length=12),
    ] = OTPTypes.TOTP
    otp_url: Union[AnyUrl, Literal[""]]
    stack: Annotated[
        List[Framework],
        Field(
            description=(
                "Technologies in target scans. The scanning engine uses them to"
                " fine-tune vulnerability tests and texts about how to fix the"
                " vulnerabilities."
            )
        ),
    ]
    verified: Annotated[
        bool, Field(description="If true, the domain is verified.Read-only.")
    ]
    verification_token: Annotated[
        str,
        Field(description="Token used to verify the domain of the target.Read-only."),
    ]
    verification_date: Annotated[
        Optional[AwareDatetime],
        Field(
            description=(
                "Date and time of the verification of the domain, in ISO 8601 UTC"
                ' format.For example, "2023-08-09T13:27.43.8208302".Read-only.'
            )
        ),
    ] = None
    verification_method: Annotated[
        Union[VerificationMethod, Literal[""]],
        Field(description=("Method used in the domain verification.")),
    ] = ""
    verification_last_error: Annotated[
        str,
        Field(
            description=("Error of the last verification of the domain of the target.")
        ),
    ]
    api_scan_settings: Annotated[
        Optional[APIScanSettings],
        Field(description="Scanning settings if the target is an API."),
    ] = None


class SimpleScope(BaseModel):
    id: str
    name: Annotated[
        str,
        Field(
            description=("Name of the target.  The maximum length is 255 characters."),
            max_length=255,
        ),
    ]
    site: Annotated[
        Target,
        Field(
            description=(
                "Core settings of the target.  Includes basic target information"
                " (like the name, description, and URL) and scanning information (like"
                " the authentication and navigation sequences)."
            )
        ),
    ]
    type: Annotated[
        TargetTypeEnum,
        Field(description=("Type of target")),
    ] = TargetTypeEnum.web
    desc: Optional[str] = ""
    labels: List[ScopeLabel]
    has_assets: bool
    report_fileformat: Annotated[
        ReportFileformat,
        Field(description=("Report format for the target.")),
    ] = ReportFileformat.pdf
    scanning_agent: Optional[ScanningAgent] = None
    teams: List[SimpleTeam]
    blackout_period: Annotated[
        Optional[BlackoutPeriod],
        Field(
            description="Time window during which scans are temporarily interrupted."
        ),
    ] = None


class Finding(BaseModel):
    id: int
    target: SimpleScope
    scans: Annotated[
        List[str],
        Field(description="Scans that originated the vulnerability finding."),
    ]
    labels: List[FindingLabel]
    fix: Annotated[
        str, Field(description="Description of how to fix the vulnerability.")
    ]
    requests: Annotated[
        List[RequestResponsePairMarkdown],
        Field(
            description="Pairs of requests and responses of the vulnerability finding."
        ),
    ]
    evidence: Annotated[
        Optional[str],
        Field(description="Evidence with proof of the vulnerability finding."),
    ] = None
    extra: Annotated[
        str, Field(description="Extra details about the vulnerability finding.")
    ]
    definition: SimpleVulnerabilityDefinition
    url: Annotated[
        AnyUrl,
        Field(
            description=("URL of the vulnerability finding."),
            max_length=66000,
        ),
    ]
    path: Annotated[
        AnyUrl,
        Field(description=("URL path of the vulnerability finding")),
    ]
    method: Annotated[
        Union[Method, Literal[""]],
        Field(description=("HTTP method used in the request")),
    ]
    insertion_point: Annotated[
        InsertionPoint,
        Field(description=("Insertion point of the parameter")),
    ]
    parameter: Annotated[
        str,
        Field(
            description=("Name of the inserted parameter."),
            max_length=1024,
        ),
    ]
    value: Annotated[str, Field(description="Value of the inserted parameter.")]
    params: Annotated[
        Optional[Dict[str, List[str]]],
        Field(
            description=(
                "Query parameters of the vulnerability finding, in JSON format."
            )
        ),
    ] = None
    assignee: Optional[SimpleUser] = None
    state: Annotated[
        FindingState,
        Field(description=("State of the vulnerability finding")),
    ]
    severity: Annotated[
        Severity,
        Field(
            description=("Severity of the vulnerability finding: low, medium, or high.")
        ),
    ]
    cvss_score: Annotated[
        float,
        Field(
            description=(
                "Score of the vulnerability finding according to the Common"
                " Vulnerability Scoring System (CVSS)."
            )
        ),
    ]
    cvss_vector: Annotated[
        str,
        Field(
            description=(
                "Vector with the metrics of the score of the vulnerability finding"
                " according to the Common Vulnerability Scoring System (CVSS)."
            )
        ),
    ]
    last_found: Annotated[
        AwareDatetime,
        Field(
            description=(
                "Date and time of when the vulnerability was last found, in ISO 8601"
                ' UTC format.For example, "2023-08-09T13:27:43.8208302"'
            )
        ),
    ]
    retesting: Annotated[
        bool,
        Field(
            description=(
                "If true, the vulnerability will be retested.  If, after the"
                " retest, the vulnerability is no longer found, the vulnerability"
                " finding is marked as fixed. Otherwise, it is marked as not fixed.  "
            )
        ),
    ]
    new: Annotated[
        bool,
        Field(
            description=(
                "If true, this is a newly found vulnerability.If false, this"
                " vulnerability has been found in previous scans."
            )
        ),
    ]
    changed: Annotated[
        AwareDatetime,
        Field(
            description=(
                "Date and time of the last change, in ISO 8601 UTC format.  For"
                ' example, "2023-08-09T13:27.43.8208302".'
            )
        ),
    ]
    changed_by: Annotated[SimpleUser, Field(description="User who last made changes.")]
    comment: Annotated[str, Field(description="Comment on the object.")]
