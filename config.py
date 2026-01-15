"""
Project-specific configuration

CUSTOMIZE THIS FILE FOR YOUR PROJECT
This is the only file that needs to be modified when using this manager in a different project.
"""

# ============================================================================
# AWS Configuration
# ============================================================================
ENV = "dev"
AWS_PROFILE = "xsi"
SERVICE_NAME = "xsi-mobile-tokin-plus"

# ============================================================================
# Build Settings
# ============================================================================
BUILD_SETTINGS = {
    "GOOS": "linux",
    "GOARCH": "amd64",
    "CGO_ENABLED": "0",
}

# Go build flags
BUILD_FLAGS = ["-ldflags", "-s -w"]

# ============================================================================
# Paths
# ============================================================================
FUNCTIONS_DIR = "functions"
BIN_DIR = ".bin"

# ============================================================================
# Deployment Settings
# ============================================================================
# Serverless Framework settings
SERVERLESS_STAGE = ENV
SERVERLESS_PROFILE = AWS_PROFILE

# ============================================================================
# Invoke Settings
# ============================================================================
# Method for remote invocation: "serverless" or "aws-cli"
# - "serverless": Use 'serverless invoke -f <function>' (requires serverless framework)
# - "aws-cli": Use 'aws lambda invoke' directly (requires AWS CLI)
INVOKE_REMOTE_METHOD = "serverless"

# AWS region for Lambda invocations (only used with aws-cli method)
INVOKE_AWS_REGION = "us-west-2"

# ============================================================================
# Function List
# ============================================================================
# List of Go functions to build/deploy
# UPDATE THIS LIST FOR YOUR PROJECT
GO_FUNCTIONS = [
    "status",
    "getVendedores",
    "getVendedor",
    "getVendedoresAgrupamiento",
    "getVendedoresClientes",
    "getVendedoresClientesAgrupamiento",
    "getCategoriasClientes",
    "getAperturaAdicionalesClientes",
    "getCondicionIva",
    "getCondicionVenta",
    "getCanalesClientes",
    "getSubCanalesClientes",
    "getTiposClientes",
    "getGruposClientes",
    "getClientesDirecciones",
    "getRutasVendedor",
    "getImpuestos",
    "getImpuestosArticulos",
    "getImpuestosClientes",
    "getImpuestosClientesIngresoBruto",
    "getBancos",
    "getProvincias",
    "getRubros",
    "getLocalidades",
    "getCodigosBarraArticulos",
    "getCabeceraCombos",
    "getDetalleCombos",
    "getCuentaCorriente",
    "getMediosPagos",
    "getCombos",
    "getClientes",
    "getConversiones",
    "getCabeceraDescuentos",
    "getDetalleDescuentos",
    "getTopesDescuentoListaPrecios",
    "getDetallesHistoricosVentas2",
    "getDetallesHistoricosVentas",
    "getNovedades",
    "getIncentivar",
    "getParametrosConfiguracion",
    "getParametrosConfiguracionVendedor",
    "getEmpresaDatosConfiguracion",
    "getZonas",
    "getMotivosNoScanQrClientes",
    "getMotivosOrdenesRetiro",
    "getClientesMaterialesPop",
    "getMaterialesPopGrupos",
    "getMaterialPopCaracteristicasSubgrupos",
    "getMaterialPopOpcionesCaracteristicas",
    "getMaterialPopPlanCabecera",
    "getMaterialPopPlanCanales",
    "getMaterialPopPlanClientes",
    "getMaterialPopPlanTipoMaterial",
    "getMaterialPopPlanVendedores",
    "getMobileMaterialPopPlan",
    "getMaterialPopSubgrupos",
    # New APIs - Batch Migration 2025-01-24
    "getArticulos",
    "getListaPrecios",
    "getListaPreciosDescuento",
    "getDetallePrecios",
    "getTiposRetenciones",
    "getExcusasNoLecturaBarra",
    "getExcusasNoVentas",
    "getDocumentosImputadosNoProcesados",
    "getTarjetaFocoCabecera",
    "getTarjetaFocoDetalle",
    "getTableroMes",
    "getTableroObjetivos",
    "getTableroVcMes",
    "getTableroVcObjetivos",
    "getTableroVdcObjetivos",
    "getTableroVdcSeguimiento",
    "getAvanceVenta",
    "getMaterialPopMateriales",
    # Mobile Sync Endpoints
    "postContenedorDescarga",
    "postContenedorDescargaDB",
    "processContenedor",
    "postConsultaEstadoDocumentos",
]

# ============================================================================
# Required System Dependencies
# ============================================================================
# Tools required to run this manager
# Add new dependencies here as needed
REQUIRED_DEPENDENCIES = {
    "fzf": {
        "command": "fzf",
        "check": "--version",
        "install": {
            "ubuntu": "sudo apt install fzf",
            "debian": "sudo apt install fzf",
            "macos": "brew install fzf",
            "arch": "sudo pacman -S fzf",
            "fedora": "sudo dnf install fzf",
        },
        "description": "Fuzzy finder for interactive menus",
        "required": True,
    },
    "serverless": {
        "command": "serverless",
        "check": "--version",
        "install": {"npm": "npm install -g serverless"},
        "description": "Serverless Framework CLI",
        "required": True,
    },
    "aws": {
        "command": "aws",
        "check": "--version",
        "install": {
            "ubuntu": "sudo apt install awscli",
            "debian": "sudo apt install awscli",
            "macos": "brew install awscli",
            "pip": "pip install awscli",
        },
        "description": "AWS Command Line Interface",
        "required": True,
    },
    "go": {
        "command": "go",
        "check": "version",
        "install": {
            "ubuntu": "sudo snap install go --classic",
            "macos": "brew install go",
            "arch": "sudo pacman -S go",
        },
        "description": "Go programming language",
        "required": True,
    },
    "python": {
        "command": "python",
        "check": "--version",
        "install": {
            "ubuntu": "sudo apt install python3",
            "macos": "brew install python3",
        },
        "description": "Python 3 interpreter",
        "required": True,
    },
    "pyyaml": {
        "command": "python",
        "check": "-c 'import yaml; print(yaml.__version__)'",
        "install": {"pip": "pip install pyyaml"},
        "description": "PyYAML library for Python",
        "required": False,  # Optional for YAML output
    },
}
