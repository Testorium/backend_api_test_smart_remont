class APIV1PrefixConfig:
    prefix: str = "/v1"
    products: str = "/products"
    carts: str = "/carts"


class APIPrefixConfig:
    prefix: str = "/api"
    v1: APIV1PrefixConfig = APIV1PrefixConfig()


api_prefix_config = APIPrefixConfig()
