import os
from dataclasses import fields

import toml
from dotenv import load_dotenv

import sc_server_auth.configs.constants as c
import sc_server_auth.configs.models as m
from sc_server_auth.configs.paths import CONFIG_PATH


class Parser:
    _config: m.Config = None

    @classmethod
    def _parse(cls) -> None:
        data = toml.load(CONFIG_PATH)
        data_common = data[c.COMMON]
        data_tokens = data[c.TOKENS]
        data_server = data[c.SERVER]
        data_database = data[c.DATABASE]
        data_postgres = data_database[c.POSTGRES]
        data_google = data[c.GOOGLE]

        cls._config = m.Config(
            common=m.CommonParams(log_level=data_common[c.LOG_LEVEL]),
            tokens=m.TokensParams(
                access_token_life_span=data_tokens[c.ACCESS_TOKEN_LIFE_SPAN],
                refresh_token_life_span=data_tokens[c.REFRESH_TOKEN_LIFE_SPAN],
                bits=data_tokens[c.BITS],
                issuer=data_tokens[c.ISSUER],
            ),
            google=m.GoogleParams(
                scope=data_google[c.GOOGLE_PROFILE_SCOPE],
                secret=data_google[c.GOOGLE_SECRET],
                local_server_port=data_google[c.GOOGLE_LOCAL_SERVER_PORT],
                token_min_length=data_google[c.GOOGLE_TOKEN_MIN_LENGTH]
            ),
            server=m.ServerParams(protocol=data_server[c.PROTOCOL], host=data_server[c.HOST], port=data_server[c.PORT]),
            database=m.DatabaseParams(
                database=m.Database(data_database[c.DATABASE]),
                user=data_postgres[c.USER],
                password=data_postgres[c.PASSWORD],
                name=data_postgres[c.NAME],
                host=data_postgres[c.HOST],
                isolation_level=m.IsolationLevel(data_postgres[c.ISOLATION_LEVEL]),
            ),
        )

    @classmethod
    def get_config(cls) -> m.Config:
        if cls._config is None:
            cls._parse()
        return cls._config

    @classmethod
    def set_config_args(cls, args: m.RunArgs) -> None:
        cls._load_dotenv_args(args)
        config = cls.get_config()
        if args.host:
            config.server.host = args.host
        if args.port:
            config.server.port = args.port
        if args.database:
            config.database.database = args.database
        if args.log_level:
            config.common.log_level = args.log_level
        if args.google_secret:
            config.google.secret = args.google_secret

    @classmethod
    def _load_dotenv_args(cls, args: m.RunArgs) -> None:
        load_dotenv(dotenv_path=args.dot_env)
        for field in fields(args):
            if env_var := os.environ.get(field.name.upper()):
                setattr(args, field.name, field.type(env_var))


get_config = Parser.get_config
