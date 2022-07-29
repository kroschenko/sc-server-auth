# SC-server-auth

Authentication server for sc-machine repository

To install poetry run command:

```shell
curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3 - 
```

or just do it with pip3 (not recommended):

```shell
pip3 install poetry
```

To install dependencies run command:

```shell
poetry env use 3.8
poetry shell
poetry install
```

Activate the virtual environment is to create a new shell with **_poetry shell_**.
To deactivate the virtual environment and **_exit_** this new shell type exit.
To deactivate the virtual environment without leaving the shell use **_deactivate_**.

To install pre-commit run next command (this command and others below run in poetry environment):

```shell
pre-commit install
```

## PostgreSQL (optional)

```shell
sudo apt install postgresql postgresql-contrib
```

Commands to create database and user for it.

```shell
sudo -u postgres psql
```

```postgresql
create database sc_auth;
create user sc_auth with encrypted password 'sc_auth';
grant all privileges on database sc_auth to sc_auth;
```

**Activation**

Set postgres in sc_server_auth/configs/settings.toml or as argument in server run script

**Insert default values (after server running)**

```shell
psql -U sc_auth -h localhost -d sc_auth
```

Write password "sc_auth" and run command:

```postgresql
insert into "user"(id, name, password)
values (1, 'admin', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3');
```

## Local-CI tool

For checking your branch before pushing just run next command:

```shell
./scripts/local_ci.sh [-h] [-t] [-c] [-i] [-b] [-p] [-a]
```

For sorting imports and clean code with black run next command:

```shell
./scripts/sort_imports.sh [-h] [-i] [-b] [-a]
```

## Running

To start auth-server run command:

```shell
python -m sc_server_auth [-h] [-H HOST] [-p PORT] [-d DATABASE] [-l LOG_LEVEL] [-r] [-e DOT_ENV] [-g GOOGLE_SECRET_FILE_PATH]
```

Google secret file you can get in [Google Developer Console](https://console.developers.google.com/)

Creating project [tutorial](https://developers.google.com/workspace/guides/create-project)
Getting client_secret.json file [tutorial](https://help.talend.com/r/en-US/7.2/google-drive/how-to-access-google-drive-using-client-secret-json-file-the)
By default secret file located in the root folder.

After server running you can check endpoints docs by link: http://127.0.0.1:5000/docs

If you don't have keys in sc-server-auth folder you can generate them by making a request to generate token. After that
keys will generate automatically.

Current credentials to test:
login - admin, password - a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3 (SHA256 hash)
