import os


class TestDatabaseConfig:
    driver: str = "postgresql+asyncpg"
    user: str | None = os.getenv("TEST_POSTGRES_USER")
    password: str | None = os.getenv("TEST_POSTGRES_PASSWORD")
    host: str | None = os.getenv("TEST_POSTGRES_HOST")
    port: str | None = os.getenv("TEST_POSTGRES_PORT")
    db_name: str | None = os.getenv("TEST_POSTGRES_DB")

    echo: bool = os.getenv("DB_ECHO", "false").lower() == "true"
    echo_pool: bool = os.getenv("DB_ECHO_POOL", "false").lower() == "true"
    pool_size: int = int(os.getenv("DB_POOL_SIZE", 10))
    max_overflow: int = int(os.getenv("DB_MAX_OVERFLOW", 50))

    @property
    def dns(self) -> str:
        return f"{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.db_name}"


test_db_config = TestDatabaseConfig()
