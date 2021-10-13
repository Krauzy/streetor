mkdir -p ~/.streamlit/

# shellcheck disable=SC2028
echo "\
[general]\n\
email = \"caiomarin26@gmail.com\"\n\
" > ~/.streamlit/credentials.toml

# shellcheck disable=SC2028
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
" > ~/.streamlit/config.toml
