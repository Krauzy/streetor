mkdir -p ~/.streamlit/

# shellcheck disable=SC2028
echo "\
[general]\n\
email = \"email@domain\"\n\
" > ~/.streamlit/credentials.toml

# shellcheck disable=SC2028
echo "\
[server]\n\
headless = true\n\
enableCORS=false\n\
port = $PORT\n\
[theme]\n\
primaryColor=\"#ae58e0\"\n\
backgroundColor=\"#202020\"\n\
secondaryBackgroundColor=\"#6717ad\"\n\
textColor=\"#ffffff\"\n\
font=\"monospace\"\n\
" > ~/.streamlit/config.toml